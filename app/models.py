from . import db

class YearResults(db.Model):
    __tablename__ = 'year_results'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    race_number = db.Column(db.Integer)
    race_name = db.Column(db.String(100))
    position = db.Column(db.Integer)
    driver_name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    points = db.Column(db.Integer)