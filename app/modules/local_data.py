"""
Functions to verify, retrieve and update data from an external SQLite database.
"""

import sqlite3

from sqlalchemy import inspect

from app import db
from app.models import YearResults


def verify_db(external_db):
    """
    Verifies if the tables in the external SQLite database match the tables in the internal Flask SQLAlchemy database.

    Args:
        external_db (str): The file path to the external SQLite database.

    Returns:
        bool: True if the tables in the external database match the tables in the internal database, False otherwise.
    """
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
    """
    Retrieve distinct seasons (years) from the external database.

    Args:
        external_db (str): The file path to the external SQLite database.

    Returns:
        list of tuple: A list of tuples, each containing a distinct year from the 'year_results' table.
    """
    conn_external = sqlite3.connect(external_db)
    cursor_external = conn_external.cursor()
    cursor_external.execute("SELECT DISTINCT year FROM year_results")
    seasons = cursor_external.fetchall()
    conn_external.close()
    return seasons


def update_db(external_db):
    """
    Updates the local database with data from an external SQLite database.

    Args:
        external_db (str): The file path to the external SQLite database.

    The function connects to the external database, retrieves all records from the 'year_results' table,
    and updates the local database accordingly. If a record with the same ID exists in the local database,
    it updates the existing record. If not, it creates a new record. Finally, it commits all changes to the database.
    """
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
