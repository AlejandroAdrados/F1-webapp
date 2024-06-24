from bs4 import BeautifulSoup
from ftfy import fix_text
import requests
from f1_webapp.domain.models import YearResults
from f1_webapp import db


def load_season(year):
    url = f'https://www.formula1.com/en/results.html/{year}/races.html'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find(
            'table', {'class': 'resultsarchive-table'}).find('tbody').find_all('tr')
        counter = 0
        for row in rows:
            counter += 1
            race_name = row.find('td', {'class': 'dark bold'}).text.strip()
            race_url = row.find('a')['href']
            race_url = f'https://www.formula1.com{race_url}'
            sprint_url = f'{race_url[:-16]}sprint-results.html'
            existing_result = YearResults.query.filter_by(
                year=year, race_name=race_name).first()
            race_info = {"year": year, "number": counter, "name": race_name}
            response_race = requests.get(race_url)

            if not existing_result:
                if response_race.status_code == 200:
                    html_race = response_race.text
                    race_content = BeautifulSoup(html_race, 'html.parser')
                    sprint_content = is_sprint_race(sprint_url)
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


def is_sprint_race(url):
    response_sprint = requests.get(url)
    if response_sprint.status_code == 200:
        html_sprint = response_sprint.text
        soup_sprint = BeautifulSoup(html_sprint, 'html.parser')
        ul_tag = soup_sprint.find('ul', class_='resultsarchive-side-nav')
        if ul_tag:
            list_items = ul_tag.find_all('li', class_='side-nav-item')
            for item in list_items:
                if "sprint" in item.get_text().lower():
                    return soup_sprint
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
    table_race = race_content.find('table', {'class': 'resultsarchive-table'})
    if table_race:
        race_rows = table_race.find('tbody').find_all('tr')
        for race_row in race_rows:
            driver_info = extract_info_from_row(race_row)
            points = float(driver_info.get("points"))
            if sprint_content:
                sprint_table = sprint_content.find(
                    'table', {'class': 'resultsarchive-table'})
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
    position = cells[1].text.strip()
    driver_name = cells[3].text.strip().replace('\n', ' ')[:-4]
    driver_name = fix_text(driver_name)
    team = cells[4].text.strip()
    points = cells[7].text.strip()
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
