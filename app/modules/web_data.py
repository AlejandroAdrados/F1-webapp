from bs4 import BeautifulSoup
import requests
from ..models import YearResults
from .. import db

def load_data(year1, year2):
    for year in range(year1, year2+1):
        url = f'https://www.formula1.com/en/results.html/{year}/races.html'

        response = requests.get(url)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            rows = soup.find('table', {'class': 'resultsarchive-table'}).find('tbody').find_all('tr')

            counter = 0

            for row in rows:
                counter += 1
                race_name = row.find('td', {'class': 'dark bold'}).text.strip()
                race_url = row.find('a')['href']
                race_url = f'https://www.formula1.com{race_url}'
                sprint_url = f'{race_url[:-16]}sprint-results.html'
                existing_result = YearResults.query.filter_by(year=year, race_name=race_name).first()

                response_race = requests.get(race_url)
                response_sprint = requests.get(sprint_url)
                if not existing_result: 
                    if response_race.status_code == 200 and response_sprint.status_code == 200:
                        html_race = response_race.text
                        soup_race = BeautifulSoup(html_race, 'html.parser')
                        table_race = soup_race.find('table', {'class': 'resultsarchive-table'})
                        html_sprint = response_sprint.text
                        soup_sprint = BeautifulSoup(html_sprint, 'html.parser')
                        ul_tag = soup_sprint.find('ul', class_='resultsarchive-side-nav')
                        is_sprint = False
                        if ul_tag:
                            list_items = ul_tag.find_all('li', class_='side-nav-item')
                            for item in list_items:
                                if "sprint" in item.get_text().lower():
                                    is_sprint = True
                                    break
                        if table_race:
                            rows_table = table_race.find('tbody').find_all('tr')
                            for row_race in rows_table:
                                cells = row_race.find_all('td')
                                position = cells[1].text.strip()
                                driver_name = cells[3].text.strip().replace('\n', ' ')[:-4]
                                team = cells[4].text.strip()
                                points = cells[7].text.strip()
                                if is_sprint:
                                    sprint_table = soup_sprint.find('table', {'class': 'resultsarchive-table'})
                                    if sprint_table:
                                        sprint_rows = sprint_table.find('tbody').find_all('tr')
                                        for row_sprint in sprint_rows:
                                            cells_sprint = row_sprint.find_all('td')
                                            driver_name_sprint = cells_sprint[3].text.strip().replace('\n', ' ')[:-4]
                                            points_sprint = cells_sprint[7].text.strip()
                                            if driver_name == driver_name_sprint:
                                                points = int(points) + int(points_sprint)
                                                break
                                new_result = YearResults(
                                    year=year,
                                    race_number=counter,
                                    race_name=race_name,
                                    position=position,
                                    driver_name=driver_name,
                                    team=team,
                                    points=points
                                )
                                db.session.add(new_result)
            if not existing_result:
                print(f"Year {year} races data added")
            else:
                print(f"Year {year} races data updated")
        else:
            print(f'Error fetching page. Status code: {response.status_code}')

    db.session.commit()

def add_sprint_points(driver, race, points):
    result = YearResults.query.filter_by(driver_name=driver, race_name=race).first()
    if result:
        result.points += points
