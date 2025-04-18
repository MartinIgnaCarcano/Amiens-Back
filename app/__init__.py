from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Usar la carpeta persistente que Render te asigna
    db_dir = os.environ.get("RENDER_PERSISTENT_FS_PATH", "./instance")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "inventario.db")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import productos_bp
    app.register_blueprint(productos_bp)

    with app.app_context():
        db.create_all()

    return app
