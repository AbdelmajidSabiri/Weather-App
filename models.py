from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class WeatherForecast(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      date = db.Column(db.DateTime, nullable=False)
      city = db.Column(db.String(100), nullable=False)
      temperature = db.Column(db.Float, nullable=False)
      precepitaion = db.Column(db.Float, nullable=False)
      wind_speed = db.Column(db.Float, nullable=False)
      cloud_cover = db.Column(db.Float, nullable=False)
      good_condition = db.Column(db.Boolean, default=False)
      bad_condition = db.Column(db.Boolean, default=False)
