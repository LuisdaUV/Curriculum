from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-me")

def get_conn():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "cv_site")
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    consent = request.form.get("consent") == "on"

    if not (name and email and message and consent):
        flash("Por favor completa todos los campos y acepta el consentimiento.", "error")
        return redirect(url_for("index"))

    conn = get_conn()
    if conn is None:
        flash("No se pudo conectar a la base de datos. Verifica tu configuración.", "error")
        return redirect(url_for("index"))

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO guestbook (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
        conn.commit()
        flash("¡Gracias! Tus datos se han guardado correctamente.", "success")
    except Error as e:
        print("DB insert error:", e)
        flash("Ocurrió un error al guardar en la base de datos.", "error")
    finally:
        try:
            conn.close()
        except:
            pass

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
