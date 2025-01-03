import pytest
from unittest.mock import patch, MagicMock
from app import db
from app.models import YearResults
from bs4 import BeautifulSoup
from app.modules.web_data import (
    load_season,
    get_table_results_content,
    initialize_result,
    get_results,
    extract_info_from_row,
    add_result,
)

# Fixture para configurar el contexto Flask y la base de datos en memoria
@pytest.fixture(scope="module")
def test_client():
    from app import create_app
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def setup_db():
    db.session.begin_nested()
    yield
    db.session.rollback()

# Test para la función load_season
@pytest.mark.usefixtures("setup_db")
@patch("app.modules.web_data.requests.get")
def test_load_season(mock_get, test_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = """
    <table class="f1-table f1-table-with-data w-full">
        <tbody>
            <tr>
                <td class="p-normal whitespace-nowrap">Mock Race</td>
                <td><a href="mock-race">link</a></td>
            </tr>
        </tbody>
    </table>
    """
    mock_get.return_value = mock_response

    result = load_season(2023)
    assert result is True

# Test para get_table_results_content
@patch("app.modules.web_data.requests.get")
def test_get_table_results_content(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test</body></html>"
    mock_get.return_value = mock_response

    content = get_table_results_content("http://example.com")
    assert content is not None
    assert content.find("body").text == "Test"

# Test para initialize_result
@pytest.mark.usefixtures("setup_db")
def test_initialize_result(test_client):
    result = YearResults(
        year=2023,
        race_number=1,
        race_name="Mock Race",
        position=1,
        driver_name="Mock Driver",
        team="Mock Team",
        points=25,
    )
    db.session.add(result)
    db.session.commit()

    initialize_result(2023, 1)
    query_result = YearResults.query.filter_by(driver_name="Mock Driver").first()
    assert query_result is not None

# Test para get_results
@patch("app.modules.web_data.add_result")
def test_get_results(mock_add_result):
    mock_race_content = BeautifulSoup("""
    <table class="f1-table f1-table-with-data w-full">
        <tbody>
            <tr>
                <td>1</td>
                <td></td>
                <td>Mock Driversss</td>
                <td>Mock Team</td>
                <td></td>
                <td></td>
                <td>25</td>
            </tr>
        </tbody>
    </table>
    """, "html.parser")

    mock_sprint_content = BeautifulSoup("""
    <table class="f1-table f1-table-with-data w-full">
        <tbody>
            <tr>
                <td>1</td>
                <td></td>
                <td>Mock Driversss</td>
                <td>Mock Team</td>
                <td></td>
                <td></td>
                <td>5</td>
            </tr>
        </tbody>
    </table>
    """, "html.parser")

    race_info = {"year": 2023, "number": 1, "name": "Mock Race"}
    get_results(mock_race_content, mock_sprint_content, race_info)

    mock_add_result({'year': 2023, 'number': 1, 'name': 'Mock Race'},
                    {'position': '1', 'name': 'Mock Dri', 'team': 'Mock Team', 'points': '25'}, 30.0)

# Test para extract_info_from_row
def test_extract_info_from_row():
    mock_html = """
    <tr>
        <td>1</td>
        <td></td>
        <td>Mock Driversss</td>
        <td>Mock Team</td>
        <td></td>
        <td></td>
        <td>25</td>
    </tr>
    """
    row = BeautifulSoup(mock_html, "html.parser").find("tr")
    info = extract_info_from_row(row)

    assert info["position"] == "1"
    assert info["name"] == "Mock Driver"
    assert info["team"] == "Mock Team"
    assert info["points"] == "25"

# Test para add_result
@patch("app.modules.web_data.db")
def test_add_result(mock_db):
    race_info = {"year": 2023, "number": 1, "name": "Mock Race"}
    driver_info = {"position": 1, "name": "Mock Driver", "team": "Mock Team"}
    points = 25

    add_result(race_info, driver_info, points)
    expected_result = YearResults(
        year=2023,
        race_number=1,
        race_name="Mock Race",
        position=1,
        driver_name="Mock Driver",
        team="Mock Team",
        points=25,
    )
    mock_db.session.add.assert_called_once()
