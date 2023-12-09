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