from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

# Obtener la ruta base de la aplicación
basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.join(basedir, os.pardir))

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8050"}})  # Ajusta el origen a la ubicación de tu app Dash

# Configurar la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(rootdir, 'data', 'f1_results.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)

from app.routes import app_routes
# Registrar las rutas de la aplicación Flask y la API
app.register_blueprint(app_routes)

from app import models
with app.app_context():
    db.create_all()