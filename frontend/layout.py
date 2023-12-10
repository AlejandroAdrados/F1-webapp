from dash import dcc, html

# Definir el diseño del dashboard
layout = html.Div([
    html.H1("Datos de Competidor"),
    html.Button("Obtener Datos", id="fetch-button"),
    html.Div(id="fetch-output"),
])