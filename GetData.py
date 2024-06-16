import requests
import json
from datetime import datetime
from flask import Flask , render_template 
from models import db, WeatherForecast


dateLyouma=datetime.today().strftime("%Y-%m-%d")

url="https://api.open-meteo.com/v1/forecast?"
url=url+"latitude=31,51&longitude=-9,77"
url=url+"&hourly=temperature_2m"
url=url+"&hourly=windspeed_10m"
url=url+"&hourly=cloud_cover"
url=url+"&hourly=precipitation"
url=url+"&daily=sunset"
url=url+"&daily=sunrise"
url=url+"&start_date="+dateLyouma
url=url+"&end_date="+dateLyouma



response=requests.get(url)
response=requests.get(url).content.decode('utf-8')
data = json.loads(response)

nomLyouma=datetime.today().strftime("%A")
jours={'Monday':'Lundi','Tuesday':'Mardi', 'Wednesday':'Mercredi',
'Thursday':'jeudi', 'Friday':'Vendredi', 'Saturday':'Samedi' , 'Sunday' : 'dimanche'}
lyouma1 = jours[nomLyouma]


def just3h(L) :
    L1 = []
    for i in range(0,len(L),3) :
        L1.append(L[i])
    return L1

DayTemperatures = data[0]["hourly"]["temperature_2m"]
DayWindspeed = data[0]["hourly"]["windspeed_10m"]
DayPrecipitation = data[0]["hourly"]["precipitation"]
Daycloud_cover = data[0]["hourly"]["cloud_cover"]
Daysunrise = int(data[0]["daily"]["sunrise"][0][11:13])
Daysunset = int(data[0]["daily"]["sunset"][0][11:13])

ListeTemperature = just3h(DayTemperatures)
ListePrecipitation = just3h(DayPrecipitation)
ListeCloud_cover = just3h(Daycloud_cover)
ListeTime = ["0:00" , "3:00" , "6:00" , "9:00" , "12:00" , "15:00" , "18:00" , "21:00"]
ListeHour = [0,3,6,9,12,15,18,21]


def daylight(T):
    if T > Daysunrise and T <= Daysunset :
        return True
    return False


def getImages(ListeHour, ListeCloud_cover, ListePrecipitation):
    listImages = []
    for i in range(8):
        if daylight(ListeHour[i]):
            if ListeCloud_cover[i] > 40:
                if ListePrecipitation[i] > 0:
                    listImages.append("sun with prece.png")
                else:
                    listImages.append("sun with could.png") 
            else :
                listImages.append("sun.png")

                    
        else:
            if ListeCloud_cover[i] > 40:
                if ListePrecipitation[i] > 0:
                    listImages.append("moon with prece.png")
                else :
                    listImages.append("moon with cloud.png")
                    
            else :
                listImages.append("MOON.png")

                
    return listImages

  
ListeImages = getImages(ListeHour, ListeCloud_cover, ListePrecipitation)                
current_Time = datetime.now().hour


DataMeteo = []
for i in range(8) :
    DataMeteo.append({"temps":ListeTime[i] ,"temperature":ListeTemperature[i],"precipitation": ListePrecipitation[i], "cloud": ListeCloud_cover[i], "wind": {"max" : max(DayWindspeed[0 + i*3] , DayWindspeed[1 + i*3] , DayWindspeed[2 + i*3]) , "min" : min(DayWindspeed[0 + i*3] , DayWindspeed[1 + i*3] , DayWindspeed[2 + i*3])}, "image":ListeImages[i] , "ListeH" : ListeHour[i]})

