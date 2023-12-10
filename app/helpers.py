from .models import YearResults
from . import db

def total_ranking(year, ranking):
    results = db.session.query(YearResults.driver_name, db.func.SUM(YearResults.points).label('total_points')) \
        .filter(YearResults.year == year, YearResults.race_number <= ranking) \
        .group_by(YearResults.driver_name) \
        .order_by(db.func.SUM(YearResults.points).desc()) \
        .all()
    serialized_results = [
        {'driver_name': row.driver_name, 'total_points': row.total_points}
        for row in results
    ]

    return serialized_results

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

def competitor_score_in_ranking(driver_name, year, race_number):
    result = db.session.query(db.func.sum(YearResults.points)).\
        filter(YearResults.driver_name == driver_name).\
        filter(YearResults.year == year).\
        filter(YearResults.race_number <= race_number).\
        scalar()
    return result

def competitor_position_in_ranking(driver_name, year, ranking):
    competitor_points = competitor_score_in_ranking(driver_name, year, ranking)

    subquery = db.session.query(YearResults.driver_name, db.func.sum(YearResults.points).label('total_points')).\
        filter(YearResults.race_number <= ranking).\
        filter(YearResults.year == year).\
        group_by(YearResults.driver_name).\
        having(db.func.sum(YearResults.points) > competitor_points).\
        order_by(db.func.sum(YearResults.points).desc()).subquery()

    count_position = db.session.query(db.func.count().label('position')).select_from(subquery).scalar() + 1

    return count_position

def competitor_position_history(driver_name, year, ranking):
    history = []
    i = 0
    for rank in range(1,ranking):
        i += 1
        history.append({'race' : i, 'position' : competitor_position_in_ranking(driver_name, year, rank)})
    return history

def competitors_list(year):
    # Realizar la consulta utilizando SQLAlchemy
    result = db.session.query(db.distinct(YearResults.driver_name)).filter(YearResults.year == year)
    serialized_result = [
        {'driver_name': row[0]}
        for row in result
    ]
    return serialized_result

def num_competitors(year):
    return len(competitors_list(year))