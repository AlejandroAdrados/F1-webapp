import sqlite3
from sqlalchemy import inspect
from f1_webapp.domain.models import YearResults
from f1_webapp import db

def verify_db(external_db):
    flask_inspector = inspect(db.engine)
    internal_db_tables = set(flask_inspector.get_table_names())
    conn = sqlite3.connect(external_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    conn.close()
    external_db_tables = set(nombre[0] for nombre in tablas)
    return internal_db_tables == external_db_tables


def get_seasons(external_db):
    conn_external = sqlite3.connect(external_db)
    cursor_external = conn_external.cursor()
    cursor_external.execute("SELECT DISTINCT year FROM year_results")
    seasons = cursor_external.fetchall()
    conn_external.close()
    return seasons


def update_db(external_db):
    conn_external = sqlite3.connect(external_db)
    cursor_external = conn_external.cursor()
    cursor_external.execute("SELECT * FROM year_results")
    results = cursor_external.fetchall()
    conn_external.close()
    for result in results:
        year_result = YearResults.query.filter_by(id=result[0]).first()
        if year_result:
            year_result.year = result[1]
            year_result.race_number = result[2]
            year_result.race_name = result[3]
            year_result.position = result[4]
            year_result.driver_name = result[5]
            year_result.team = result[6]
            year_result.points = result[7]
        else:
            year_result = YearResults(id=result[0], year=result[1], race_number=result[2], race_name=result[3], 
                                       position=result[4], driver_name=result[5], team=result[6], points=result[7])
            db.session.add(year_result)
    db.session.commit()
