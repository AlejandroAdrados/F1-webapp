import networkx as nx
from app.modules import database as db
import plotly.graph_objs as go


# Función que crea un grafo de los cambios de posición de los pilotos en una ranking
def graph_in_ranking(year, ranking):
    G = nx.Graph()
    G.add_nodes_from(db.competitors_list(year))
    swaps_list = db.positions_swaps_in_ranking(year, ranking)
    for i in swaps_list:
        for j in i[2]:
            G.add_edge(i[1], j)
    return G


# Función que crea un grafo de los cambios de posición hasta una ranking
def graph_until_ranking(year, ranking):
    G = nx.Graph()
    G.add_nodes_from(db.competitors_list(year))
    swaps_list = db.positions_swaps_until_ranking(year, ranking)
    return G, swaps_list


def weighted_graph(G, swaps_list, bonuses={}):
    edge_weights = {}
    for i in swaps_list:
        for j in i:
            # Obtener la bonificación según la posición
            current_position = j[0]
            bonus = bonuses.get(current_position, 1)  # Si la posición no tiene bonificación especial, se otorga 1 punto
            for k in j[2]:
                # Define la tupla de la dupla de pilotos
                edge = (j[1], k)
                if edge in edge_weights:
                    # Si la dupla ya existe, aumenta el peso en la bonificación correspondiente
                    edge_weights[edge] += bonus
                else:
                    # Si es una nueva dupla, crea una nueva entrada con peso igual a la bonificación
                    edge_weights[edge] = bonus
                    # Agrega las aristas con pesos al grafo
    for edge, weight in edge_weights.items():
        G.add_edge(edge[0], edge[1], weight=weight)
    labels = nx.get_edge_attributes(G, "weight")
    important_labels = {edge: weight for edge, weight in labels.items() if weight > 1}
    return G, important_labels

def convert_networkx_to_plotly(G, edge_labels):
    pos = nx.shell_layout(G)

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='text',
        mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)  # Usa paréntesis para crear una tupla en lugar de corchetes
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2))
)

    node_trace['x'] = []  # Inicializa como lista vacía
    node_trace['y'] = []  # Inicializa como lista vacía

    import numpy as np

    for node in G.nodes():
        x, y = pos[node]
        if isinstance(x, np.float64):
            x_list = [float(x)]  # Convertir a float y luego a lista
        else:
            x_list = list(x)  # Si es iterable, mantenerlo como lista

        if isinstance(y, np.float64):
            y_list = [float(y)]  # Convertir a float y luego a lista
        else:
            y_list = list(y)  # Si es iterable, mantenerlo como lista

        # Convertir las tuplas existentes a listas
        node_trace['x'] = list(node_trace['x'])
        node_trace['y'] = list(node_trace['y'])

        # Crear nuevas listas con los valores existentes y los nuevos valores
        node_trace['x'] = list(node_trace['x']) + x_list
        node_trace['y'] = list(node_trace['y']) + y_list

        node_trace['text'] = list(node_trace['text']) + [node]

    node_trace['mode'] = 'text'



    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title="",
                       #plot_bgcolor='white',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
               )
    
    # Añadir etiquetas personalizadas de las aristas al gráfico
    for edge, label in edge_labels.items():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        x_coords = [x0, x1, None]
        y_coords = [y0, y1, None]
        # Calcular el punto medio de la arista para colocar la etiqueta
        x_mid = np.mean([x0, x1])
        y_mid = np.mean([y0, y1])

        fig.add_trace(go.Scatter(
            x=[x_mid],  # Colocar el texto en el punto medio x de la arista
            y=[y_mid],  # Colocar el texto en el punto medio y de la arista
            mode='text',
            text=[f'{label}'],
            textfont=dict(size=10),  # Ajustar el tamaño de la fuente
            hoverinfo='none',
            showlegend=False
        ))

    return fig

