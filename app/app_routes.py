from flask import Blueprint, render_template, request, make_response
import json
import http.client

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/competitor')
def competitor_dashboard():
    return render_template('competitor_dashboard.html')

@app.route('/clasification')
def clasification():
    return render_template('clasification.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/metrics')
def metrics():
    return render_template('metrics.html')

@app.route('/metrics/plots')
def metrics_plots():
    return render_template('metrics_plots.html')

@app.route('/error')
def error():
    error = {"code": "500", "description": "", "message": "Ha ocurrido un error desconocido."}
    error_message_json = request.cookies.get('error')
    if error_message_json:
        error_message = json.loads(error_message_json)
        error = error_message
    error["description"] = http.client.responses.get(int(error["code"]), "Desconocido")
    response = make_response(render_template('error.html', error=error))
    response.set_cookie('error', '', expires=0)
    return response



