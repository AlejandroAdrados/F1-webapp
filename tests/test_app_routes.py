import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as flask_client:
        with app.app_context():
            yield flask_client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    # Check for the unique content in the template
    assert b'<h1 class="display-4">Bienvenido a la WebApp de la F\xc3\xb3rmula 1</h1>' in response.data


def test_competitor_dashboard(client):
    response = client.get('/competitor')
    assert response.status_code == 200
    assert b'<h1 id="pageTitle">Informe del piloto</h1>' in response.data

def test_clasification(client):
    response = client.get('/clasification')
    assert response.status_code == 200
    assert b'<h1 id="pageTitle">Clasificaci\xc3\xb3n</h1>' in response.data

def test_graph(client):
    response = client.get('/graph')
    assert response.status_code == 200
    assert b'<h1 id="pageTitle">Grafos de competitividad &nbsp;</h1>' in response.data

def test_metrics(client):
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'<h1 id="pageTitle">Resumen de m\xc3\xa9tricas</h1>' in response.data

def test_metrics_plots(client):
    response = client.get('/metrics/plots')
    assert response.status_code == 200
    assert b'<h1 id="pageTitle">Evoluci\xc3\xb3n de m\xc3\xa9tricas de competitividad &nbsp;</h1>' in response.data  # Adjust based on metrics_plots.html content

def test_error_with_cookie(client):
    error_data = {"code": "404", "description": "", "message": "Not Found"}
    client.set_cookie('error', json.dumps(error_data))

    response = client.get('/error')
    assert response.status_code == 200
    assert b'404' in response.data
    assert b'Not Found' in response.data

def test_error_without_cookie(client):
    response = client.get('/error')
    assert response.status_code == 200
    assert b'Ha ocurrido un error desconocido' in response.data

def test_swagger_ui(client):
    response = client.get('/docs')
    assert response.status_code == 200
    assert b'<title>Swagger UI</title>' in response.data

def test_get_spec(client):
    response = client.get('/spec')
    assert response.status_code == 200
    assert response.content_type == 'application/yaml'
