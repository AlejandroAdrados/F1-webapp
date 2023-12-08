from . import db  # Suponiendo que db es la instancia de SQLAlchemy creada en __init__.py

class YearResults(db.Model):
    __tablename__ = 'year_results'  # Asegúrate de especificar el nombre de la tabla si no está definido

    # Define las columnas de la tabla, asegúrate de agregar extend_existing=True
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    race_number = db.Column(db.Integer)
    race_name = db.Column(db.String(100))
    position = db.Column(db.Integer)
    driver_name = db.Column(db.String(100))
    team = db.Column(db.String(100))
    points = db.Column(db.Integer)