from __future__ import print_function
# specific calendar id
#from keys import cal_key
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth import Oauth


class Gcalendar:
    def __init__(self):
        self.events = []

    def gcal_connect(self, cal_key):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 2 events on the user's calendar.
        """

        # If modifying these scopes, delete the file token.pickle.
        OAUTH_API_SCOPES = [
            'https://www.googleapis.com/auth/calendar.readonly']
        OAUTH_CREDENTIALS_PATH = '.credentials.json'

        client = Oauth(
            credentials_path=OAUTH_CREDENTIALS_PATH,
            scopes=OAUTH_API_SCOPES
        )

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                callback_url = '{}/api/google/calendar/callback'.format(
                    settings.APP_BASE_URL)
                oauth_consent_url = client.get_authorization_url(
                    redirect_uri=callback_url)
                print("oauth consent url is :", oauth_consent_url)
                response = input("Press any key when authised")

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
        return None


'''
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now()  # .isoformat()  # + 'Z'  # 'Z' indicates UTC time
        today = datetime.datetime(now.year, now.month, now.day)
        tomorrow = today + datetime.timedelta(days=1)
        now = now.isoformat()
        today = today.isoformat() + 'Z'
        tomorrow = tomorrow.isoformat() + 'Z'

        events_result = service.events().list(calendarId=cal_key, timeMin=today,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'
        return self.set_data(events, cal_key)
'''

'''WAS WORKING LOCALLY WITH DESKTOP API KEY
    def gcal_connect(self, cal_key):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 2 events on the user's calendar.
        """

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now()  # .isoformat()  # + 'Z'  # 'Z' indicates UTC time
        today = datetime.datetime(now.year, now.month, now.day)
        tomorrow = today + datetime.timedelta(days=1)
        now = now.isoformat()
        today = today.isoformat() + 'Z'
        tomorrow = tomorrow.isoformat() + 'Z'

        events_result = service.events().list(calendarId=cal_key, timeMin=today,
                                              maxResults=100, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'
        return self.set_data(events, cal_key)
'''


def set_data(self, events, cal_key):
     now = datetime.datetime.now()  # .isoformat()  # + 'Z'  # 'Z' indicates UTC time
      today = datetime.datetime(now.year, now.month, now.day)
       for event in events:
            start1 = event['start'].get('dateTime', event['start'].get('date'))
            if len(start1) == 10:
                start1 = start1 + 'T00:00:00'
            start = datetime.datetime.strptime(start1[0:10], '%Y-%m-%d')
            end1 = event['end'].get('dateTime', event['end'].get('date'))
            if len(end1) == 10:
                end1 = end1 + 'T00:00:00'
            end = datetime.datetime.strptime(end1[0:10], '%Y-%m-%d')
            startdiff = start - today
            enddiff = end - today

            self.events.append(
                dict(
                    summary=event['summary'],
                    start=event['start'].get(
                        'dateTime', event['start'].get('date')),
                    starttime=datetime.datetime.strptime(
                        start1[11:19], '%H:%M:%S').strftime('%H:%M'),
                    end=event['end'].get(
                        'dateTime', event['end'].get('date')),
                    endtime=datetime.datetime.strptime(
                        end1[11:19], '%H:%M:%S').strftime('%H:%M'),
                    location=event['location'] if 'location' in event.keys(
                    ) else '',
                    startsindays=startdiff.days,
                    endsindays=enddiff.days,
                    cal=cal_key
                )
            )
        return tuple(self.events)


if __name__ == '__main__':
    cal = Gcalendar()
    print(cal.gcal_connect())
