from email.mime.text import MIMEText
import os
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import base64


scopes = ["https://mail.google.com/"]

def auth():
  global creds
  global service
  creds = None
  if (os.path.exists('token1.json')):
    print('good')
    creds = Credentials.from_authorized_user_file('token1.json', scopes)
    service = build('gmail', 'v1', credentials = creds)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("secrets.json", scopes)
      creds = flow.run_local_server(port = 0)
    with open('token1.json', 'w') as token:
      token.write(creds.to_json())


def send_mail(to, msg):
    global message
    global create_msg
    message = MIMEText(msg)
    message['To'] = to
    message['Subject'] = "Sent from Discord Bot"
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_msg = {'message': {
                  'raw': encoded_message
    }}
    
    send_gmail = service.users().messages().send(userId = 'me', body = {'raw': encoded_message}).execute()
    
    print('done!')

def send_details():
        draft = service.users().drafts().create(userId = 'me', body = create_msg).execute()
        return (f"Message: {draft['message']}\nID: {draft['id']}")





