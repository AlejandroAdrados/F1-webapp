import dash
from dash import dcc, html

# Define el layout del frontend
layout = html.Div([
    html.H1('¡Hola, Dash en Flask!'),
    dcc.Graph(
        id='ejemplo-grafico',
        figure={
            'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Ejemplo'}],
            'layout': {'title': 'Gráfico de ejemplo'}
        }
    )
])