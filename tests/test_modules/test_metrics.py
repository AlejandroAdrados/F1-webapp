import pytest
import networkx as nx
from app.modules.metrics import (
    normalized_degree,
    normalized_weight,
    clustering_coefficient,
    kendall_correlation,
    evolutionary_kendall_correlation,
    weighted_graph_metrics,
    unweighted_graph_metrics
)

@pytest.fixture
def graph():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])
    nx.set_edge_attributes(G, 1, 'weight')
    return G

def test_normalized_degree(graph):
    result = normalized_degree(graph)
    assert result == pytest.approx(2/3)

def test_normalized_weight(graph):
    result = normalized_weight(graph, 3)
    assert result == pytest.approx(1/3)

def test_clustering_coefficient(graph):
    result = clustering_coefficient(graph)
    assert result == pytest.approx(0)

@pytest.mark.skip()
def test_kendall_correlation(graph):
    result = kendall_correlation(graph)
    assert result == pytest.approx(0.33333333333333337)

def test_evolutionary_kendall_correlation(graph):
    result = evolutionary_kendall_correlation(graph, 3)
    assert result == pytest.approx(1/3)

@pytest.mark.skip()
def test_weighted_graph_metrics(graph):
    result = weighted_graph_metrics(graph, 3)
    expected = {
        'Grado Normalizado': 0.5,
        'Peso Normalizado': 0.3333333333333333,
        'Coeficiente de Clustering': 0.5,
        'Kendall': 0.33333333333333337,
        'Kendall Evolutivo': 0.6666666666666667
    }
    assert result == expected

@pytest.mark.skip()
def test_unweighted_graph_metrics(graph):
    result = unweighted_graph_metrics(graph)
    expected = {
        'Grado Normalizado': 0.5,
        'Coeficiente de Clustering': 0.5,
        'Kendall': 0.33333333333333337
    }
    assert result == expected

@pytest.mark.skip()
def test_empty_graph():
    G = nx.Graph()
    result = normalized_degree(G)
    assert result == 0

@pytest.mark.skip()
def test_single_node_graph():
    G = nx.Graph()
    G.add_node(1)
    result = normalized_degree(G)
    assert result == 0
