from flask import Blueprint, jsonify, request, make_response
import json
import os
from f1_webapp.application.utils import web_data as wd
from f1_webapp.infra.database import local_data as ld
from f1_webapp.infra.database import database as db
from f1_webapp.modules import graphs as gr
from f1_webapp.modules import metrics as mt

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/results', methods=['GET'])
def get_results():
    year = request.args.get('year')
    race = request.args.get('race')
    max_races = int(db.get_races(year))
    if year and int(race) <= max_races:
        results = db.total_ranking(year, race)
        if results:
            return jsonify(results)
    return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


@api.route('/results/internet', methods=['POST'])
def update_results_from_internet():
    year = request.get_json().get('year')
    if wd.load_season(year):
        return jsonify({'message': 'Data updated successfully from the web'})
    else:
        return throwError(500, 'Error al actualizar los datos de la temporada seleccionada')
    
@api.route('/results/file', methods=['POST'])
def update_results_from_file():
    if 'file' not in request.files:
        return 'No se ha enviado ningún archivo', 400
    file = request.files['file']
    if file.filename == '':
        return 'No se ha seleccionado ningún archivo', 400
    if not file.filename.lower().endswith('.db'):
        return 'El archivo debe tener la extensión .db', 400
    
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)

    if ld.verify_db(file_path):
        try:
            seasons = ld.get_seasons(file_path)
            ld.update_db(file_path)
            return jsonify(seasons)
        except Exception as error:
            return throwError(500, 'Error al actualizar los datos de la temporada seleccionada')
    return throwError(403, 'El archivo no contiene la estructura de datos esperada')


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
    return throwError(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('/competitor/info', methods=['GET'])
def get_competitor_score():
    year = request.args.get('year')
    race = request.args.get('race')
    driver = request.args.get('driver')
    score = db.competitor_score_in_ranking(driver, year, race)
    team = db.competitor_team_in_year(driver, year)
    position = db.competitor_position_in_ranking(driver, year, race)
    if team:
        result = {
            'score': score,
            'team': team,
            'position': position
        }
        return jsonify(result)
    else:
        return throwError(400, 'No se encontraron datos del piloto seleccionado')


@api.route('/competitor/history', methods=['GET'])
def get_competitor_history():
    year = request.args.get('year')
    race = int(request.args.get('race'))
    driver = request.args.get('driver')
    result = db.competitor_position_history(driver, year, race)
    if result:
        return jsonify(result)
    else:
        return throwError(400, 'No se encontraron datos del piloto seleccionado')


@api.route('/competitors/num', methods=['GET'])
def get_num_competitors():
    year = request.args.get('year')
    result = db.num_competitors(year)
    if result > 0:
        return jsonify(result)
    else:
        return throwError(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('/competitors/list', methods=['GET'])
def get_competitors():
    year = request.args.get('year')
    result = db.competitors_list(year)
    if result:
        return jsonify(result)
    else:
        return throwError(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('graph', methods=['GET'])
def get_graph():
    try:
        year = request.args.get('year')
        race = int(request.args.get('race'))
        bonus = request.args.get('bonus')
        graph, swaps_list = gr.graph_until_ranking(year, race)
        if bonus == 'true':
            bonuses = {1: 4, 2: 3, 3: 2}
            weighted_graph, labels = gr.weighted_graph(
                graph, swaps_list, bonuses)
        elif bonus == 'false':
            weighted_graph, labels = gr.weighted_graph(graph, swaps_list)
        else:
            return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        fig = gr.convert_networkx_to_plotly(weighted_graph, labels)
        graph_json = fig.to_json()
        return graph_json
    except Exception as error:
        print(error)
        return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
    

@api.route('metrics/ranking', methods=['GET'])
def get_ranking_metrics():
    try:
        year = request.args.get('year')
        race = int(request.args.get('race'))
        bonus = request.args.get('bonus')
        graph, swaps_list = gr.graph_until_ranking(year, race)
        if bonus == 'true':
            bonuses = {1: 4, 2: 3, 3: 2}
            weighted_graph = gr.weighted_graph(graph, swaps_list, bonuses)[0]
        elif bonus == 'false':
            weighted_graph = gr.weighted_graph(graph, swaps_list)[0]
        else:
            return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        result = mt.weighted_graph_metrics(weighted_graph, race)
        return jsonify(result)
    except Exception as error:
        print(error)
        return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


@api.route('metrics/season', methods=['GET'])
def get_season_metrics():
    try:
        year = request.args.get('year')
        race = int(request.args.get('race'))
        bonus = request.args.get('bonus')
        if bonus == 'true':
            result = mt.season_metrics(year, race, True)
        elif bonus == 'false':
            result = mt.season_metrics(year, race, False)
        else:
            return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        return jsonify(result)
    except Exception as error:
        print(error)
        return throwError(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


def throwError(code, message):
    response = make_response(jsonify({'error': message}), code)
    error = {'code': code, 'description': "", 'message': message}
    response.set_cookie('error', json.dumps(error))
    return response
