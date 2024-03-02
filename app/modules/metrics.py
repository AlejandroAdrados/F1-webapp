import networkx as nx
import math
import app.modules.graphs as graphs

# Función que calcula el grado normalizado de un grafo
def normalized_degree(graph):
    num_nodes = graph.number_of_nodes()
    degree_sum = sum(dict(graph.degree()).values())
    max_possible_degree_sum = num_nodes * (num_nodes - 1)
    return degree_sum / max_possible_degree_sum


# Función que calcula el peso normalizado de un grafo
def normalized_weight(graph, num_rankings):
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    weight_sum = sum(edge_weights.values())
    num_nodes = graph.number_of_nodes()
    combinatory_number = math.comb(num_nodes, 2)
    max_possible_weight_sum = combinatory_number * (num_rankings - 1)
    if max_possible_weight_sum == 0:
        return 0
    return weight_sum / max_possible_weight_sum


# Función que calcula el coeficiente de agrupamiento de un grafo
def clustering_coefficient(graph):
    clustering_coeffs = nx.clustering(graph)
    return sum(clustering_coeffs.values()) / graph.number_of_nodes()


# Función que calcula el coeficiente de correlación de Kendall de un grafo
def kendall_correlation(graph):
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    coefficient = 1 - (4 * num_edges) / (num_nodes * (num_nodes - 1))
    return coefficient


# Función que calcula el coeficiente de correlación de Kendall evolutivo de un grafo
def evolutionary_kendall_correlation(graph, num_rankings):
    num_nodes = graph.number_of_nodes()
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    weight_sum = sum(edge_weights.values())
    max_possible_weight_sum = math.comb(num_nodes, 2) * (num_rankings - 1)
    if max_possible_weight_sum == 0:
        return 0
    coefficient = 1 - (2 * weight_sum) / max_possible_weight_sum
    return coefficient


# Función que devuelve las métricas de un grafo ponderado
def weighted_graph_metrics(graph, num_rankings):
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


# Función que devuelve las métricas de un grafo no ponderado
def unweighted_graph_metrics(graph):
    normalized_degree_value = normalized_degree(graph)
    clustering_coefficient_value = clustering_coefficient(graph)
    kendall_coefficient = kendall_correlation(graph)

    stats = {
        'Grado Normalizado': normalized_degree_value,
        'Coeficiente de Clustering': clustering_coefficient_value,
        'Kendall': kendall_coefficient
    }

    return stats

# Función que devuelve las métricas de una temporada
def season_metrics(year, ranking, bonus):
    season_metrics = []
    for rank in range(ranking):
        graph, swaps_list = graphs.graph_until_ranking(year, rank+1)
        if bonus:
            bonuses = {1: 4, 2: 3, 3: 2}
            weighted_graph = graphs.weighted_graph(
                graph, swaps_list, bonuses)[0]
        else:
            weighted_graph = graphs.weighted_graph(graph, swaps_list)[0]
        ranking_metrics = weighted_graph_metrics(weighted_graph, rank+1)
        season_metrics.append((ranking_metrics, year, rank+1))
    return season_metrics
