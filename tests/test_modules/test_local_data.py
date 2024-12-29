import sqlite3
import pytest
from app.modules.local_data import get_seasons

@pytest.fixture
def setup_external_db(tmp_path):
    db_path = tmp_path / "test_external.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE year_results (id INTEGER PRIMARY KEY, year INTEGER, race_number INTEGER, race_name TEXT, position INTEGER, driver_name TEXT, team TEXT, points INTEGER)")
    cursor.execute("INSERT INTO year_results (year, race_number, race_name, position, driver_name, team, points) VALUES (2020, 1, 'Race 1', 1, 'Driver 1', 'Team 1', 25)")
    cursor.execute("INSERT INTO year_results (year, race_number, race_name, position, driver_name, team, points) VALUES (2021, 2, 'Race 2', 2, 'Driver 2', 'Team 2', 18)")
    conn.commit()
    conn.close()
    return db_path

def test_get_seasons(setup_external_db):
    external_db = setup_external_db
    seasons = get_seasons(external_db)
    assert seasons == [(2020,), (2021,)]

def test_get_seasons_empty_db(tmp_path):
    db_path = tmp_path / "empty_test_external.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE year_results (id INTEGER PRIMARY KEY, year INTEGER, race_number INTEGER, race_name TEXT, position INTEGER, driver_name TEXT, team TEXT, points INTEGER)")
    conn.commit()
    conn.close()
    seasons = get_seasons(db_path)
    assert seasons == []
    