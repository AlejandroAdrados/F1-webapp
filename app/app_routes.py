"""
Class that defines the routes for the application.
"""
import http.client
import json

from flask import Blueprint, make_response, render_template, request, send_from_directory

app = Blueprint('app', __name__)


@app.route('/')
def index():
    """
    Renders the index page.

    Returns:
        Response: The rendered HTML of the index page.
    """
    return render_template('index.html')


@app.route('/competitor')
def competitor_dashboard():
    """
    Renders the competitor dashboard page.

    Returns:
        Response: A Flask response object that renders the 'competitor_dashboard.html' template.
    """
    return render_template('competitor_dashboard.html')


@app.route('/clasification')
def clasification():
    """
    Renders the classification page.

    Returns:
        Response: The rendered 'clasification.html' template.
    """
    return render_template('clasification.html')


@app.route('/graph')
def graph():
    """
    Renders the 'graph.html' template.

    Returns:
        A rendered HTML template for the graph page.
    """
    return render_template('graph.html')


@app.route('/metrics')
def metrics():
    """
    Renders the metrics page.

    Returns:
        Response: A Flask response object that renders the 'metrics.html' template.
    """
    return render_template('metrics.html')


@app.route('/metrics/plots')
def metrics_plots():
    """
    Renders the metrics plots page.

    Returns:
        A rendered template for the metrics plots page.
    """
    return render_template('metrics_plots.html')


@app.route('/error')
def error():
    """
    Handles the error page rendering.

    This function retrieves an error message from the cookies, if available,
    and uses it to render an error page. If no error message is found in the
    cookies, a default error message is used. The error description is updated
    based on the HTTP status code. The function also clears the error cookie
    after rendering the error page.

    Returns:
        Response: A Flask response object with the rendered error page.
    """
    error_content = {"code": "500", "description": "",
                     "message": "Ha ocurrido un error desconocido."}
    error_message_json = request.cookies.get('error')
    if error_message_json:
        error_message = json.loads(error_message_json)
        error_content = error_message
    error_content["description"] = http.client.responses.get(
        int(error_content["code"]), "Desconocido")
    response = make_response(render_template('error.html', error=error_content))
    response.set_cookie('error', '', expires=0)
    return response


@app.route('/docs')
def swagger_ui():
    """
    Renders the Swagger UI template.

    This function returns the rendered HTML template for the Swagger UI,
    which provides a web-based interface for interacting with the API's
    documentation and testing endpoints.

    Returns:
        str: The rendered HTML content of the Swagger UI template.
    """
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    """
    Retrieves the Swagger specification file.

    This function prints the root path of the application and returns the
    'swagger.yaml' file from the application's root directory.

    Returns:
        Response: A Flask response object that sends the 'swagger.yaml' file
        from the application's root directory.
    """
    print(app.root_path)
    return send_from_directory(app.root_path, 'swagger.yaml')
