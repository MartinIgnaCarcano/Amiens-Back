import os
from dotenv import load_dotenv

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

jwt = JWTManager()

# Inicializar SQLAlchemy sin asociar aún con la app
db = SQLAlchemy()

# Cargar variables de entorno desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurar base de datos (usa la URL real de Supabase en tu .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        # Configurar base de datos (usa la URL real de Supabase en tu .env)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres.uvqhfytlzlxwnjhxulfg:rinkashichikito@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)  # expira en 10 segundos
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    @jwt.expired_token_loader
    def token_expirado(jwt_header, jwt_payload):
        return jsonify({
            "error": "El token ha expirado",
            "mensaje": "Por favor, iniciá sesión nuevamente"
        }), 401

    with app.app_context():
        from app import models
        from .routes import productos_bp, auth_bp
        app.register_blueprint(productos_bp)
        app.register_blueprint(auth_bp)
        
        
    return app
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text

# # Crear la instancia de la base de datos
# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)

#     # Configuración de la base de datos (sin .env)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres.uvqhfytlzlxwnjhxulfg:rinkashichikito@aws-0-sa-east-1.pooler.supabase.com:6543/postgres'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     # Inicializar la base de datos con la app
#     db.init_app(app)

#     # Ruta para verificar que la conexión funciona
#     @app.route('/ping_db')
#     def ping_db():
#         try:
#             # Ejecutar un SELECT 1 usando text()
#             result = db.session.execute(text('SELECT 1')).scalar()
#             return f"Conexión exitosa. Resultado: {result}"
#         except Exception as e:
#             return f"Error al conectar a la base de datos: {e}"

#     return app
