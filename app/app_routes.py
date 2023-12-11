from flask import Blueprint, render_template

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

@app.route('/metrics/plots')
def metrics_plots():
    return render_template('metrics_plots.html')
