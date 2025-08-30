from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno (.env en local, Railway en producción)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "s3cr3t2025!")  # valor por defecto

# 🔹 Conexión a MySQL (Railway)
def get_conn():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),              # Host
            port=int(os.getenv("MYSQLPORT", "3306")), # Puerto
            user=os.getenv("MYSQLUSER"),              # Usuario
            password=os.getenv("MYSQLPASSWORD"),      # Contraseña
            database=os.getenv("MYSQL_DATABASE")      # Base de datos
        )
        print("✅ Conexión a MySQL establecida")
        return conn
    except Error as e:
        print("❌ Error conectando a MySQL:", e)
        return None

# Página principal
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Guardar datos del formulario
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    consent = request.form.get("consent") == "on"

    if not (name and email and message and consent):
        flash("⚠️ Completa todos los campos y acepta el consentimiento.", "error")
        return redirect(url_for("index"))

    conn = get_conn()
    if conn is None:
        flash("❌ No se pudo conectar a la base de datos.", "error")
        return redirect(url_for("index"))

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO guestbook (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        flash("✅ ¡Gracias! Tus datos se guardaron correctamente.", "success")
    except Error as e:
        print("❌ Error insertando en BD:", e)
        flash("⚠️ Ocurrió un error al guardar en la base de datos.", "error")
    finally:
        try:
            conn.close()
        except:
            pass

    return redirect(url_for("index"))

# Para correr localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
