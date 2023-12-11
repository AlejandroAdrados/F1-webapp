import networkx as nx
import pandas as pd
import math


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
    max_possible_weight_sum = math.comb(num_nodes,2) * (num_rankings - 1)
    if max_possible_weight_sum == 0:
        return 0
    coefficient = 1 - (2 * weight_sum) / max_possible_weight_sum
    return coefficient


# Función que imprime las métricas de un grafo ponderado
def weighted_graph_metrics(graph, num_rankings):
    normalized_degree_value = normalized_degree(graph)
    normalized_weight_value = normalized_weight(graph, num_rankings)
    clustering_coefficient_value = clustering_coefficient(graph)
    kendall_coefficient = kendall_correlation(graph)
    evolutionary_kendall_coefficient = evolutionary_kendall_correlation(graph, num_rankings)

    stats = {
        'Grado Normalizado': normalized_degree_value,
        'Peso Normalizado': normalized_weight_value,
        'Coeficiente de Clustering': clustering_coefficient_value,
        'Kendall': kendall_coefficient,
        'Kendall Evolutivo': evolutionary_kendall_coefficient
    }

    return stats


# Función que imprime las métricas de un grafo no ponderado
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


# Función que compara las métricas de varios grafos
def comparation_metrics(graphs):
    statistics = []
    i = 0
    for elements in graphs:
        i += 1
        current_graph = elements[0][0]
        year = elements[1]
        ranking = elements[2]
        normalized_degree_value = normalized_degree(current_graph)
        normalized_weight_value = normalized_weight(current_graph, ranking)
        clustering_coefficient_value = clustering_coefficient(current_graph)
        kendall_coefficient = kendall_correlation(current_graph)
        evolutionary_kendall_coefficient = evolutionary_kendall_correlation(current_graph, ranking)

        statistics.append({
            'Grafo': f'Jornada {ranking} año {year}',
            'Grado Normalizado': normalized_degree_value,
            'Peso Normalizado': normalized_weight_value,
            'Coeficiente de Clustering': clustering_coefficient_value,
            'Kendall': kendall_coefficient,
            'Kendall Evolutivo': evolutionary_kendall_coefficient
        })

    stats_df = pd.DataFrame(statistics)
    return stats_df
