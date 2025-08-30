from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import logging

# Configurar logging para que Render muestre más info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "s3cr3t2025!")

# 🔹 Conexión a MySQL (Railway)
def get_conn():
    try:
        host = os.getenv("MYSQLHOST")
        port = os.getenv("MYSQLPORT")
        user = os.getenv("MYSQLUSER")
        password = os.getenv("MYSQLPASSWORD")
        database = os.getenv("MYSQLDATABASE")

        # Mostrar valores en logs (sin exponer la contraseña completa)
        logger.info(f"Intentando conectar a MySQL:")
        logger.info(f"  HOST={host}")
        logger.info(f"  PORT={port}")
        logger.info(f"  USER={user}")
        logger.info(f"  DB={database}")

        conn = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database
        )
        return conn
    except Error as e:
        logger.error(f"❌ Error conectando a MySQL: {e}")
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
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO guestbook (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
        conn.commit()
        logger.info(f"✅ Registro insertado: {name}, {email}, {message}")
        flash("✅ ¡Gracias! Tus datos se guardaron correctamente.", "success")
    except Error as e:
        logger.error(f"❌ Error insertando en BD: {e}")
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
