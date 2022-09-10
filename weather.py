from keys import weather_key, state, city
from datetime import date, datetime, timedelta, time
import requests


class Weather():
    def __init__(self):
        self.today = []
        #self.tomorrow = {}
        #self.day_p2 = {}
        #self.day_p3 = {}
        self.date = date.today()
        self.time = time(15, 0, 0, 0)
        self.URIstart = 'http://openweathermap.org/img/wn/'
        self.URIend = '@2x.png'

    def get_data(self, key, city, state):
        resp = requests.get(
            f'https://api.openweathermap.org/data/3.0/onecall?lat=51.781634&lon=-2.200388&exclude=current,minutely,alerts&units=metric&appid={key}')
        return self.organize_data(resp.json()['daily'])

    def organize_data(self, data):
        for data_point in data:
            date = datetime.fromtimestamp(data_point['dt']).date()
            time = datetime.fromtimestamp(data_point['dt']).time()
            diffdate = date - self.date
            diffdate = diffdate.days
            self.today.append(
                dict(
                    temp=round(data_point['temp']['day'], 1),
                    weather=data_point["weather"][0]["main"],
                    icon=self.URIstart +
                    data_point['weather'][0]['icon']+self.URIend,
                    precipprob=round(data_point['pop']*100),
                    uvi=round(data_point['uvi'], 1),
                    date=date,
                    day=date.strftime('%A'),
                    diffday=diffdate
                )
            )

        return self.today


if __name__ == "__main__":
    weather = Weather()
    print(weather.get_data(weather_key, city, state))
