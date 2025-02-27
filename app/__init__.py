"""
Initialize the Flask application.
"""
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """
    Create and configure the Flask application.

    This function sets up the Flask application, configures the database URI,
    initializes the database, registers blueprints for application routes and
    API routes, and defines a custom error handler for 404 errors.

    Returns:
        Flask: The configured Flask application instance.
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    rootdir = os.path.abspath(os.path.join(basedir, os.pardir))

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(rootdir, 'data', 'f1_results.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.api_routes import api as api_routes
    from app.app_routes import app as app_routes
    app.register_blueprint(app_routes)
    app.register_blueprint(api_routes)

    @app.errorhandler(404)
    def page_not_found(error):
        custom_error = {"code": error.code, "description": "Not Found",
                        "message": """La URL solicitada no se encontró en el servidor.
                        Si ingresaste la URL manualmente, por favor verifica la ortografía e intenta nuevamente."""}
        return render_template('error.html', error=custom_error), 404

    with app.app_context():
        db.create_all()
    return app
