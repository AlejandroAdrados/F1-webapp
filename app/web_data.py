from bs4 import BeautifulSoup
import requests
from .models import YearResults
from . import db

def load_data():
    for year in range(2020, 2024):
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

                response = requests.get(race_url)

                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table', {'class': 'resultsarchive-table'})

                    if table:
                        rows = table.find('tbody').find_all('tr')

                        for row in rows:
                            cells = row.find_all('td')

                            position = cells[1].text.strip()
                            driver_name = cells[3].text.strip().replace('\n', ' ')[:-4]
                            team = cells[4].text.strip()
                            points = cells[7].text.strip()

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

            print(f"Year {year} races data added")
        else:
            print(f'Error fetching page. Status code: {response.status_code}')

    db.session.commit()
