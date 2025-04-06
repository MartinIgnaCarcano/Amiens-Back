from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa el módulo
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS para la app
    # Configuración de la base de datos
    
    db_path = os.path.join('/tmp', 'inventario.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Importar rutas después de crear la app para evitar circular imports
    from .routes import productos_bp
    app.register_blueprint(productos_bp)
    
    with app.app_context():
        db.create_all()
    
    return app