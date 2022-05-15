import os
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from time import sleep


scopes = ['https://www.googleapis.com/auth/drive']

def auth():
  global creds
  global service
  creds = None
  if (os.path.exists('token.json')):
    print('good')
    creds = Credentials.from_authorized_user_file('token.json', scopes)
    service = build('drive', 'v3', credentials = creds)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("secrets.json", scopes)
      creds = flow.run_local_server(port = 0)
    with open('token.json', 'w') as token:
      token.write(creds.to_json())


def create(folder):
    file_metadata = {
        'name': folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body = file_metadata, fields = 'id').execute()
    
def search_upload(name, title, content):
  path = 'E:\pythonprojects\drive_bot'

  os.chdir(path)
  for file in os.listdir():
    if file.endswith('.txt'):
      file_path = f'{path}\{file}'
      os.rename(f'{path}\{file}', f'{title}.txt')

  f = open(f'{title}.txt', 'r+')
  
  for i in f:
    f.writelines(content) 
  resources = service.files().list (q="mimeType='application/vnd.google-apps.folder'",fields = "files(id, name)").execute()
  file_list = (resources.get('files'))
  ans = None
  
  for i in range(0, len(file_list)):
    if file_list[i]['name'] == name:
      ans = file_list[i]['id']  

  folder_id = ans
  file_metadata = {
    'name': f'{title}.txt',
    'parents': [folder_id]
}
  media = MediaFileUpload(f'{title}.txt',
                        mimetype='text/plain'
                        )
  file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
  print('done')
  
  f.close()


