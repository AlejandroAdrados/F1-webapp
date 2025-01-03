import sqlite3
import pytest
from unittest.mock import patch

from app import create_app
from app.modules.local_data import get_seasons, verify_db, update_db

@pytest.fixture(scope='function')
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

def test_verify_db(setup_external_db):
    app = create_app()
    with app.app_context():
        external_db = setup_external_db
        assert verify_db(external_db) == True

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

@patch('app.modules.local_data.YearResults')
@patch('app.modules.local_data.db')
def test_update_db(mock_db, mock_YearResults, setup_external_db):
    external_db = setup_external_db
    def result(**kwargs):
        for key, value in kwargs.items():
            setattr(result, key, value)
        return result
    mocked_result = result(id=1, year=2020, race_number=1, race_name='Race 1', position=1, driver_name='Driver 1', team='Team 1', points=25)
    mock_YearResults.query.filter_by().first.side_effect = [mocked_result, None]
    mock_YearResults.reset_mock()
    
    app = create_app()
    with app.app_context():
        update_db(external_db)
        assert mock_db.session.commit.called
        assert mock_YearResults.query.filter_by.call_count == 2
        mock_YearResults.assert_called_once_with(id=2, year=2021, race_number=2, race_name='Race 2', position=2, driver_name='Driver 2', team='Team 2', points=18)
        mock_db.session.add.assert_called_once_with(mock_YearResults.return_value)
        
