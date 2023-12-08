# En el archivo app/routes.py
from flask import Blueprint, jsonify
from app import web_data as wd
from .helpers import total_ranking
from frontend import app_dash as dash_app

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/flask')
def index():
    return '¡Hola! Esta es tu aplicación Flask.'

@app_routes.route('/api/results', methods=['GET'])
def get_results():
    results = total_ranking(2022, 17)
    return jsonify(results)

@app_routes.route('/api/results', methods=['POST'])
def update_results():
    wd.load_data()
    return jsonify({'message': 'Data updated successfully from the web'})
