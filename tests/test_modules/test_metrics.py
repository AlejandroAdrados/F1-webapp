from unittest.mock import patch

import pytest
import networkx as nx
from app.modules.metrics import (
    normalized_degree,
    normalized_weight,
    clustering_coefficient,
    kendall_correlation,
    evolutionary_kendall_correlation,
    weighted_graph_metrics,
    unweighted_graph_metrics,
    season_metrics
)

@pytest.fixture(scope='function')
def graph():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edges_from([(1, 2), (2, 3)])
    return G

def test_normalized_degree(graph):
    result = normalized_degree(graph)
    assert result == pytest.approx(1/3)

def test_normalized_weight(graph):
    result = normalized_weight(graph, 3)
    assert result == pytest.approx(0)

def test_clustering_coefficient(graph):
    result = clustering_coefficient(graph)
    assert result == pytest.approx(0)

def test_kendall_correlation(graph):
    result = kendall_correlation(graph)
    assert result == pytest.approx(0.33333333333333337)

def test_evolutionary_kendall_correlation(graph):
    result = evolutionary_kendall_correlation(graph, 3)
    assert result == pytest.approx(1)

def test_weighted_graph_metrics(graph):
    result = weighted_graph_metrics(graph, 3)
    expected = {
        'Grado Normalizado': pytest.approx(1/3),
        'Peso Normalizado': 0,
        'Coeficiente de Clustering': 0,
        'Kendall': pytest.approx(1/3),
        'Kendall Evolutivo': 1
    }
    assert result == expected

def test_unweighted_graph_metrics(graph):
    result = unweighted_graph_metrics(graph)
    expected = {
        'Grado Normalizado': pytest.approx(1/3),
        'Coeficiente de Clustering': 0,
        'Kendall': pytest.approx(1/3)
    }
    assert result == expected

@patch('app.modules.metrics.graphs')
def test_season_metrics_no_bonus(mock_graphs, graph):
    mock_graphs.graph_until_ranking.return_value = (graph, [])
    mock_graphs.weighted_graph.return_value = (graph, [])
    
    result = season_metrics(2023, 3, False)
    assert len(result) == 3
    for metrics, year, rank in result:
        assert year == 2023
        assert rank in [1, 2, 3]
        assert 'Grado Normalizado' in metrics
        assert 'Peso Normalizado' in metrics
        assert 'Coeficiente de Clustering' in metrics
        assert 'Kendall' in metrics
        assert 'Kendall Evolutivo' in metrics

@patch('app.modules.metrics.graphs')
def test_season_metrics_with_bonus(mock_graphs, graph):
    mock_graphs.graph_until_ranking.return_value = (graph, [])
    mock_graphs.weighted_graph.return_value = (graph, [])
    
    result = season_metrics(2023, 3, True)
    
    assert len(result) == 3
    for metrics, year, rank in result:
        assert year == 2023
        assert rank in [1, 2, 3]
        assert 'Grado Normalizado' in metrics
        assert 'Peso Normalizado' in metrics
        assert 'Coeficiente de Clustering' in metrics
        assert 'Kendall' in metrics
        assert 'Kendall Evolutivo' in metrics
