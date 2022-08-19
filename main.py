import pickle
import os
import datetime
import random
import sys
from collections import namedtuple
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')

def myform():
    return render_template('index.html')



@app.route('/', methods=['POST'])
def home():
    def Create_Service(client_secret_file, api_name, api_version, *scopes):
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]

        cred = None
        working_dir = os.getcwd()
        token_dir = 'token files'

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

        ### Check if token dir exists first, if not, create the folder
        if not os.path.exists(os.path.join(working_dir, token_dir)):
            os.mkdir(os.path.join(working_dir, token_dir))

        if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
            with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            return service
        except Exception as e:
            os.remove(os.path.join(working_dir, token_dir, pickle_file))
            return None

    def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
        dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
        return dt

    CLIENT_SECRET_FILE = 'client_secret_168938097114-v224i9n4kadp91es4ht1ackk3njpfs6t.apps.googleusercontent.com.json'
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    ''
    # TO CREATE A CALENDAR

    # request_body = {
    #     'summary': 'Revision'
    # }
    #
    # response = service.calendars().insert(body=request_body).execute()
    # print(response)

    ''

    # TO DELETE A CALENDAR

    # service.calendars().delete(calendarId='l8sr8soehei20relr7a3tfngig@group.calendar.google.com').execute()

    hrRan = [8, 9, 10, 14, 17, 18, 19, 20]
    baseLstUser = []
    toBeAddedLst = []


    chapterName = request.form['chap-name']
    subjectName = request.form['sub-name']
    conceptName = request.form['con-name']
    isConceptIncluded = request.form['y-or-no']
    monthNum = int(request.form['month-name'])
    dayNum = int(request.form['day-name'])




    if isConceptIncluded == 'y':
        conceptChapter = f'{conceptName} from {chapterName} | {subjectName}'
    elif isConceptIncluded == 'n':
        conceptChapter = f'{chapterName} | {subjectName}'
    else:
        print('Please use smallcase "y" or "n".')
        sys.exit()

    baseLstUser.append(conceptChapter)

    # ------------------------------------------------------------------
    #
    #  CHANGE THE YEAR HERE||
    #                      VV
    #

    # ------------------------------------------------------------------
    #
    #
    # CHANGE THE YEAR HERE||
    #                     VV

    # ------------------------------------------------------------------
    # CHANGE THE YEAR HERE||
    #                     VV

    baseLstUser.append(2022)
    baseLstUser.append(monthNum)
    baseLstUser.append(dayNum)
    baseLstUser.append(random.choice(hrRan))
    baseLstUser.append(30)

    print(baseLstUser)

    def ttCreator(iteratingCheckpoint):
        lstnf = []
        if iteratingCheckpoint == 1:
            lstnf = baseLstUser.copy()
            lstnf[3] = lstnf[3] + 1
            if lstnf[3] > 28:
                lstnf[3] -= 28
                lstnf[2] += 1
            if lstnf[2] > 12:
                lstnf[2] -= 12
                lstnf[1] += 1
            # toBeAddedLst.append(lstnf)
            return lstnf
        elif 6 > iteratingCheckpoint > 1:
            lstnf = toBeAddedLst[-1].copy()
            lstnf[3] += 7
            if lstnf[3] > 28:
                lstnf[3] -= 28
                lstnf[2] += 1
            if lstnf[2] > 12:
                lstnf[2] -= 12
                lstnf[1] += 1
            # toBeAddedLst.append(lstnf)
            return lstnf
        elif iteratingCheckpoint > 5:
            lstnf = toBeAddedLst[-1].copy()
            lstnf[3] += 15
            if lstnf[3] > 28:
                lstnf[3] -= 28
                lstnf[2] += 1
            if lstnf[2] > 12:
                lstnf[2] -= 12
                lstnf[1] += 1
            # toBeAddedLst.append(lstnf)
            return lstnf

    iteratingCheckpoint = 0

    while iteratingCheckpoint < 40:
        iteratingCheckpoint += 1
        print(iteratingCheckpoint)
        resultFromFunc = ttCreator(iteratingCheckpoint)
        toBeAddedLst.append(resultFromFunc)

    for i in toBeAddedLst:
        calendar_id_revision = '7vdaah41ohga5n65n2546t4g4o@group.calendar.google.com'

        event_request_body = {
            'start': {
                'dateTime': convert_to_RFC_datetime(i[1], i[2], i[3], (i[4] - 6), i[5]),
            },
            'end': {
                'dateTime': convert_to_RFC_datetime(i[1], i[2], i[3], ((i[4] - 6) + 1), i[5]),
            },
            'summary': i[0],
            'status': 'confirmed',
            'colorId': 11
        }

        response = service.events().insert(
            calendarId=calendar_id_revision,
            maxAttendees=5,
            sendNotifications=True,
            body=event_request_body
        ).execute()
    print(toBeAddedLst)
    return toBeAddedLst



if __name__ == '__main__':
    app.run(debug=True)

















# ------------------------------------------------------------------------------------------------------------------------------


def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None



def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


CLIENT_SECRET_FILE = 'client_secret_168938097114-v224i9n4kadp91es4ht1ackk3njpfs6t.apps.googleusercontent.com.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
''
# TO CREATE A CALENDAR

# request_body = {
#     'summary': 'Revision'
# }
#
# response = service.calendars().insert(body=request_body).execute()
# print(response)

''

# TO DELETE A CALENDAR

# service.calendars().delete(calendarId='l8sr8soehei20relr7a3tfngig@group.calendar.google.com').execute()

hrRan = [8, 9, 10, 14, 17, 18, 19, 20]
baseLstUser = []
toBeAddedLst = []

print('Is concept included?')
isConceptIncluded = input('y/n: ')

if isConceptIncluded == 'y':
    conceptName = input('Concept name? ')
elif isConceptIncluded != 'n':
    print('Please use smallcase "y" or "n".')
    sys.exit()


chapterName = input('Chapter name? ')
subjectName = input('Subject name? ')
monthNum = int(input('Current month? '))
dayNum = int(input('Day of the month? '))




if isConceptIncluded == 'y':
    conceptChapter = f'{conceptName} from {chapterName} | {subjectName}'
elif isConceptIncluded == 'n':
    conceptChapter = f'{chapterName} | {subjectName}'
else:
    print('Please use smallcase "y" or "n".')
    sys.exit()


baseLstUser.append(conceptChapter)

# ------------------------------------------------------------------
#
#  CHANGE THE YEAR HERE||
#                      VV
#

# ------------------------------------------------------------------
#
#
# CHANGE THE YEAR HERE||
#                     VV

# ------------------------------------------------------------------
# CHANGE THE YEAR HERE||
#                     VV

baseLstUser.append(2022)
baseLstUser.append(monthNum)
baseLstUser.append(dayNum)
baseLstUser.append(random.choice(hrRan))
baseLstUser.append(30)

print(baseLstUser)


def ttCreator(iteratingCheckpoint):
    lstnf = []
    if iteratingCheckpoint == 1:
        lstnf = baseLstUser.copy()
        lstnf[3] = lstnf[3] + 1
        if lstnf[3] > 28:
            lstnf[3] -= 28
            lstnf[2] += 1
        if lstnf[2] > 12:
            lstnf[2] -= 12
            lstnf[1] += 1
        # toBeAddedLst.append(lstnf)
        return lstnf
    elif 6 > iteratingCheckpoint > 1:
        lstnf = toBeAddedLst[-1].copy()
        lstnf[3] += 7
        if lstnf[3] > 28:
            lstnf[3] -= 28
            lstnf[2] += 1
        if lstnf[2] > 12:
            lstnf[2] -= 12
            lstnf[1] += 1
        # toBeAddedLst.append(lstnf)
        return lstnf
    elif iteratingCheckpoint > 5:
        lstnf = toBeAddedLst[-1].copy()
        lstnf[3] += 15
        if lstnf[3] > 28:
            lstnf[3] -= 28
            lstnf[2] += 1
        if lstnf[2] > 12:
            lstnf[2] -= 12
            lstnf[1] += 1
        # toBeAddedLst.append(lstnf)
        return lstnf


iteratingCheckpoint = 0


while iteratingCheckpoint < 40:
    iteratingCheckpoint += 1
    print(iteratingCheckpoint)
    resultFromFunc = ttCreator(iteratingCheckpoint)
    toBeAddedLst.append(resultFromFunc)


for i in toBeAddedLst:
    calendar_id_revision = '7vdaah41ohga5n65n2546t4g4o@group.calendar.google.com'

    event_request_body = {
        'start': {
            'dateTime': convert_to_RFC_datetime(i[1], i[2], i[3], (i[4] - 6), i[5]),
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(i[1], i[2], i[3], ((i[4] - 6) + 1), i[5]),
        },
        'summary': i[0],
        'status': 'confirmed',
        'colorId': 11
    }

    response = service.events().insert(
        calendarId=calendar_id_revision,
        maxAttendees=5,
        sendNotifications=True,
        body=event_request_body
    ).execute()


print(toBeAddedLst)
