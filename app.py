from flask import Flask, render_template, redirect, url_for, request
from keys import weather_key, city, state, cal_key
from gcalendar import Gcalendar
from weather import Weather
from datetime import date


# Weather
my_weather = Weather()
get_weather = my_weather.get_data(weather_key, city, state)

# Events
my_cal = Gcalendar()
get_events = tuple()
get_events1 = tuple()
get_events2 = tuple()
print(f'### get_events intial len = {len(get_events)}')
for cal_key_item in cal_key:
    get_events1 = my_cal.gcal_connect(cal_key_item)
    if type(get_events1) != type('str'):
        get_events2 = get_events2 + get_events1
    get_events1 = tuple()

event_list = []
for item in get_events2:
    if item not in event_list:
        event_list.append(item)
get_events = tuple(event_list)


# Today's date for header


def today_date():
    today = date.today()
    weekday = today.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March',
              'April', 'May', 'June',
              'July', 'August', 'September',
              'October', 'November', 'December']
    return str(days[weekday] + ', ' + months[today.month - 1] + ' ' + str(today.day))


app = Flask(__name__)


@ app.route('/')
def index():
    return render_template('index.html', date=today_date(), weather=get_weather, events=get_events)


if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=8000)
    app.run(host='0.0.0.0')
