```markdown
# Hayuelos

Aplicación web para la gestión de mediciones y operación de estación de servicios (Hayuelos). Aplicación server-rendered con Flask, SQLAlchemy y Bootstrap.

Estado
- Backend: Flask con blueprints.
- Frontend: Templates Jinja2 + Bootstrap.
- DB: SQLAlchemy (Postgres / MySQL), migraciones con Flask-Migrate (recomendado).
- Despliegue: Preparado para Render; ajustes para DATABASE_URL incluidos.

Características principales
- Autenticación con Flask-Login
- Roles (admin, encargado, islero)
- Registro de mediciones y descargues
- Carga masiva (CSV / Excel)
- Auditoría de cambios
- Uploads de archivos y validaciones con WTForms

Requisitos
- Python 3.10+ (pyproject / requirements indican compatibilidad)
- PostgreSQL o MySQL (según DATABASE_URL)
- pip / Poetry / pipx

Instalación (local)
1. Clona el repositorio:
   git clone https://github.com/camilo68/Hayuelos.git
   cd Hayuelos

2. Crea y activa un virtualenv:
   python -m venv .venv
   source .venv/bin/activate    # Linux / macOS
   .venv\Scripts\activate       # Windows (PowerShell use: .\.venv\Scripts\Activate.ps1)

3. Instala dependencias:
   pip install -r requirements.txt

4. Copia variables de entorno:
   cp .env.example .env
   # Edita .env con valores reales (DATABASE_URL, SESSION_SECRET, MAIL_*, etc.)

5. Inicializa la base de datos:
   # Recomendada: usar migraciones (flask db init / migrate / upgrade)
   flask db upgrade
   # Si no usas migraciones, puedes usar:
   python seed_db.py

6. Correr la app:
   export FLASK_APP=main.py
   export FLASK_ENV=development
   flask run

Variables de entorno (principales en .env.example)
- SESSION_SECRET: secreto de la app (SECRET_KEY)
- DATABASE_URL: URL de la base de datos (Postgres/ MySQL). Para Render: reemplaza postgres:// por postgresql:// (app_factory.py lo hace).
- MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER
- ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL (opcional para create_admin)

Despliegue en Render (resumen)
- Crea un servicio web en Render apuntando al repo.
- Asegúrate de definir las environment variables en el dashboard (DATABASE_URL, SESSION_SECRET, MAIL_*).
- Comando de build: pip install -r requirements.txt
- Start command: gunicorn main:app --bind 0.0.0.0:$PORT

Buenas prácticas recomendadas (acciones prioritarias)
1. Añadir README.md y .env.example (hecho aquí).
2. Configurar CI (GitHub Actions) para lint + tests.
3. Extraer lógica a services/ y repositories/ para testabilidad.
4. Añadir tests unitarios y de integración.
5. No usar db.create_all() en producción; usar migraciones versionadas (flask-migrate).
6. Añadir logging estructurado y rotación de logs.
7. Añadir documentación de la API (OpenAPI / Postman) si debes exponer endpoints.

Cómo contribuir
- Fork + branch feature/<nombre>
- Tests para cambios funcionales
- PR con descripción y screenshots si aplica

Contacto
- Owner: camilo68
```
