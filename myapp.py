from flask import Flask
from models import db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Kgvo3539'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/tpFlask2/weather.db' 
    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    return app
