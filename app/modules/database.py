"""
Functions to query the database and return results.
"""

from app import db
from app.models import YearResults


def total_ranking(year, ranking):
    """
    Returns the classification of a ranking.

    Args:
        year (int): The year of the season
        ranking (int): The race number to calculate rankings up to

    Returns:
        list: List of dictionaries containing driver name, team and total points
    """
    results = db.session.query(YearResults.driver_name, YearResults.team,
                               db.func.SUM(YearResults.points).label('total_points')) \
        .filter(YearResults.year == year, YearResults.race_number <= ranking) \
        .group_by(YearResults.driver_name) \
        .order_by(db.func.SUM(YearResults.points).desc()) \
        .all()
    serialized_results = [
        {'driver_name': row.driver_name, 'team': row.team,
            'total_points': row.total_points}
        for row in results
    ]
    return serialized_results


def get_info():
    """
    Returns the years and number of seasons in the database.

    Returns:
        list: List of dictionaries containing year and number of races for each season
    """
    results = db.session.query(
        YearResults.year,
        db.func.max(YearResults.race_number).label('max_num_race')
    ).group_by(YearResults.year).all()
    serialized_results = [
        {'year': row.year, 'races': row.max_num_race}
        for row in results
    ]
    return serialized_results


def get_races(year):
    """
    Returns the number of races in a year.

    Args:
        year (int): The year to query

    Returns:
        int: Number of races in the specified year
    """
    result = db.session.query(db.func.max(YearResults.race_number)).filter(
        YearResults.year == year).scalar()
    return result


def competitor_score_in_ranking(driver_name, year, race_number):
    """
    Returns a driver's points in a specific ranking.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year
        race_number (int): Race number to calculate points up to

    Returns:
        float: Total points for the driver, 0 if no results found
    """
    result = db.session.query(db.func.sum(YearResults.points)).\
        filter(YearResults.driver_name == driver_name).\
        filter(YearResults.year == year).\
        filter(YearResults.race_number <= race_number).\
        scalar()
    if result:
        return result
    return 0


def competitor_team_in_year(driver_name, year):
    """
    Returns a driver's team in a specific season.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year

    Returns:
        str: Team name, None if not found
    """
    result = db.session.query(YearResults.team).\
        filter(YearResults.driver_name == driver_name).\
        filter(YearResults.year == year).\
        first()
    if result:
        return result[0]
    return None


def competitor_position_in_ranking(driver_name, year, ranking):
    """
    Returns a driver's position in a specific ranking.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year
        ranking (int): Race number to calculate position up to

    Returns:
        int: Position of the driver, None if not found
    """
    results = total_ranking(year, ranking)
    sorted_results = sorted(
        results, key=lambda x: x['total_points'], reverse=True)
    position = next((i + 1 for i, result in enumerate(sorted_results)
                    if result['driver_name'] == driver_name), None)
    return position


def competitor_position_history(driver_name, year, ranking):
    """
    Returns the historical positions of a driver up to a specific ranking.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year
        ranking (int): Race number to calculate history up to

    Returns:
        list: List of dictionaries containing race number and position
    """
    history = []
    i = 0
    for rank in range(1, ranking+1):
        i += 1
        history.append(
            {'race': i, 'position': competitor_position_in_ranking(driver_name, year, rank)})
    return history


def competitors_list(year):
    """
    Returns the list of drivers in a year.

    Args:
        year (int): Season year

    Returns:
        list: List of driver names
    """
    result = db.session.query(db.distinct(YearResults.driver_name)).filter(
        YearResults.year == year).order_by(YearResults.driver_name).all()
    serialized_result = [row[0] for row in result]
    return serialized_result


def num_competitors(year):
    """
    Returns the number of drivers in a year.

    Args:
        year (int): Season year

    Returns:
        int: Number of competitors, 0 if no data found
    """
    competitors = competitors_list(year)
    if competitors:
        return len(competitors)
    return 0


def competitors_below(driver_name, year, ranking):
    """
    Returns the drivers below a specific driver in a ranking.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year
        ranking (int): Race number to calculate positions from

    Returns:
        list: List of driver names that are below the specified driver
    """
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    sorted_results = sorted(
        results, key=lambda x: x['total_points'], reverse=True)
    return [result['driver_name'] for result in sorted_results[position:]]


def competitors_above(driver_name, year, ranking):
    """
    Returns the drivers above a specific driver in a ranking.

    Args:
        driver_name (str): Name of the driver
        year (int): Season year
        ranking (int): Race number to calculate positions from

    Returns:
        list: List of driver names that are above the specified driver, None if driver not found
    """
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    if position:
        sorted_results = sorted(
            results, key=lambda x: x['total_points'], reverse=True)
        return [result['driver_name'] for result in sorted_results[:position - 1]]
    return None


def competitor_in_position_in_ranking(position, ranking, year):
    """
    Returns the driver in a specific position in a ranking.

    Args:
        position (int): Position to query
        ranking (int): Race number to calculate position from
        year (int): Season year

    Returns:
        str: Driver name in the specified position, None if not found
    """
    competitor = (
        db.session.query(YearResults.driver_name, db.func.sum(
            YearResults.points).label('total_points'))
        .filter(YearResults.race_number <= ranking, YearResults.year == year)
        .group_by(YearResults.driver_name)
        .order_by(db.func.sum(YearResults.points).desc())
        .offset(position - 1)
        .limit(1)
        .first()
    )
    if competitor:
        return competitor[0]
    return None


def positions_swaps_in_ranking(year, ranking):
    """
    Returns position changes between two consecutive rankings.

    Args:
        year (int): Season year
        ranking (int): Race number to analyze changes from

    Returns:
        list: List of tuples containing current position, driver name, and overtaken competitors
    """
    result = []
    competitors_number = num_competitors(year)
    for i in range(1, competitors_number):
        competitor_in_current_position = competitor_in_position_in_ranking(
            i, ranking, year)
        competitors_above_current_ranking = competitors_above(
            competitor_in_current_position, year, ranking)
        competitors_above_past_ranking = competitors_above(
            competitor_in_current_position, year, ranking - 1)
        if competitors_above_past_ranking:
            if set(competitors_above_current_ranking) != set(competitors_above_past_ranking):
                competitors_below_current_ranking = competitors_below(
                    competitor_in_current_position, year, ranking)
                overtaken_competitors = list(
                    set(competitors_above_past_ranking) & set(competitors_below_current_ranking))
                current_position = competitor_position_in_ranking(
                    competitor_in_current_position, year, ranking)
                if overtaken_competitors:
                    result.append(
                        (current_position, competitor_in_current_position, overtaken_competitors))
    return result


def positions_swaps_until_ranking(year, ranking):
    """
    Returns position changes up to a specific ranking.

    Args:
        year (int): Season year
        ranking (int): Race number to analyze changes up to

    Returns:
        list: List of position changes for each race up to the specified ranking
    """
    result = []
    for i in range(2, ranking+1):
        result.append(positions_swaps_in_ranking(year, i))
    return result
