from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy() 

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    rootdir = os.path.abspath(os.path.join(basedir, os.pardir))

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(rootdir, 'data', 'f1_results.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.app_routes import app as app_routes
    from app.api_routes import api as api_routes
    app.register_blueprint(app_routes)
    app.register_blueprint(api_routes)

    with app.app_context():
        db.create_all()
    return app