from __future__ import print_function

import os.path
from email.message import EmailMessage
import ssl
import smtplib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sqlite3
import datetime;

def create_table_email_sent():
    con = sqlite3.connect("mysqlite3.db")
    cur = con.cursor()
    sql = "create table IF NOT EXISTS email_sent(email, dtime)"
    cur.execute(sql)
    con.close()

def get_email_sent_info(email):
    con = sqlite3.connect("mysqlite3.db")
    cur = con.cursor()
    sql = "select email, dtime from email_sent where email = '" + email + "'";
    res = cur.execute(sql)
    ans = res.fetchone()
    # print(res.fetchall())
    con.close()
    return ans

def delete_email_sent_info(email):
    con = sqlite3.connect("mysqlite3.db")
    cur = con.cursor()
    sql = "delete from email_sent where email = '" + email + "'";
    res = cur.execute(sql)
    ans = res.fetchone()
    con.commit()
    sql = "select email, dtime from email_sent where email = '" + email + "'";
    res = cur.execute(sql)
    ans = res.fetchall()
    # print(ans)
    con.close()
    return ans

def record_email_sent(email):
    con = sqlite3.connect("mysqlite3.db")
    cur = con.cursor()

    res = get_email_sent_info(email)
    if res is not None:
        return res

    # ct stores current time
    ct = datetime.datetime.now()
    ct_str = ct.strftime("%m/%d/%Y, %H:%M:%S")

    sql = "insert into email_sent values ('" + email + "', '" + ct_str + "')"
    res = cur.execute(sql)

    con.commit()

    sql = "select email, dtime from email_sent where email = '" + email + "'";
    res = cur.execute(sql)
    ans = res.fetchone()
    con.close()
    return ans

zoomlink = {
        'Reentry' :  'zoom link1',
        'Psychiatric hospitalization experience' :  'zoom link2',
        'Military Veteran' :  'zoom link3',
        'LGBTQ+' :  'zoom link4',
        'Age 18-24' :  'zoom link5',
        'Age 55+' :  'zoom link6',
        'Disabled' :  'zoom link7',
        'Decline to State' :  ' '
}

def email_send(row):
    email_receiver = row[1]

    email_sender = '?????????????/@gmail.com'
    email_password = '???????????/'

    subject = "Connection 1"

    body = """
    Hello,
    
    Thank you for registering. Here is the zoom link:

    """
            # Print columns A and E, which correspond to indices 0 and 4.
            
    groups=row[5].split(', ')
    for g in groups:
        body += "\t" + g + ": "
        body += zoomlink[g]
        body += "\n"
        # print(g, " => ", zoomlink[g])

    print(body)
    # if testing, add return line of code so it doesn't send an email
    # return

    em = EmailMessage()
    em['From'] = email_sender
    em['To']= email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1JX???????????????????????uHI0E'
SAMPLE_RANGE_NAME = 'Form Responses 1'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print(SAMPLE_RANGE_NAME)
        values.pop(0)
        for row in values:
            email_send(row)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()