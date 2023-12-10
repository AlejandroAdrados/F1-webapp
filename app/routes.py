from flask import Blueprint, jsonify, render_template, request
from app import web_data as wd
from app import helpers as hp

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/clasificacion')
def index():
    return render_template('index.html')

@app_routes.route('/competitor')
def competitor_dashboard():
    return render_template('competitor_dashboard.html')

@app_routes.route('/api/results', methods=['GET'])
def get_results():
    year = request.args.get('year')
    race = request.args.get('race')
    
    # Verifica si los parámetros fueron proporcionados en la solicitud
    if race and year:
        results = hp.total_ranking(year, race)
        return jsonify(results)
    
    # En caso de que los parámetros no estén presentes, devuelve un error o una respuesta indicando que faltan parámetros
    return jsonify({'error': 'Se requieren los parámetros año y jornada'}), 400

@app_routes.route('/api/results', methods=['POST'])
def update_results():
    data = request.get_json()
    year_start = data.get('year_start')
    year_end = data.get('year_end')
    wd.load_data(year_start, year_end)
    return jsonify({'message': 'Data updated successfully from the web'})

@app_routes.route('/api/years', methods=['GET'])
def get_years():
    results = hp.get_info()
    return jsonify(results)

@app_routes.route('/api/races', methods=['GET'])
def get_races():
    year = request.args.get('year')
    data = hp.get_info()
    for item in data:
        if item['year'] == int(year):
            return jsonify(item)
        
@app_routes.route('/api/competitor/score', methods=['GET'])
def get_competitor_score():
    year = request.args.get('year')
    race = request.args.get('race')
    driver = request.args.get('driver')
    result = hp.competitor_score_in_ranking(driver, year, race)
    return jsonify(result)

@app_routes.route('/api/competitor/position', methods=['GET'])
def get_competitor_position():
    year = request.args.get('year')
    race = request.args.get('race')
    driver = request.args.get('driver')
    result = hp.competitor_position_in_ranking(driver, year, race)
    return jsonify(result)

@app_routes.route('/api/competitor/history', methods=['GET'])
def get_competitor_history():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    driver = request.args.get('driver')
    result = hp.competitor_position_history(driver, year, race)
    return jsonify(result)

@app_routes.route('/api/competitors/num', methods=['GET'])
def get_num_copetitors():
    year = request.args.get('year')
    result = hp.num_competitors(year)
    return jsonify(result)

@app_routes.route('/api/competitors/list', methods=['GET'])
def get_copmetitors():
    year = request.args.get('year')
    result = hp.competitors_list(year)
    return jsonify(result)
