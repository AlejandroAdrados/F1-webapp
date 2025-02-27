"""
File contains the model for the year_results table
"""

from . import db


class YearResults(db.Model):
    """
    Represents the results of a Formula 1 race for a specific year.

    Attributes:
        id (int): The primary key for the record.
        year (int): The year of the race.
        race_number (int): The number of the race in the season.
        race_name (str): The name of the race.
        position (int): The finishing position of the driver.
        driver_name (str): The name of the driver.
        team (str): The name of the team.
        points (int): The points awarded to the driver for this race.
    """
    __tablename__ = 'year_results'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    race_number = db.Column(db.Integer)
    race_name = db.Column(db.String(100))
    position = db.Column(db.Integer)
    driver_name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    points = db.Column(db.Integer)
