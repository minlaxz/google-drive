import pickle,predef,os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_service():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./credentials/token.pickle'):
        with open('./credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials/client_secret.json', predef.SCOPES)
            creds = flow.run_local_server(port=0)
        
        #save credentials for the next run
        with open('./credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    print("Authenticated.")
    return service