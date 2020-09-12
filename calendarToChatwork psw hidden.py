
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import  sys
import requests
# from datetime import datetime
# tmp = datetime.combine(datetime.now(), time.max)

clientID = "*****************"
clientSecret = "*****************"


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    last_today = datetime.datetime.today().max.isoformat() + 'Z'
    print('Let me check if you work at home today...')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = last_today,
                                        maxResults=1, singleEvents=True, q = "在宅").execute()
    events = events_result.get('items', [])

    if not events:
        print('You work at the office today.')
    else:
        print('You work at home today! I am goning to send a message to everyone.')

        APIKEY = '*****************'
        ROOMID = '*****************'
        #
        URLendpoint = 'https://api.chatwork.com/v2'
        # ----------------------------------------------------------------------------------
        # use \n to start a new line, type \t to indent --------------

        # str_out = "*テスト\n"
        str_out = "おはようございます！本日在宅にて勤務しております！"
        str_out += "\nよろしくお願いします！"

        # ----------------------------------------------------------------------------------
        url = URLendpoint + '/rooms/' + ROOMID + '/messages'
        headers = { 'X-ChatWorkToken': APIKEY }
        params = { 'body': str_out }

        resp = requests.post(url,
                            headers=headers,
                            params=params)

        print(resp.content)

        print('Alright, message has been sent.')




main()

