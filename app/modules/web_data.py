from bs4 import BeautifulSoup
from ftfy import fix_text
import requests
from app.models import YearResults
from app import db


def load_season(year):
    url = f'https://www.formula1.com/en/results/{year}'
    response = requests.get(f'{url}/races')
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
    else:
        return False


def get_table_results_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, 'html.parser')
    return None


def add_sprint_points(driver, race, points):
    result = YearResults.query.filter_by(
        driver_name=driver, race_name=race).first()
    if result:
        result.points += points


def initialize_result(year, ranking):
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
    cells = row.find_all('td')
    position = cells[0].text.strip()
    driver_name = cells[2].text.strip().replace('\n', ' ')[:-3]
    driver_name = fix_text(driver_name)
    team = cells[3].text.strip()
    points = cells[6].text.strip()
    return {"position": position, "name": driver_name, "team": team, "points": points}


def add_result(race_info, driver_info, points):
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
