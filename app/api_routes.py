from flask import Blueprint, jsonify, request
from app.modules import web_data as wd
from app.modules import database as db
from app.modules import graphs as gr
from app.modules import metrics as mt

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/results', methods=['GET'])
def get_results():
    year = request.args.get('year')
    race = request.args.get('race')
    if race and year:
        results = db.total_ranking(year, race)
        return jsonify(results)
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

@api.route('bgraph', methods=['GET'])
def get_bonus_graph():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    graph, swaps_list = gr.graph_until_ranking(year, race)
    bonuses = {1: 4, 2: 3, 3: 2}
    weighted_graph, labels = gr.weighted_graph(graph, swaps_list, bonuses)
    fig = gr.convert_networkx_to_plotly(weighted_graph, labels)
    graph_json = fig.to_json()
    return graph_json

@api.route('metrics/ranking', methods=['GET'])
def get_ranking_metrics():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    graph, swaps_list = gr.graph_until_ranking(year, race)
    weighted_graph = gr.weighted_graph(graph, swaps_list)[0]
    result = mt.weighted_graph_metrics(weighted_graph, race)
    return jsonify(result)

@api.route('metrics/branking', methods=['GET'])
def get_ranking_bonus_metrics():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    graph, swaps_list = gr.graph_until_ranking(year, race)
    bonuses = {1: 4, 2: 3, 3: 2}
    weighted_graph = gr.weighted_graph(graph, swaps_list, bonuses)[0]
    result = mt.weighted_graph_metrics(weighted_graph, race)
    return jsonify(result)

@api.route('metrics/season', methods=['GET'])
def get_season_metrics():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    result = mt.season_metrics(year, race, False)
    return jsonify(result)

@api.route('metrics/bseason', methods=['GET'])
def get_season_bonus_metrics():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    result = mt.season_metrics(year, race, True)
    return jsonify(result)
