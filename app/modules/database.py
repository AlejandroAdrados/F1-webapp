from ..models import YearResults
from .. import db


# Función que devuelve la clasificación de una ranking
def total_ranking(year, ranking):
    results = db.session.query(YearResults.driver_name, YearResults.team, db.func.SUM(YearResults.points).label('total_points')) \
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


# Función que devuelve el año y el número de temporadas que hay en la bbdd
def get_info():
    results = db.session.query(
        YearResults.year,
        db.func.max(YearResults.race_number).label('max_num_race')
    ).group_by(YearResults.year).all()
    serialized_results = [
        {'year': row.year, 'races': row.max_num_race}
        for row in results
    ]
    return serialized_results


# Función que devuelve el número de carrearas de un año
def get_races(year):
    result = db.session.query(db.func.max(YearResults.race_number)).filter(
        YearResults.year == year).scalar()
    return result


# Función que devuelve los puntos de un piloto en una ranking
def competitor_score_in_ranking(driver_name, year, race_number):
    result = db.session.query(db.func.sum(YearResults.points)).\
        filter(YearResults.driver_name == driver_name).\
        filter(YearResults.year == year).\
        filter(YearResults.race_number <= race_number).\
        scalar()
    if result:
        return result
    else:
        return 0


# Función que devuelve el equipo de un piloto en una temporada
def competitor_team_in_year(driver_name, year):
    result = db.session.query(YearResults.team).\
        filter(YearResults.driver_name == driver_name).\
        filter(YearResults.year == year).\
        first()
    if result:
        return result[0]
    else:
        return None


# Función que devuelve la posición de un piloto en una clasificación
def competitor_position_in_ranking(driver_name, year, ranking):
    results = total_ranking(year, ranking)
    sorted_results = sorted(
        results, key=lambda x: x['total_points'], reverse=True)
    position = next((i + 1 for i, result in enumerate(sorted_results)
                    if result['driver_name'] == driver_name), None)
    return position


# Función que devuelve el histórico de pilotos que ocupan una posición hasta una ranking
def competitor_position_history(driver_name, year, ranking):
    history = []
    i = 0
    for rank in range(1, ranking+1):
        i += 1
        history.append(
            {'race': i, 'position': competitor_position_in_ranking(driver_name, year, rank)})
    return history


# Función que devuelve la lista de pilotos de un año
def competitors_list(year):
    result = db.session.query(db.distinct(YearResults.driver_name)).filter(
        YearResults.year == year).order_by(YearResults.driver_name)
    serialized_result = [row[0] for row in result]
    return serialized_result


# Función que devuelve el número de pilotos de un año
def num_competitors(year):
    competitors = competitors_list(year)
    if competitors:
        return len(competitors)
    else:
        return 0


# Función que devuelve los pilotos por encima de un piloto en una ranking
def competitors_below(driver_name, year, ranking):
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    sorted_results = sorted(
        results, key=lambda x: x['total_points'], reverse=True)
    return [result['driver_name'] for result in sorted_results[position:]]


# Función que devuelve los pilotos por encima de un piloto en una ranking
def competitors_above(driver_name, year, ranking):
    results = total_ranking(year, ranking)
    position = competitor_position_in_ranking(driver_name, year, ranking)
    if position:
        sorted_results = sorted(
            results, key=lambda x: x['total_points'], reverse=True)
        return [result['driver_name'] for result in sorted_results[:position - 1]]
    else:
        return None


# Función que devuelve el piloto que ocupa una posición en una ranking
def competitor_in_position_in_ranking(position, ranking, year):
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
    else:
        return None


# Función que devuelve los cambios de posición entre dos rankings
def positions_swaps_in_ranking(year, ranking):
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


# Función que devuelve los cambios de posición hasta una ranking
def positions_swaps_until_ranking(year, ranking):
    result = []
    for i in range(2, ranking+1):
        result.append(positions_swaps_in_ranking(year, i))
    return result
