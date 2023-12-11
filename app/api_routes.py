from flask import Blueprint, jsonify, request
from app.modules import web_data as wd
from app.modules import database as db
from app.modules import graphs as gr

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/results', methods=['GET'])
def get_results():
    year = request.args.get('year')
    race = request.args.get('race')
    
    # Verifica si los parámetros fueron proporcionados en la solicitud
    if race and year:
        results = db.total_ranking(year, race)
        return jsonify(results)
    
    # En caso de que los parámetros no estén presentes, devuelve un error o una respuesta indicando que faltan parámetros
    return jsonify({'error': 'Se requieren los parámetros año y jornada'}), 400

@api.route('/results', methods=['POST'])
def update_results():
    data = request.get_json()
    year_start = data.get('year_start')
    year_end = data.get('year_end')
    wd.load_data(year_start, year_end)
    return jsonify({'message': 'Data updated successfully from the web'})

@api.route('/years', methods=['GET'])
def get_years():
    results = db.get_info()
    return jsonify(results)

@api.route('/races', methods=['GET'])
def get_races():
    year = request.args.get('year')
    data = db.get_info()
    for item in data:
        if item['year'] == int(year):
            return jsonify(item)
        
@api.route('/competitor/score', methods=['GET'])
def get_competitor_score():
    year = request.args.get('year')
    race = request.args.get('race')
    driver = request.args.get('driver')
    result = db.competitor_score_in_ranking(driver, year, race)
    return jsonify(result)

@api.route('/competitor/position', methods=['GET'])
def get_competitor_position():
    year = request.args.get('year')
    race = request.args.get('race')
    driver = request.args.get('driver')
    result = db.competitor_position_in_ranking(driver, year, race)
    return jsonify(result)

@api.route('/competitor/history', methods=['GET'])
def get_competitor_history():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    driver = request.args.get('driver')
    result = db.competitor_position_history(driver, year, race)
    return jsonify(result)

@api.route('/competitors/num', methods=['GET'])
def get_num_competitors():
    year = request.args.get('year')
    result = db.num_competitors(year)
    return jsonify(result)

@api.route('/competitors/list', methods=['GET'])
def get_competitors():
    year = request.args.get('year')
    result = db.competitors_list(year)
    return jsonify(result)

@api.route('graph', methods=['GET'])
def get_graph():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    graph, swaps_list = gr.graph_until_ranking(year, race)
    weighted_graph, labels = gr.weighted_graph(graph, swaps_list)
    fig = gr.convert_networkx_to_plotly(weighted_graph, labels)
    graph_json = fig.to_json()
    return graph_json