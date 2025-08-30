from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno (.env en local, Railway en producción)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "s3cr3t2025!")

# 🔹 Conexión a MySQL (Railway)
def get_conn():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "localhost"),
            port=int(os.getenv("MYSQLPORT", "3306")),
            user=os.getenv("MYSQLUSER", "flaskuser"),
            password=os.getenv("MYSQLPASSWORD", "FlaskPass2025!"),
            database=os.getenv("MYSQLDATABASE", "railway")
        )
        return conn
    except Error as e:
        print("❌ Error conectando a MySQL:", e)
        return None


# 🔹 Test de conexión al iniciar Render
try:
    print("🔍 Probando conexión con las siguientes variables:")
    print("  MYSQLUSER =", os.getenv("MYSQLUSER"))
    print("  MYSQLPASSWORD =", os.getenv("MYSQLPASSWORD")[:3] + "***")  # ocultamos parte
    print("  MYSQLHOST =", os.getenv("MYSQLHOST"))
    print("  MYSQLPORT =", os.getenv("MYSQLPORT"))
    print("  MYSQLDATABASE =", os.getenv("MYSQLDATABASE"))

    conn = get_conn()
    if conn:
        print("✅ Conexión inicial exitosa a MySQL")
        conn.close()
    else:
        print("❌ No se pudo conectar en el arranque")
except Exception as e:
    print("⚠️ Error en el test inicial:", e)


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
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO guestbook (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
        conn.commit()
        flash("✅ ¡Gracias! Tus datos se guardaron correctamente.", "success")
        return redirect(url_for("index"))   # 🔹 redirigir siempre aquí
    except Error as e:
        print("❌ Error insertando en BD:", e)
        flash("⚠️ Ocurrió un error al guardar en la base de datos.", "error")
        return redirect(url_for("index"))   # 🔹 manejar también el error con redirect
    finally:
        try:
            conn.close()
        except:
            pass


    return redirect(url_for("index"))


# Para correr localmente
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
