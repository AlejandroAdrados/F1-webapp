from flask import Blueprint, jsonify, render_template, request
from app import web_data as wd
from app import helpers as hp
from frontend import app_dash as dash_app

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/clasificacion')
def index():
    return render_template('index.html')

@app_routes.route('/api/results', methods=['GET'])
def get_results():
    jornada = request.args.get('jornada')
    anio = request.args.get('anio')
    
    # Verifica si los parámetros fueron proporcionados en la solicitud
    if jornada and anio:
        results = hp.total_ranking(anio, jornada)
        return jsonify(results)
    
    # En caso de que los parámetros no estén presentes, devuelve un error o una respuesta indicando que faltan parámetros
    return jsonify({'error': 'Se requieren los parámetros "jornada" y "anio"'}), 400

@app_routes.route('/api/results', methods=['POST'])
def update_results():
    wd.load_data()
    return jsonify({'message': 'Data updated successfully from the web'})

@app_routes.route('/api/info', methods=['GET'])
def get_info():
    results = hp.get_info()
    return jsonify(results)
