import dash
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import requests

# Registrar los callbacks
def register_callbacks(app):
    @app.callback(
        Output('fetch-output', 'children'),
        [Input('fetch-button', 'n_clicks')]
    )
    def update_output(n_clicks):   
        if not n_clicks:
            raise dash.exceptions.PreventUpdate

        url = "http://localhost:8050/api/competitor/history?year=2023&race=20&driver=Fernando%20Alonso"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return [html.P(f'Posición: {position}') for position in data]
        
        return html.P('No se recibieron datos')
