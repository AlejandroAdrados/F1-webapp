import sqlite3
from contextlib import closing

DB_PATH = '/path/to/your/database.db'  # Especificar la ruta a la base de datos

def total_ranking(year, ranking):
    """
    Returns the total points of each driver up to a certain ranking
    :param year: year of the season
    :param ranking: ranking to consider
    """
    query = """
    SELECT driver_name, team, SUM(points) AS total_points
    FROM YearResults
    WHERE year = ? AND race_number <= ?
    GROUP BY driver_name
    ORDER BY total_points DESC
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (year, ranking))
            rows = cursor.fetchall()
    serialized_results = [
        {'driver_name': row[0], 'team': row[1], 'total_points': row[2]}
        for row in rows
    ]
    return serialized_results

def get_info():
    """
    Returns the years and the number of races saved in the database
    """
    query = """
    SELECT year, MAX(race_number) AS max_num_race
    FROM YearResults
    GROUP BY year
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
    serialized_results = [
        {'year': row[0], 'races': row[1]}
        for row in rows
    ]
    return serialized_results

def get_races(year):
    """
    Returns the number of races of a year
    :param year: year of the season
    """
    query = """
    SELECT MAX(race_number)
    FROM YearResults
    WHERE year = ?
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (year,))
            result = cursor.fetchone()
    return result[0] if result else 0

def competitor_score_in_ranking(driver_name, year, race_number):
    """
    Returns the total points of a driver up to a certain ranking
    :param driver_name: name of the driver
    :param year: year of the season
    :param race_number: number of the race
    """
    query = """
    SELECT SUM(points)
    FROM YearResults
    WHERE driver_name = ? AND year = ? AND race_number <= ?
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (driver_name, year, race_number))
            result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def competitor_team_in_year(driver_name, year):
    """
    Returns the team of a driver in a season
    :param driver_name: name of the driver
    :param year: year of the season
    """
    query = """
    SELECT team
    FROM YearResults
    WHERE driver_name = ? AND year = ?
    LIMIT 1
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (driver_name, year))
            result = cursor.fetchone()
    return result[0] if result else None

def competitor_position_in_ranking(driver_name, year, ranking):
    """
    Returns the position of a driver in a ranking
    :param driver_name: name of the driver
    :param year: year of the season
    :param ranking: ranking to consider
    """
    results = total_ranking(year, ranking)
    sorted_results = sorted(results, key=lambda x: x['total_points'], reverse=True)
    position = next((i + 1 for i, result in enumerate(sorted_results)
                    if result['driver_name'] == driver_name), None)
    return position

def competitor_position_history(driver_name, year, ranking):
    """
    Returns the history of the drivers that have occupied a certain position up to a ranking
    :param driver_name: name of the driver
    :param year: year of the season
    :param ranking: ranking to consider
    """
    history = []
    for rank in range(1, ranking+1):
        history.append(
            {'race': rank, 'position': competitor_position_in_ranking(driver_name, year, rank)}
        )
    return history

def competitors_list(year):
    """
    Returns the list of drivers of a year
    :param year: year of the season
    """
    query = """
    SELECT DISTINCT driver_name
    FROM YearResults
    WHERE year = ?
    ORDER BY driver_name
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (year,))
            result = cursor.fetchall()
    return [row[0] for row in result]

def num_competitors(year):
    """
    Returns the number of drivers of a year
    :param year: year of the season
    """
    competitors = competitors_list(year)
    return len(competitors)

def competitors_below(driver_name, year, ranking):
    """
    Returns the list of drivers below a certain driver in the ranking
    :param driver_name: name of the driver
    :param year: year of the season
    :param ranking: ranking to consider
    """
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    sorted_results = sorted(results, key=lambda x: x['total_points'], reverse=True)
    return [result['driver_name'] for result in sorted_results[position:]]

def competitors_above(driver_name, year, ranking):
    """
    Returns the list of drivers above a certain driver in the ranking
    :param driver_name: name of the driver
    :param year: year of the season
    :param ranking: ranking to consider
    """
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    if position:
        sorted_results = sorted(results, key=lambda x: x['total_points'], reverse=True)
        return [result['driver_name'] for result in sorted_results[:position - 1]]
    else:
        return None

def competitor_in_position_in_ranking(position, ranking, year):
    """
    Returns the driver in a certain position in the ranking
    :param position: position in the ranking
    :param ranking: ranking to consider
    :param year: year of the season
    """
    query = """
    SELECT driver_name, SUM(points) AS total_points
    FROM YearResults
    WHERE race_number <= ? AND year = ?
    GROUP BY driver_name
    ORDER BY total_points DESC
    LIMIT 1 OFFSET ?
    """
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query, (ranking, year, position - 1))
            result = cursor.fetchone()
    return result[0] if result else None

def positions_swaps_in_ranking(year, ranking):
    """
    Returns the position swaps between two rankings
    :param year: year of the season
    :param ranking: ranking to consider
    """
    result = []
    competitors_number = num_competitors(year)
    for i in range(1, competitors_number + 1):
        competitor_in_current_position = competitor_in_position_in_ranking(i, ranking, year)
        competitors_above_current_ranking = competitors_above(competitor_in_current_position, year, ranking)
        competitors_above_past_ranking = competitors_above(competitor_in_current_position, year, ranking - 1)
        if competitors_above_past_ranking:
            if set(competitors_above_current_ranking) != set(competitors_above_past_ranking):
                competitors_below_current_ranking = competitors_below(competitor_in_current_position, year, ranking)
                overtaken_competitors = list(set(competitors_above_past_ranking) & set(competitors_below_current_ranking))
                current_position = competitor_position_in_ranking(competitor_in_current_position, year, ranking)
                if overtaken_competitors:
                    result.append((current_position, competitor_in_current_position, overtaken_competitors))
    return result

def positions_swaps_until_ranking(year, ranking):
    """
    Returns the position swaps up to a certain ranking
    :param year: year of the season
    :param ranking: ranking to consider
    """
    result = []
    for i in range(2, ranking+1):
        result.append(positions_swaps_in_ranking(year, i))
    return result
