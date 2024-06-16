from models import WeatherForecast, db
from datetime import datetime

def distance(V,W):
  d=0
  for i in range(len(V)):
    d=d+(V[i]-W[i])**2
  return d**(1/2)


def distanceRef(S):
    d=0
    cardS=len(S)
    for i in range(cardS):
        for j in range(cardS):
            d=d+distance(S[i],S[j])
    return d/((cardS-1)*cardS)


def cardSpp(S, Vt):
    dRef = distanceRef(S)
    Spp = []
    for V in S:
        if distance(V, Vt) < dRef:
            Spp.append(V)
    return len(Spp)


def propaVrai(S, Vt):
    return cardSpp(S, Vt) / len(S)

def retrieve_weather_data():

    forecasts = WeatherForecast.query.all()
    weather_data = []

    for forecast in forecasts:
        weather_vector = [forecast.temperature , forecast.wind_speed , forecast.precepitaion , forecast.cloud_cover , forecast.bad_condition , forecast.good_condition]
        weather_data.append(weather_vector)
    
    return weather_data


def calculate_probability(weather_data, Vt ,condition):

    weather_good = []
    weather_bad = []

    if condition == 'good':
        for vector in weather_data:
            if vector[-1] == True:
                weather_good.append(vector[:-2])
        probability_Good_weather = propaVrai(weather_good,Vt)
        return probability_Good_weather


    elif condition == 'bad':
        for vector in weather_data:
            if vector[-2] == True:
                weather_bad.append(vector[:-2])
        probability_Bad_weather = propaVrai(weather_bad,Vt)
        return probability_Bad_weather


