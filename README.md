# Sitio CV en Flask + MySQL

Este proyecto crea una página web de tu hoja de vida con barras de habilidades, área de contenido personal, información personal y un formulario que guarda datos del visitante en MySQL.

## Requisitos
- Python 3.10+
- MySQL 8+
- (Opcional) Virtualenv

## Instalación
```bash
cd cv_site_flask
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Base de datos
1. Inicia MySQL y ejecuta el archivo `db.sql`:
```sql
SOURCE db.sql;
```

2. Copia `.env.example` a `.env` y coloca tus credenciales:
```
cp .env.example .env  # Linux/macOS
# o copia manual en Windows
```

## Ejecutar
```bash
python app.py
# Abre http://localhost:5000
```

## Estructura
- `app.py`: aplicación Flask
- `templates/`: HTML (Jinja)
- `static/style.css`: estilos
- `db.sql`: esquema MySQL
- `.env.example`: variables de entorno
- `requirements.txt`: dependencias

## Seguridad y privacidad
Este proyecto guarda nombre, email y mensaje en la tabla `guestbook`. Asegúrate de:
- Configurar `FLASK_SECRET_KEY` con un valor seguro.
- Proteger el acceso a la base de datos.
- Añadir un aviso de privacidad si lo publicas.

## Personalización rápida
- Cambia textos/porcentajes de barras en `templates/index.html`.
- Ajusta colores/estilos en `static/style.css`.
- Agrega más secciones repitiendo el patrón `.card`.
