from flask import Flask, render_template, redirect, url_for, request
from keys import weather_key, city, state, cal_key
from gcalendar import Gcalendar
from weather import Weather
from datetime import date
from oauth import Oauth
import pickle


OAUTH_API_SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly']
OAUTH_CREDENTIALS_PATH = './credentials.json'
APP_BASE_URL = 'http://cal.the-etheridges.com:5000'


client = Oauth(
    credentials_path=OAUTH_CREDENTIALS_PATH,
    scopes=OAUTH_API_SCOPES
)

callback_url = '{}/api/google/calendar/callback'.format(
    APP_BASE_URL)
oauth_consent_url = client.get_authorization_url(
    redirect_uri=callback_url)
redirect(oauth_consent_url)
print("oauth consent url is :", oauth_consent_url)

# Weather
my_weather = Weather()
get_weather = my_weather.get_data(weather_key, city, state)

# Events
my_cal = Gcalendar(client)
get_events = tuple()
get_events1 = tuple()
get_events2 = tuple()
print(f'### get_events intial len = {len(get_events)}')
for cal_key_item in cal_key:
    get_events1 = my_cal.gcal_connect(
        cal_key_item)
    # if type(get_events1) != type('str'):
    #    get_events2 = get_events2 + get_events1
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


@ app.route('/api/google/calendar/connect')
def connect_google_calendar():
    '''
    First step is to get users consent for using calendar APIs
    Steps:
    - Get Consent Url 
    - Redirect with callback url 
    (Callback APP api url Eg. https://example.com/api/google/calendar/callback )
    '''
    print('## app.py  in connect_google_calendar')
    callback_url = '{}/api/google/calendar/callback'.format(
        APP_BASE_URL)
    print('### callback_url      :', callback_url)
    oauth_consent_url = client.get_authorization_url(redirect_uri=callback_url)
    print('### oauth_consent_url :', oauth_consent_url)
    return redirect(oauth_consent_url)


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
    print('# app.py def google_calendar_callback')
    state = request.args.get('state')
    print('## state:', state)
    code = request.args.get('code')
    print('## code :', code)
    print('\n')
    print('## Calling client.on_auth_callback from app.py google_calendar_callback')
    client.on_auth_callback(state, code)
    print('## Calling client.get_user_credentials from app.py google_calendar_callback')
    user_google_auth_credentials = client.get_user_credentials()
    with open('token.pickle', 'wb') as token:
        pickle.dump(user_google_auth_credentials, token)
    print('User Google Auth Creds', user_google_auth_credentials)
    print('\n')
    #resp = make_response(render_template('auth_success.html'))
    #resp.set_cookie('is_calendar_connected', 'true')

    # Note: Storing creds in cookies for demonstration purpose only
    # You should keep it in some database
    #resp.set_cookie('user_google_auth_credentials',
    #               json.dumps(user_google_auth_credentials))
    return True


if __name__ == '__main__':
    #app.run(debug=True, host='127.0.0.1', port=8000)
    app.run(host='0.0.0.0')
