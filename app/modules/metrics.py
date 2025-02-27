"""
Functions to calculate metrics for a graph.
"""

import math

import networkx as nx

from app.modules import graphs


def normalized_degree(graph):
    """
    Calculate the normalized degree of a graph.

    Args:
        graph: NetworkX graph object

    Returns:
        float: The normalized degree value of the graph
    """
    num_nodes = graph.number_of_nodes()
    degree_sum = sum(dict(graph.degree()).values())
    max_possible_degree_sum = num_nodes * (num_nodes - 1)
    return degree_sum / max_possible_degree_sum


def normalized_weight(graph, num_rankings):
    """
    Calculate the normalized weight of a graph.

    Args:
        graph: NetworkX graph object
        num_rankings (int): Number of rankings considered

    Returns:
        float: The normalized weight value of the graph
    """
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    weight_sum = sum(edge_weights.values())
    num_nodes = graph.number_of_nodes()
    combinatory_number = math.comb(num_nodes, 2)
    max_possible_weight_sum = combinatory_number * (num_rankings - 1)
    if max_possible_weight_sum == 0:
        return 0
    return weight_sum / max_possible_weight_sum


def clustering_coefficient(graph):
    """
    Calculate the clustering coefficient of a graph.

    Args:
        graph: NetworkX graph object

    Returns:
        float: The average clustering coefficient of the graph
    """
    clustering_coeffs = nx.clustering(graph)
    return sum(clustering_coeffs.values()) / graph.number_of_nodes()


def kendall_correlation(graph):
    """
    Calculate the Kendall correlation coefficient of a graph.

    Args:
        graph: NetworkX graph object

    Returns:
        float: The Kendall correlation coefficient
    """
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    coefficient = 1 - (4 * num_edges) / (num_nodes * (num_nodes - 1))
    return coefficient


def evolutionary_kendall_correlation(graph, num_rankings):
    """
    Calculate the evolutionary Kendall correlation coefficient of a graph.

    Args:
        graph: NetworkX graph object
        num_rankings (int): Number of rankings considered

    Returns:
        float: The evolutionary Kendall correlation coefficient
    """
    num_nodes = graph.number_of_nodes()
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    weight_sum = sum(edge_weights.values())
    max_possible_weight_sum = math.comb(num_nodes, 2) * (num_rankings - 1)
    if max_possible_weight_sum == 0:
        return 0
    coefficient = 1 - (2 * weight_sum) / max_possible_weight_sum
    return coefficient


def weighted_graph_metrics(graph, num_rankings):
    """
    Get metrics for a weighted graph.

    Args:
        graph: NetworkX graph object
        num_rankings (int): Number of rankings considered

    Returns:
        dict: Dictionary containing normalized degree, normalized weight,
             clustering coefficient, Kendall and evolutionary Kendall coefficients
    """
    normalized_degree_value = normalized_degree(graph)
    normalized_weight_value = normalized_weight(graph, num_rankings)
    clustering_coefficient_value = clustering_coefficient(graph)
    kendall_coefficient = kendall_correlation(graph)
    evolutionary_kendall_coefficient = evolutionary_kendall_correlation(
        graph, num_rankings)

    stats = {
        'Grado Normalizado': normalized_degree_value,
        'Peso Normalizado': normalized_weight_value,
        'Coeficiente de Clustering': clustering_coefficient_value,
        'Kendall': kendall_coefficient,
        'Kendall Evolutivo': evolutionary_kendall_coefficient
    }

    return stats


def unweighted_graph_metrics(graph):
    """
    Get metrics for an unweighted graph.

    Args:
        graph: NetworkX graph object

    Returns:
        dict: Dictionary containing normalized degree,
             clustering coefficient and Kendall coefficient
    """
    normalized_degree_value = normalized_degree(graph)
    clustering_coefficient_value = clustering_coefficient(graph)
    kendall_coefficient = kendall_correlation(graph)

    stats = {
        'Grado Normalizado': normalized_degree_value,
        'Coeficiente de Clustering': clustering_coefficient_value,
        'Kendall': kendall_coefficient
    }

    return stats


def season_metrics(year, ranking, bonus):
    """
    Calculate metrics for a complete F1 season.

    Args:
        year (int): Season year
        ranking (int): Number of rankings to consider
        bonus (bool): Whether to apply bonus points

    Returns:
        list: List of tuples containing metrics for each ranking,
              year and ranking number
    """
    season_metrics_list = []
    for rank in range(ranking):
        graph, swaps_list = graphs.graph_until_ranking(year, rank+1)
        if bonus:
            bonuses = {1: 4, 2: 3, 3: 2}
            weighted_graph = graphs.weighted_graph(
                graph, swaps_list, bonuses)[0]
        else:
            weighted_graph = graphs.weighted_graph(graph, swaps_list)[0]
        ranking_metrics = weighted_graph_metrics(weighted_graph, rank+1)
        season_metrics_list.append((ranking_metrics, year, rank+1))
    return season_metrics_list
