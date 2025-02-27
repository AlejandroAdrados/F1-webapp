"""
Functions to load and process Formula 1 web data
"""
import requests
from bs4 import BeautifulSoup
from ftfy import fix_text

from app import db
from app.models import YearResults


def load_season(year):
    """
    Loads the race data for a given Formula 1 season year from the official Formula 1 website.

    Args:
        year (int): The year of the Formula 1 season to load.

    Returns:
        bool: True if the data was successfully loaded and processed, False otherwise.
    """
    url = f'https://www.formula1.com/en/results/{year}'
    response = requests.get(f'{url}/races', timeout=10)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find(
            'table', {'class': 'f1-table f1-table-with-data w-full'}).find('tbody').find_all('tr')
        counter = 0
        for row in rows:
            counter += 1
            race_name = row.find('td', {'class': 'p-normal whitespace-nowrap'}).text.strip()
            race_url = row.find('a')['href']
            race_url = f'{url}/{race_url}'
            sprint_url = f'{race_url[:-12]}/sprint-results'
            existing_result = YearResults.query.filter_by(
                year=year, race_name=race_name).first()
            race_info = {"year": year, "number": counter, "name": race_name}

            if not existing_result:
                race_content = get_table_results_content(race_url)
                sprint_content = get_table_results_content(sprint_url)
                if not sprint_content.find('table', {'class': 'f1-table f1-table-with-data w-full'}):
                    sprint_content = None

                get_results(race_content, sprint_content, race_info)

        initialize_result(year, len(rows))
        if not existing_result:
            print(f"Year {year} races data added")
        else:
            print(f"Year {year} races data updated")
        db.session.commit()
        return True
    return False


def get_table_results_content(url):
    """
    Fetches and parses the HTML content of a table from the given URL.

    Args:
        url (str): The URL of the web page to fetch the table content from.

    Returns:
        BeautifulSoup: Parsed HTML content of the table if the request is successful.
        None: If the request fails (status code is not 200).
    """
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, 'html.parser')
    return None


def add_sprint_points(driver, race, points):
    """
    Adds sprint points to a driver's result for a specific race.

    Args:
        driver (str): The name of the driver.
        race (str): The name of the race.
        points (int): The number of points to add.

    Returns:
        None
    """
    result = YearResults.query.filter_by(
        driver_name=driver, race_name=race).first()
    if result:
        result.points += points


def initialize_result(year, ranking):
    """
    Initializes the race results for a given year and ranking.

    This function queries the database for driver names and their respective teams
    for a specific year and up to a certain ranking. It then initializes race information
    and adds the result for each driver.

    Args:
        year (int): The year for which the race results are being initialized.
        ranking (int): The ranking up to which the race results are considered.

    Returns:
        The result of adding the race information and driver information to the database.
    """
    results = (
        db.session.query(YearResults.driver_name, YearResults.team)
        .filter(YearResults.year == year, YearResults.race_number <= ranking)
        .distinct()
        .all()
    )
    race_info = {"year": year, "number": 0, "name": " "}
    for driver, team in results:
        driver_info = {"position": 1, "name": driver,
                       "team": team, "points": 0}
        return add_result(race_info, driver_info, 0)


def get_results(race_content, sprint_content, race_info):
    """
    Extracts race and sprint results, calculates total points for each driver, and adds the results to race_info.

    Args:
        race_content (BeautifulSoup): Parsed HTML content of the race results page.
        sprint_content (BeautifulSoup): Parsed HTML content of the sprint results page (can be None).
        race_info (dict): Dictionary to store the results of the race.

    Returns:
        None
    """
    table_ref = {'class': 'f1-table f1-table-with-data w-full'}
    table_race = race_content.find('table', table_ref)
    if table_race:
        race_rows = table_race.find('tbody').find_all('tr')
        for race_row in race_rows:
            driver_info = extract_info_from_row(race_row)
            points = float(driver_info.get("points"))
            if sprint_content:
                sprint_table = sprint_content.find('table', table_ref)
                if sprint_table:
                    sprint_rows = sprint_table.find('tbody').find_all('tr')
                    for row_sprint in sprint_rows:
                        driver_sprint_info = extract_info_from_row(row_sprint)
                        if driver_info.get("name") == driver_sprint_info.get("name"):
                            points += int(driver_sprint_info.get("points"))
                            break
            add_result(race_info, driver_info, points)


def extract_info_from_row(row):
    """
    Extracts information from a table row element.

    Args:
        row (bs4.element.Tag): A BeautifulSoup Tag object representing a table row.

    Returns:
        dict: A dictionary containing the extracted information with keys:
            - "position" (str): The position of the driver.
            - "name" (str): The name of the driver.
            - "team" (str): The team of the driver.
            - "points" (str): The points scored by the driver.
    """
    cells = row.find_all('td')
    position = cells[0].text.strip()
    driver_name = cells[2].text.strip().replace('\n', ' ')[:-3]
    driver_name = fix_text(driver_name)
    team = cells[3].text.strip()
    points = cells[6].text.strip()
    return {"position": position, "name": driver_name, "team": team, "points": points}


def add_result(race_info, driver_info, points):
    """
    Adds a new race result to the database.

    Args:
        race_info (dict): A dictionary containing race information with keys "year", "number", and "name".
        driver_info (dict): A dictionary containing driver information with keys "position", "name", and "team".
        points (int): The number of points the driver earned in the race.

    Returns:
        None
    """
    new_result = YearResults(
        year=race_info.get("year"),
        race_number=race_info.get("number"),
        race_name=race_info.get("name"),
        position=driver_info.get("position"),
        driver_name=driver_info.get("name"),
        team=driver_info.get("team"),
        points=points
    )
    return db.session.add(new_result)
