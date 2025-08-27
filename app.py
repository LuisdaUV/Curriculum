from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambia-esto")

# 🔹 Conexión a MySQL (Railway)
def get_conn():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST", "mysql.railway.internal"),
            port=int(os.getenv("MYSQLPORT", "3306")),
            user=os.getenv("MYSQLUSER", "root"),
            password=os.getenv("MYSQLPASSWORD", ""),
            database=os.getenv("MYSQLDATABASE", "railway")
        )
        return conn
    except Error as e:
        print("❌ Error conectando a MySQL:", e)
        return None

# 🔹 Inicializar base de datos (crear tabla si no existe)
def init_db():
    conn = get_conn()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS guestbook (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(150) NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()
            print("✅ Tabla 'guestbook' verificada/creada.")
        except Error as e:
            print("❌ Error creando/verificando la tabla:", e)
        finally:
            conn.close()
    else:
        print("⚠️ No se pudo conectar a la base de datos en init_db().")

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
    except Error as e:
        print("❌ Error insertando en BD:", e)
        flash("⚠️ Ocurrió un error al guardar en la base de datos.", "error")
    finally:
        try:
            conn.close()
        except:
            pass

    return redirect(url_for("index"))

# Para correr localmente o en Render
if __name__ == "__main__":
    init_db()  # 🔹 Verifica o crea la tabla antes de arrancar la app
    app.run(host="0.0.0.0", port=5000, debug=True)
