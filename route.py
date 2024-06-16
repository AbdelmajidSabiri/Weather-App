from flask import Flask, request, redirect, render_template,url_for
import GetData
import datetime
from myapp import create_app
from models import WeatherForecast , db
import CalculProba

app=create_app()

@app.route("/")
def meteo():
    date = GetData.dateLyouma
    jour = GetData.lyouma1
    DataMeteo = GetData.DataMeteo
    current = GetData.current_Time
    probabilities = {}

    for i in range(8) :
        add_forecast(i)

    date = datetime.datetime.now().date() 
    difference =  (date - datetime.date(2024, 5, 12)).days
    all_forecasts = CalculProba.retrieve_weather_data()
    
    for id in range(8) :
        forecast_id = (id+1) + difference * 8
        forecast = WeatherForecast.query.get_or_404(forecast_id)
        weather_vector = [forecast.temperature , forecast.wind_speed , forecast.precepitaion , forecast.cloud_cover , forecast.bad_condition , forecast.good_condition]

        forecast_proba_good = CalculProba.calculate_probability(all_forecasts, weather_vector, condition='good')
        forecast_proba_bad = CalculProba.calculate_probability(all_forecasts, weather_vector, condition='bad') 

        probabilities[id] = {
            'bad_proba': forecast_proba_bad,
            'good_proba': forecast_proba_good
        }


    return render_template('meteo.html', DataMeteo=DataMeteo, date=date, jour=jour , current = current , probabilities = probabilities)


@app.route('/forecasts')
def forecasts():
    forecasts = WeatherForecast.query.all()
    return render_template('forecasts.html', forecasts=forecasts)



@app.route('/good_condition/<int:id>', methods=['POST'])
def good_condition(id):

    date = datetime.datetime.now().date()
    difference =  (date - datetime.date(2024, 5, 12)).days
    
    forecast_id = (id+1) + difference * 8
    forecast = WeatherForecast.query.get_or_404(forecast_id)
    forecast.good_condition = True
    db.session.commit()
    return redirect(url_for('forecasts'))
    

@app.route('/bad_condition/<int:id>', methods=['POST'])
def bad_condition(id):

    date = datetime.datetime.now().date()
    start_date = datetime.date(2024, 5, 12)
    difference = (date - start_date).days

    forecast_id = (id+1) + difference * 8
    forecast = WeatherForecast.query.get_or_404(forecast_id)
    forecast.bad_condition = True
    db.session.commit()
    return redirect(url_for('forecasts'))


def add_forecast(id):
    date = datetime.datetime.strptime(GetData.dateLyouma, '%Y-%m-%d')
    date += datetime.timedelta(hours=id*3)
    existing_forecast = WeatherForecast.query.filter_by(date=date , city="Essaouira").first()

    if existing_forecast:
        pass
    else:
        forecast = WeatherForecast(
            date=date,
            city="Essaouira",
            temperature=GetData.DataMeteo[id]['temperature'],
            precepitaion=GetData.DataMeteo[id]['precipitation'],
            wind_speed=(int(GetData.DataMeteo[id]['wind']["min"]) + int(GetData.DataMeteo[id]['wind']["max"]))/2,
            cloud_cover=GetData.DataMeteo[id]['cloud'],
        )
        db.session.add(forecast)
        db.session.commit()
