
import datetime
import os.path

import threading

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Calendar(threading.Thread):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = "cred.json"
    NOW = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    creds = None
    calendarList =None
    """ Класс который будет работать с гугл календарем, асинхронный"""
    def __init__(self):
        
        """Если нет токена, будет первая авторизация, и добавиться файл токена"""
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'cred.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())
            
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
        except HttpError as error:
            print('An error occurred: %s' % error)



    def get_events(self):
        events_result = self.service.events().list(calendarId='primary', timeMin=self.NOW,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        for event in events:
              start = event['start'].get('dateTime', event['start'].get('date'))
              print(start, event['summary'])
              
    def add_events(self,dateStart,dataEnd,description:str = None ):
      
        event={
            "summary":f"{description}",
             'start': {
                  'dateTime': f'{dateStart}',
                  
                },
              'end': {
                  'dateTime':f'{dataEnd}',
                 
                },    
        }
        
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        # print ('Event created: %s' % (event.get('htmlLink')))







if __name__ =="__main__":
    cl = Calendar()
    