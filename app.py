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


@ app.route('/api/google/calendar/callback')
def google_calendar_callback():
    '''
    After user consent is provided, google provides state & code
    using which we have to get User credentials
    Steps:
    - Get state and code from query
    - Call on_auth_callback function using state and code
    - You can get users credentials using get_user_credentials function
    (You can store and reuse those credentials for calendar actions)
    '''
    state = request.args.get('state')
    code = request.args.get('code')
    client.on_auth_callback(state, code)
    user_google_auth_credentials = client.get_user_credentials()
    print('User Google Auth Creds', user_google_auth_credentials)
    resp = make_response(render_template('auth_success.html'))
    resp.set_cookie('is_calendar_connected', 'true')

    # Note: Storing creds in cookies for demonstration purpose only
    # You should keep it in some database
    resp.set_cookie('user_google_auth_credentials',
                    json.dumps(user_google_auth_credentials))
    return resp


if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=8000)
    app.run(host='0.0.0.0')
