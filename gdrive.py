from __future__ import print_function
import pickle
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# PREDEFINED#
SCOPES = ['https://www.googleapis.com/auth/drive']
# scope is important ref: https://developers.google.com/drive/api/v3/about-auth#OAuth2Authorizing

GDRIVE_FOLDER_NAME = "LAZE-BACKUP"  #folder on google drive
FOLDER_TO_ZIP_DIRECTORY= "/home/laxz/go-to-drive"
NOTIFICATION_EMIAL_ADDRESS = "mgmglatt.6991@gmail.com"


def get_service():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        #save credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def get_folder_id(service,name):
    results = service.files().list(q="name='"+name+"'",
                                spaces='drive',
                                fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])
    if items:
        folderID = items[0]['id']
    else:
        folder_metadata = {
            'name' : GDRIVE_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata,fields='id').execute()
        folderID = folder.get('id')
    return folderID

def getTimestampLabel():
    return "BACKUP_"+datetime.now().strftime('%d_%b_%Y__%X').replace(":","_")
	#return "BACKUP_"+time.strftime("%x").replace("/","-")+"_"+time.strftime("%X")+"_"+str(int(round(time.time())))

def zip_this(directory):
	print("Creating ZIP folder to upload...")
	zipFileName = getTimestampLabel()+".zip"
	os.system("zip -r "+zipFileName+" "+directory)
	print("ZIP folder created: "+zipFileName+"\n")
	return zipFileName # 'Backup_20_Apr_2020__00_22_18.zip'

def main():
    service = get_service()
    print('Authenticated.')

    folderID = get_folder_id(service=service, name=GDRIVE_FOLDER_NAME)
    print("FolderID for {0} is {1}".format(GDRIVE_FOLDER_NAME, folderID))

    zipFileName = zip_this(FOLDER_TO_ZIP_DIRECTORY)
    print('zipped. {0}'.format(zipFileName))

if __name__ == "__main__":
    main()