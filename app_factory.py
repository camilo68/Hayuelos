# app_factory.py - CORREGIDO PARA RENDER FREE (init en startup)
import os
from flask import Flask
from extensions import db, login_manager, migrate, csrf, mail
from dotenv import load_dotenv
import bcrypt  # <-- Agrega esto arriba

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'fallback-secret-key-change-in-production')
    
    # Base de datos - Fix para Render Postgres
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'mysql+pymysql://root:@localhost/sitex_prueba'
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Correo
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@hayuelos.com')
    
    # Uploads
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Empleado
        empleado = db.session.get(Empleado, int(user_id))
        if empleado and not empleado.activo:
            return None
        return empleado
    
    # Blueprints
    from routes import auth_bp, main_bp, dashboard_bp, medicion_bp, admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicion_bp)
    app.register_blueprint(admin_bp)
    
    # === INICIALIZACIÓN AUTOMÁTICA (TABLAS + TANQUES + ADMIN) ===
    with app.app_context():
        from models import Tanque, Empleado
        
        db.create_all()  # Crea tablas
        
        # Tanques
        if db.session.query(Tanque).count() == 0:
            tanques = [
                Tanque(tipo_combustible='Diesel', capacidad=6000, activo=True),
                Tanque(tipo_combustible='Diesel', capacidad=12000, activo=True),
                Tanque(tipo_combustible='ACPM', capacidad=12000, activo=True),
                Tanque(tipo_combustible='Extra', capacidad=6000, activo=True)
            ]
            db.session.add_all(tanques)
            db.session.commit()
            print("✓ Tanques creados")
        
        # Admin
        if not Empleado.query.filter_by(usuario='admin').first():
            hashed = bcrypt.hashpw('Hayuelos2025!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = Empleado(
                nombre_empleado='Admin', apellido_empleado='Hayuelos',
                numero_documento='0000', tipo_documento='CC',
                email='admin@hayuelos.com', cargo_establecido='admin',
                usuario='admin', contrasena=hashed,
                activo=True, aceptado_terminos=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin creado: admin / Hayuelos2025!")
    
    # Headers de seguridad
    @app.after_request
    def set_secure_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return app