from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import networkx as nx
from app.modules.graphs import graph_in_ranking, graph_until_ranking, weighted_graph, convert_networkx_to_plotly

import plotly.graph_objs as go


def test_convert_networkx_to_plotly():
    # Create a sample graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4)])
    edge_labels = {(1, 2): 1, (2, 3): 2, (3, 4): 3}

    # Call the function
    fig = convert_networkx_to_plotly(G, edge_labels)

    # Check if the figure is an instance of plotly.graph_objs.Figure
    assert isinstance(fig, go.Figure)

    # Check if the figure contains the correct number of traces
    assert len(fig.data) == 2

    # Check if the edge trace is correctly created
    edge_trace = fig.data[0]
    assert isinstance(edge_trace, go.Scatter)
    assert edge_trace.mode == 'lines'
    assert len(edge_trace.x) == 9  # 3 edges * 3 points (x0, x1, None)
    assert len(edge_trace.y) == 9  # 3 edges * 3 points (y0, y1, None)

    # Check if the node trace is correctly created
    node_trace = fig.data[1]
    assert isinstance(node_trace, go.Scatter)
    assert node_trace.mode == 'text'
    assert len(node_trace.x) == 4  # 4 nodes
    assert len(node_trace.y) == 4  # 4 nodes
    assert len(node_trace.text) == 4  # 4 nodes

    # Check if the annotations are correctly created
    annotations = fig.layout.annotations
    assert len(annotations) == 4  # 4 edge labels
    for annotation in annotations[1:]:
        assert annotation.text in ['1', '2', '3']
        assert annotation.font.size == 12
        assert annotation.font.color == 'black'
        assert annotation.bgcolor == 'white'
        assert annotation.opacity == 0.8

    # Check if the shapes are correctly created
    shapes = fig.layout.shapes
    assert len(shapes) == 3  # 3 edges
    for shape in shapes:
        assert shape.type == 'line'
        assert shape.line.color == 'darkgray'
        assert shape.line.width in [1, 2, 3]


@patch('app.modules.database.positions_swaps_in_ranking')
@patch('app.modules.database.competitors_list')
def test_graph_in_ranking(mock_competitors_list, mock_positions_swaps_in_ranking):
    mock_competitors_list.return_value = ['Driver1', 'Driver2', 'Driver3']
    mock_positions_swaps_in_ranking.return_value = [
        (1, 'Driver1', ['Driver2']),
        (2, 'Driver2', ['Driver3'])
    ]
    G = graph_in_ranking(2021, 5)
    assert len(G.nodes) == 3
    assert len(G.edges) == 2
    assert ('Driver1', 'Driver2') in G.edges
    assert ('Driver2', 'Driver3') in G.edges


@patch('app.modules.database.positions_swaps_until_ranking')
@patch('app.modules.database.competitors_list')
def test_graph_until_ranking(mock_competitors_list, mock_positions_swaps_until_ranking):
    mock_competitors_list.return_value = ['Driver1', 'Driver2', 'Driver3']
    mock_positions_swaps_until_ranking.return_value = [
        (1, 'Driver1', ['Driver2']),
        (2, 'Driver2', ['Driver3'])
    ]
    G, swaps_list = graph_until_ranking(2021, 5)
    assert len(G.nodes) == 3
    assert len(swaps_list) == 2


def test_weighted_graph():
    G = nx.Graph()
    G.add_nodes_from(['Driver1', 'Driver2', 'Driver3'])
    swaps_list = [
        [(1, 'Driver1', ['Driver2'])],
        [(2, 'Driver2', ['Driver3'])]
    ]
    bonuses = {1: 2, 2: 3}
    G, important_labels = weighted_graph(G, swaps_list, bonuses)
    assert len(G.edges) == 2
    assert G.edges['Driver1', 'Driver2']['weight'] == 2
    assert G.edges['Driver2', 'Driver3']['weight'] == 3
    assert important_labels == {('Driver1', 'Driver2'): 2, ('Driver2', 'Driver3'): 3}
