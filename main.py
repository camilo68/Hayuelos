# main.py - CORREGIDO
from app_factory import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# from flask import Flask, jsonify
# from flask_cors import CORS
# import mysql.connector

# app = Flask(__name__)
# CORS(app)

# def conectar_bd():
#     return mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='sitex_prueba'
#     )

# @app.route('/api/tanques', methods=['GET'])
# def obtener_tanques():
#     conexion = conectar_bd()
#     cursor = conexion.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM tanques")
#     resultados = cursor.fetchall()
#     cursor.close()
#     conexion.close()
#     return jsonify(resultados)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

with app.app_context():
    from extensions import db
    from models import Tanque, Empleado
    import bcrypt

    db.create_all()  # Crea tablas si no existen

    # Crea tanques si no hay
    if db.session.query(Tanque).count() == 0:
        tanques = [
            Tanque(tipo_combustible='Diesel', capacidad=6000, activo=True),
            Tanque(tipo_combustible='Diesel', capacidad=12000, activo=True),
            Tanque(tipo_combustible='ACPM', capacidad=12000, activo=True),
            Tanque(tipo_combustible='Extra', capacidad=6000, activo=True)
        ]
        db.session.add_all(tanques)
        db.session.commit()

    # Crea admin si no existe
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