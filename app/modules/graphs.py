"""
Functions to create and visualize graphs representing position changes in a championship ranking.
"""

import networkx as nx
import numpy as np
import plotly.graph_objs as go

from app.modules import database as db


def graph_in_ranking(year, ranking):
    """
    Creates a graph representing position changes of drivers in a specific ranking.

    Args:
        year (int): The year of the championship
        ranking (int): The ranking number to analyze

    Returns:
        networkx.Graph: Graph where nodes are drivers and edges represent position changes
    """
    graph = nx.Graph()
    graph.add_nodes_from(db.competitors_list(year))
    swaps_list = db.positions_swaps_in_ranking(year, ranking)
    for i in swaps_list:
        for j in i[2]:
            graph.add_edge(i[1], j)
    return graph


def graph_until_ranking(year, ranking):
    """
    Creates a graph representing position changes up to a specific ranking.

    Args:
        year (int): The year of the championship
        ranking (int): The target ranking number

    Returns:
        tuple: (networkx.Graph, list) - The graph and list of position swaps
    """
    graph = nx.Graph()
    graph.add_nodes_from(db.competitors_list(year))
    swaps_list = db.positions_swaps_until_ranking(year, ranking)
    return graph, swaps_list


def weighted_graph(graph, swaps_list, bonuses={}):
    """
    Creates a weighted graph based on position changes and bonus points.

    Args:
        graph (networkx.Graph): The initial graph
        swaps_list (list): List of position changes
        bonuses (dict): Dictionary of position-based bonus points

    Returns:
        tuple: (networkx.Graph, dict) - The weighted graph and dictionary of important edge labels
    """
    edge_weights = {}
    for i in swaps_list:
        for j in i:
            # Get bonus based on position
            current_position = j[0]
            # If position has no special bonus, assign 1 point
            bonus = bonuses.get(current_position, 1)
            for k in j[2]:
                # Define the tuple for the pair of drivers
                edge = (j[1], k)
                if edge in edge_weights:
                    # If the pair exists, increase the weight by the corresponding bonus
                    edge_weights[edge] += bonus
                else:
                    # If it's a new pair, create new entry with weight equal to bonus
                    edge_weights[edge] = bonus
                    # Add weighted edges to the graph
    for edge, weight in edge_weights.items():
        graph.add_edge(edge[0], edge[1], weight=weight)
    # If you want to export the graph:
    # nx.write_gml(G, "app/static/graph.gml")
    labels = nx.get_edge_attributes(graph, "weight")
    important_labels = {edge: weight for edge,
                        weight in labels.items() if weight > 1}
    return graph, important_labels


def convert_networkx_to_plotly(graph, edge_labels):
    """
    Converts a NetworkX graph to a Plotly figure for visualization.

    Args:
        G (networkx.Graph): The NetworkX graph to convert
        edge_labels (dict): Dictionary of edge labels to display

    Returns:
        plotly.graph.objs.Figure: Interactive Plotly figure of the graph
    """
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.shell_layout(graph)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line={"width": 0.5, "color": '#000'},
        hoverinfo='text',
        mode='lines')

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        # Use parentheses to create a tuple instead of brackets
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker={
            "showscale": True,
            "colorscale": 'YlGnBu',
            "reversescale": True,
            "color": [],
            "size": 10,
            "colorbar": {
                "thickness": 15,
                "title": 'Node Connections',
                "xanchor": 'left',
                "titleside": 'right'
            },
            "line": {"width": 2}}
    )

    node_trace['x'] = []  # Initialize as empty list
    node_trace['y'] = []  # Initialize as empty list

    for node in graph.nodes():
        x, y = pos[node]
        if isinstance(x, np.float64):
            x_list = [float(x)]  # Convert to float and then to list
        else:
            x_list = list(x)  # If iterable, keep as list

        if isinstance(y, np.float64):
            y_list = [float(y)]  # Convert to float and then to list
        else:
            y_list = list(y)  # If iterable, keep as list

        # Convert existing tuples to lists
        node_trace['x'] = list(node_trace['x'])
        node_trace['y'] = list(node_trace['y'])

        # Create new lists with existing and new values
        node_trace['x'] = list(node_trace['x']) + x_list
        node_trace['y'] = list(node_trace['y']) + y_list

        node_trace['text'] = list(node_trace['text']) + [node]

    node_trace['mode'] = 'text'

    node_trace['textfont'] = {"color": 'black'}
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
        plot_bgcolor='white',
        showlegend=False,
        hovermode='closest',
        margin={"b": 20, "l": 5, "r": 5, "t": 40},
        annotations=[{
            "text": "",
            "showarrow": False,
            "xref": "paper", "yref": "paper",
            "x": 0.005, "y": -0.002}],
        xaxis={"showgrid": False, "zeroline": False,
               "showticklabels": False, "visible": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        height=800  # Set the figure box height
    )
    )

    # Add custom edge labels to the graph
    for edge, label in edge_labels.items():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        # Calculate the midpoint of the edge to place the label
        x_mid = np.mean([x0, x1])
        y_mid = np.mean([y0, y1])

        fig.add_shape(
            type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line={"width": label, "color": 'darkgray'},
        )
        fig.add_annotation(
            x=x_mid, y=y_mid,  # Text coordinates
            text=label,  # Label text
            # Adjust font size and color of the text
            font={"size": 12, "color": 'black'},
            showarrow=False,  # Don't show arrow
            xref="x", yref="y",
            bgcolor="white",  # White background
            borderpad=2,  # Space between text and border
            opacity=0.8  # White background opacity
        )
    return fig
