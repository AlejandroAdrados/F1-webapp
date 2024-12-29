import pytest
from unittest.mock import MagicMock
from app import db

from app.modules.database import (
    total_ranking, get_info, get_races, competitor_score_in_ranking,
    competitor_team_in_year, competitor_position_in_ranking,
    competitor_position_history, competitors_list, num_competitors,
    competitors_below, competitors_above, competitor_in_position_in_ranking,
    positions_swaps_in_ranking, positions_swaps_until_ranking
)

@pytest.fixture
def mock_db_session():
    db.session = MagicMock()
    return db.session

def test_total_ranking(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = total_ranking(2021, 5)
    assert result == [
        {'driver_name': 'Driver1', 'team': 'Team1', 'total_points': 100},
        {'driver_name': 'Driver2', 'team': 'Team2', 'total_points': 90}
    ]

def test_get_info(mock_db_session):
    mock_db_session.query().group_by().all.return_value = [
        MagicMock(year=2021, max_num_race=10),
        MagicMock(year=2020, max_num_race=12)
    ]
    result = get_info()
    assert result == [
        {'year': 2021, 'races': 10},
        {'year': 2020, 'races': 12}
    ]

def test_get_races(mock_db_session):
    mock_db_session.query().filter().scalar.return_value = 10
    result = get_races(2021)
    assert result == 10

def test_competitor_score_in_ranking(mock_db_session):
    mock_db_session.query().filter().filter().filter().scalar.return_value = 50
    result = competitor_score_in_ranking('Driver1', 2021, 5)
    assert result == 50

def test_competitor_team_in_year(mock_db_session):
    mock_db_session.query().filter().filter().first.return_value = ['Team1']
    result = competitor_team_in_year('Driver1', 2021)
    assert result == 'Team1'

def test_competitor_position_in_ranking(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = competitor_position_in_ranking('Driver1', 2021, 5)
    assert result == 1

def test_competitor_position_history(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = competitor_position_history('Driver1', 2021, 5)
    assert result == [
        {'race': 1, 'position': 1},
        {'race': 2, 'position': 1},
        {'race': 3, 'position': 1},
        {'race': 4, 'position': 1},
        {'race': 5, 'position': 1}
    ]

def test_competitors_list(mock_db_session):
    mock_db_session.query().filter().order_by().all.return_value = [
        ('Driver1',),
        ('Driver2',)
    ]
    result = competitors_list(2021)
    assert result == ['Driver1', 'Driver2']

def test_num_competitors(mock_db_session):
    mock_db_session.query().filter().order_by().all.return_value = [
        ('Driver1',),
        ('Driver2',)
    ]
    result = num_competitors(2021)
    assert result == 2

def test_competitors_below(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = competitors_below('Driver1', 2021, 5)
    assert result == ['Driver2']

def test_competitors_above(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = competitors_above('Driver2', 2021, 5)
    assert result == ['Driver1']

def test_competitor_in_position_in_ranking(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().offset().limit().first.return_value = [
        'Driver1'
    ]
    result = competitor_in_position_in_ranking(1, 5, 2021)
    assert result == 'Driver1'

def test_positions_swaps_in_ranking(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = positions_swaps_in_ranking(2021, 5)
    assert result == []

def test_positions_swaps_until_ranking(mock_db_session):
    mock_db_session.query().filter().group_by().order_by().all.return_value = [
        MagicMock(driver_name='Driver1', team='Team1', total_points=100),
        MagicMock(driver_name='Driver2', team='Team2', total_points=90)
    ]
    result = positions_swaps_until_ranking(2021, 5)
    assert result == [[] for _ in range(2, 6)]
