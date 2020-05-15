from __future__ import print_function
import sys
sys.path.insert(1, 'venv/Lib/site-packages')
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']


def check(mail_miem):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
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
                'client_secret_17576357117-4147f3o9s70bpcl9alltt1rh7a49ckg3.apps.googleusercontent.com(1).json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    results = service.users().list(customer='my_customer', maxResults=1,
                                orderBy='email', query='email:' + mail_miem).execute()

    users = results.get('users', [])
    if not users:
        return ''
    else:
        if 'Образовательные программы' in users[0]['orgUnitPath']:
            return mail_miem.replace('@miem', '@edu')
        return mail_miem.replace('@miem.', '@')


def check_by_name(name_miem):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """
    # print(name_miem)
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
                'client_secret_17576357117-4147f3o9s70bpcl9alltt1rh7a49ckg3.apps.googleusercontent.com(1).json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    results = service.users().list(customer='my_customer', maxResults=1,
                                orderBy='email', query='name:' + name_miem).execute()

    users = results.get('users', [])
    if not users:
        return ''
    elif len(users) == 1:
        if 'Образовательные программы' in users[0]['orgUnitPath']:
            return users[0]['emails'][0]['address'].replace('@miem', '@edu')
        return users[0]['emails'][0]['address'].replace('@miem.', '@')
    else:
        return '404'

# if __name__ == '__main__':
#     main()