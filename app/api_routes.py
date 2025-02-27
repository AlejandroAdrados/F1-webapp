"""
Class that defines the routes for the API.
"""

import json
import os

from flask import Blueprint, jsonify, make_response, request

from app.modules import database as db
from app.modules import graphs as gr
from app.modules import local_data as ld
from app.modules import metrics as mt
from app.modules import web_data as wd

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/results', methods=['GET'])
def get_results():
    """
    Fetches the race results for a given year and race number.

    Retrieves the year and race number from the request arguments, checks if the race number is valid for the given year
    and returns the race results in JSON format if available.

    Returns:
        Response: JSON response containing the race results if found, otherwise an error response with status code 400.

    Raises:
        ValueError: If the race number exceeds the maximum number of races for the given year.
    """
    year = request.args.get('year')
    race = request.args.get('race')
    max_races = int(db.get_races(year))
    if year and int(race) <= max_races:
        results = db.total_ranking(year, race)
        if results:
            return jsonify(results)
    return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


@api.route('/results/internet', methods=['POST'])
def update_results_from_internet():
    """
    Updates the results of a specific season from the internet.

    This function retrieves the year from the JSON payload of the request,
    attempts to load the season data for that year from the web, and returns
    a JSON response indicating whether the update was successful or not.

    Returns:
        Response: A JSON response with a message indicating the result of the update.
                 - If successful: {'message': 'Data updated successfully from the web'}
                 - If failed: A 500 error with the message 'Error al actualizar los datos de la temporada seleccionada'
    """
    year = request.get_json().get('year')
    if wd.load_season(year):
        return jsonify({'message': 'Data updated successfully from the web'})
    return throw_error(500, 'Error al actualizar los datos de la temporada seleccionada')


@api.route('/results/file', methods=['POST'])
def update_results_from_file():
    """
    Updates the results from an uploaded file.

    This function handles the upload of a file, verifies its extension,
    saves it to a temporary location, and updates the database if the
    file is valid.

    Returns:
        tuple: A message and an HTTP status code if there is an error.
        Response: A JSON response containing the seasons if the update is successful.
    """
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
        except Exception:
            return throw_error(500, 'Error al actualizar los datos de la temporada seleccionada')
    return throw_error(403, 'El archivo no contiene la estructura de datos esperada')


@api.route('/years', methods=['GET'])
def get_years():
    """
    Get the years saved in the database.

    Returns:
        Response: A Flask JSON response containing the results from the database.
    """
    results = db.get_info()
    return jsonify(results)


@api.route('/races', methods=['GET'])
def get_races():
    """
    Get the number of races for a given year.

    Returns:
        Response: A JSON response containing race information for the specified year,
                  or an error response if no data is found.

    Raises:
        HTTPException: If the 'year' parameter is not provided or if no data is found
                       for the specified year.
    """
    year = request.args.get('year')
    data = db.get_info()
    for item in data:
        if item['year'] == int(year):
            return jsonify(item)
    return throw_error(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('/competitor/info', methods=['GET'])
def get_competitor_score():
    """
    Retrieves the score, team, and position of a specified driver in a given race and year.

    Query Parameters:
    - year (str): The year of the race.
    - race (str): The name or identifier of the race.
    - driver (str): The name or identifier of the driver.

    Returns:
    - JSON response containing:
        - score (int): The score of the driver in the specified race and year.
        - team (str): The team of the driver in the specified year.
        - position (int): The position of the driver in the specified race and year.
    - If the team is not found, returns a 400 error with a message indicating no data was found for the selected driver.
    """
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
    return throw_error(400, 'No se encontraron datos del piloto seleccionado')


@api.route('/competitor/history', methods=['GET'])
def get_competitor_history():
    """
    Retrieves the position history for a specified competitor until a given race in a year.

    Query Parameters:
        year (str): The year of the race.
        race (int): The race number.
        driver (str): The driver's identifier.

    Returns:
        Response: A JSON response containing the competitor's position history if found,
                  otherwise a JSON error message with a 400 status code.

    Raises:
        HTTPException: If no data is found for the specified driver, year, and race.
    """
    year = request.args.get('year')
    race = int(request.args.get('race'))
    driver = request.args.get('driver')
    result = db.competitor_position_history(driver, year, race)
    if result:
        return jsonify(result)
    return throw_error(400, 'No se encontraron datos del piloto seleccionado')


@api.route('/competitors/num', methods=['GET'])
def get_num_competitors():
    """
    Retrieves the number of competitors for a given year from the database.

    Returns:
        Response: A JSON response containing the number of competitors if
        data is found, or an error response with a 400 status code if no data
        is found.

    Raises:
        HTTPException: If no data is found for the given year, an HTTP 400
        error is raised with a message indicating that no data was found for
        the selected season.
    """
    year = request.args.get('year')
    result = db.num_competitors(year)
    if result > 0:
        return jsonify(result)
    return throw_error(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('/competitors/list', methods=['GET'])
def get_competitors():
    """
    Fetches the list of competitors for a given year from the database.

    Returns:
        Response: A JSON response containing the list of competitors if found,
                  otherwise an error response with status code 400 and an error message.
    """
    year = request.args.get('year')
    result = db.competitors_list(year)
    if result:
        return jsonify(result)
    return throw_error(400, 'No se encontraron datos para la temporada seleccionada')


@api.route('graph', methods=['GET'])
def get_graph():
    """
    Retrieves and processes the competitive graph based on the provided year, race, and bonus parameters.

    Query Parameters:
    - year (str): The year of the race season.
    - race (int): The race number within the season.
    - bonus (str): A flag indicating whether to apply bonuses ('true' or 'false').

    Returns:
    - str: A JSON representation of the processed graph.

    Raises:
    - HTTPException: If the provided parameters are invalid or if an error occurs during processing.
    """
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
            return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        fig = gr.convert_networkx_to_plotly(weighted_graph, labels)
        graph_json = fig.to_json()
        return graph_json
    except Exception as error:
        print(error)
        return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


@api.route('metrics/ranking', methods=['GET'])
def get_ranking_metrics():
    """
    Retrieves ranking metrics for a specified year and race, with an optional bonus weighting.

    Returns:
        Response: A JSON response containing the ranking metrics or an error message.

    Raises:
        Exception: If any error occurs during the process, a 400 error response is returned with
                   a message indicating that no data was found for the selected season and race.
    """
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
            return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        result = mt.weighted_graph_metrics(weighted_graph, race)
        return jsonify(result)
    except Exception as error:
        print(error)
        return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


@api.route('metrics/season', methods=['GET'])
def get_season_metrics():
    """
    Retrieves metrics based on the provided year and bonus flag until a race number.

    Query Parameters:
    - year (str): The year of the season.
    - race (int): The race number within the season.
    - bonus (str): A flag indicating whether to include bonus metrics ('true' or 'false').

    Returns:
    - JSON response containing the season metrics if successful.
    - Error response with status code 400 if any error occurs or if the input parameters are invalid.

    Raises:
    - Exception: If an error occurs during the processing of the request.
    """
    try:
        year = request.args.get('year')
        race = int(request.args.get('race'))
        bonus = request.args.get('bonus')
        if bonus == 'true':
            result = mt.season_metrics(year, race, True)
        elif bonus == 'false':
            result = mt.season_metrics(year, race, False)
        else:
            return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')
        return jsonify(result)
    except Exception as error:
        print(error)
        return throw_error(400, 'No se encontraron datos para la temporada y carrera seleccionadas')


def throw_error(code, message):
    """
    Generates an HTTP error response with a specified status code and message.

    Args:
        code (int): The HTTP status code for the error response.
        message (str): The error message to include in the response.

    Returns:
        Response: A Flask response object containing the error message and status code,
                  with an error cookie set.
    """
    response = make_response(jsonify({'error': message}), code)
    error = {'code': code, 'description': "", 'message': message}
    response.set_cookie('error', json.dumps(error))
    return response
