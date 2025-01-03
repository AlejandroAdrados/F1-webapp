import io
import pytest
from app import create_app
from unittest.mock import patch
import plotly.graph_objects as go


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as flask_client:
        with app.app_context():
            yield flask_client


def test_get_results_success(client):
    with patch('app.modules.database.total_ranking',
               return_value=[{'driver': 'Driver1', 'points': 100}]), \
            patch('app.modules.database.get_races', return_value=1):
        response = client.get('/api/results?year=2021&race=1')

    assert response.status_code == 200
    assert response.json == [{'driver': 'Driver1', 'points': 100}]


def test_get_results_no_data(client):
    with patch('app.modules.database.get_races', return_value=5), \
            patch('app.modules.database.total_ranking', return_value=None):
        response = client.get('/api/results?year=2021&race=1')

    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada y carrera seleccionadas'}


def test_get_results_invalid_race(client):
    with patch('app.modules.database.get_races', return_value=5):
        response = client.get('/api/results?year=2021&race=6')

    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada y carrera seleccionadas'}


def test_update_results_from_internet_success(client):
    with patch('app.modules.web_data.load_season', return_value=True):
        response = client.post('/api/results/internet', json={'year': 2021})
    assert response.status_code == 200
    assert response.json == {
        'message': 'Data updated successfully from the web'}


def test_update_results_from_internet_failure(client):
    with patch('app.modules.web_data.load_season', return_value=False):
        response = client.post('/api/results/internet', json={'year': 2021})
    assert response.status_code == 500
    assert response.json == {
        'error': 'Error al actualizar los datos de la temporada seleccionada'}


def test_update_results_from_file_success(client):
    with patch('app.modules.local_data.verify_db', return_value=True), \
            patch('app.modules.local_data.get_seasons', return_value={'seasons': [2021]}), \
            patch('app.modules.local_data.update_db', return_value=True):
        data = {'file': (io.BytesIO(b"fake content"), 'test.db')}
        response = client.post('/api/results/file',
                               data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.json == {'seasons': [2021]}


def test_update_results_from_file_no_file(client):
    response = client.post('/api/results/file')
    assert response.status_code == 400
    assert response.data.decode() == 'No se ha enviado ningún archivo'


def test_update_results_from_file_invalid_extension(client):
    data = {'file': (io.BytesIO(b"fake content"), 'test.txt')}
    response = client.post('/api/results/file', data=data,
                           content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.data.decode() == 'El archivo debe tener la extensión .db'


def test_get_years(client):
    with patch('app.modules.database.get_info', return_value=[{'year': 2021}]):
        response = client.get('/api/years')
    assert response.status_code == 200
    assert response.json == [{'year': 2021}]


def test_get_races_success(client):
    with patch('app.modules.database.get_info', return_value=[{'year': 2021, 'races': [1, 2, 3]}]):
        response = client.get('/api/races?year=2021')
    assert response.status_code == 200
    assert response.json == {'year': 2021, 'races': [1, 2, 3]}


def test_get_races_invalid_year(client):
    with patch('app.modules.database.get_info', return_value=[]):
        response = client.get('/api/races?year=2021')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada seleccionada'}


def test_get_competitor_score_success(client):
    with patch('app.modules.database.competitor_score_in_ranking', return_value=100), \
            patch('app.modules.database.competitor_team_in_year', return_value='Team1'), \
            patch('app.modules.database.competitor_position_in_ranking', return_value=1):
        response = client.get(
            '/api/competitor/info?year=2021&race=1&driver=Driver1')
    assert response.status_code == 200
    assert response.json == {'score': 100, 'team': 'Team1', 'position': 1}


def test_get_competitor_score_no_data(client):
    with patch('app.modules.database.competitor_team_in_year', return_value=None):
        response = client.get(
            '/api/competitor/info?year=2021&race=1&driver=Driver1')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos del piloto seleccionado'}


def test_get_competitor_history_success(client):
    with patch('app.modules.database.competitor_position_history', return_value=[1, 2, 3]):
        response = client.get(
            '/api/competitor/history?year=2021&race=1&driver=Driver1')
    assert response.status_code == 200
    assert response.json == [1, 2, 3]


def test_get_competitor_history_no_data(client):
    with patch('app.modules.database.competitor_position_history', return_value=None):
        response = client.get(
            '/api/competitor/history?year=2021&race=1&driver=Driver1')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos del piloto seleccionado'}


def test_get_num_competitors_success(client):
    with patch('app.modules.database.num_competitors', return_value=10):
        response = client.get('/api/competitors/num?year=2021')
    assert response.status_code == 200
    assert response.json == 10


def test_get_num_competitors_no_data(client):
    with patch('app.modules.database.num_competitors', return_value=0):
        response = client.get('/api/competitors/num?year=2021')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada seleccionada'}


def test_get_competitors_success(client):
    with patch('app.modules.database.competitors_list', return_value=[{'driver': 'Driver1'}]):
        response = client.get('/api/competitors/list?year=2021')
    assert response.status_code == 200
    assert response.json == [{'driver': 'Driver1'}]


def test_get_competitors_no_data(client):
    with patch('app.modules.database.competitors_list', return_value=None):
        response = client.get('/api/competitors/list?year=2021')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada seleccionada'}


def test_get_graph_success(client):
    mock_figure = go.Figure()
    with patch('app.modules.graphs.graph_until_ranking', return_value=(None, None)), \
            patch('app.modules.graphs.weighted_graph', return_value=(None, None)), \
            patch('app.modules.graphs.convert_networkx_to_plotly', return_value=mock_figure):
        response = client.get('/api/graph?year=2021&race=1&bonus=true')
    assert response.status_code == 200
    assert response.json == None


def test_get_graph_no_data(client):
    with patch('app.modules.graphs.graph_until_ranking', side_effect=Exception):
        response = client.get('/api/graph?year=2021&race=1&bonus=true')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada y carrera seleccionadas'}


def test_get_ranking_metrics_success(client):
    with patch('app.modules.graphs.graph_until_ranking', return_value=(None, None)), \
            patch('app.modules.graphs.weighted_graph', return_value=(None, None)), \
            patch('app.modules.metrics.weighted_graph_metrics', return_value={'metric': 1}):
        response = client.get(
            '/api/metrics/ranking?year=2021&race=1&bonus=true')
    assert response.status_code == 200
    assert response.json == {'metric': 1}


def test_get_ranking_metrics_no_data(client):
    with patch('app.modules.graphs.graph_until_ranking', side_effect=Exception):
        response = client.get(
            '/api/metrics/ranking?year=2021&race=1&bonus=true')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada y carrera seleccionadas'}


def test_get_season_metrics_success(client):
    with patch('app.modules.metrics.season_metrics', return_value={'metric': 1}):
        response = client.get(
            '/api/metrics/season?year=2021&race=1&bonus=true')
    assert response.status_code == 200
    assert response.json == {'metric': 1}


def test_get_season_metrics_no_data(client):
    with patch('app.modules.metrics.season_metrics', side_effect=Exception):
        response = client.get(
            '/api/metrics/season?year=2021&race=1&bonus=true')
    assert response.status_code == 400
    assert response.json == {
        'error': 'No se encontraron datos para la temporada y carrera seleccionadas'}
