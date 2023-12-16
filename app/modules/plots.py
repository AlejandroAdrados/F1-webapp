from app.modules import graphs, metrics, database as db
import matplotlib.pyplot as plt
import networkx as nx


def season_metrics(year, ranking, bonus):
    season_metrics = []
    for rank in range(ranking):
        graph, swaps_list = graphs.graph_until_ranking(year, rank+1)
        if bonus:
            bonuses = {1: 4, 2: 3, 3: 2}
            weighted_graph = graphs.weighted_graph(graph, swaps_list, bonuses)[0]
        else:
            weighted_graph = graphs.weighted_graph(graph, swaps_list)[0]
        ranking_metrics = metrics.weighted_graph_metrics(weighted_graph, rank+1)
        season_metrics.append((ranking_metrics, year, rank+1))
    return season_metrics


def mean_degree_plot(df_array, save = False):
    plt.figure(figsize=(8, 5))
    for df, year in df_array:
        plt.plot(df.index, df['Grado Normalizado'], label=year)
        plt.xlabel('Jornadas')
        plt.ylabel('Grado Medio Normalizado')
    plt.title('Comparación del Grado Medio Normalizado.')
    plt.legend()
    plt.grid(True)
    plt.show()


def mean_weight_plot(df_array, save = False):
    plt.figure(figsize=(8, 5))
    for df, year in df_array:
        plt.plot(df.index, df['Peso Normalizado'], label=year)
        plt.xlabel('Jornadas')
        plt.ylabel('Peso Medio Normalizado')
    plt.title('Comparación del Peso Medio Normalizado.')
    plt.legend()
    plt.grid(True)
    plt.show()


def clustering_coefficient_plot(df_array, save = False):
    plt.figure(figsize=(8, 5))
    for df, year in df_array:
        plt.plot(df.index, df['Coeficiente de Clustering'], label=year)
        plt.xlabel('Jornadas')
        plt.ylabel('Coeficiente de Clustering')
    plt.title('Comparación del Coeficiente de Clustering.')
    plt.legend()
    plt.grid(True)
    plt.show()


def kendall_plot(df_array, save = False):
    plt.figure(figsize=(8, 5))
    for df, year in df_array:
        plt.plot(df.index, df['Kendall'], label=year)
        plt.xlabel('Jornadas')
        plt.ylabel('Coeficiente de Kendall')
    plt.title('Comparación del Coeficiente de Kendall.')
    plt.legend()
    plt.grid(True)
    plt.show()


def evolutionary_kendall_plot(df_array, save = False):
    plt.figure(figsize=(8, 5))
    for df, year in df_array:
        plt.plot(df.index, df['Kendall Evolutivo'], label=year)
        plt.xlabel('Jornadas')
        plt.ylabel('Coeficiente de Kendall Evolutivo')
    plt.title('Comparación del Coeficiente de Kendall Evolutivo.')
    plt.legend()
    plt.grid(True)
    plt.show()
