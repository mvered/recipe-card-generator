# Set up credentials to access Google Sheets & Google Photos APIs


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", 
"https://www.googleapis.com/auth/photoslibrary.readonly"]

# Libraries
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Functions
def get_creds():
    """
    Checks if credentials already exist (in a token.json file), otherwise prompts log-in.
    """
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("../google_api/token.json"):
        creds = Credentials.from_authorized_user_file("../google_api/token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../google_api/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("../google_api/token.json", "w") as token:
            token.write(creds.to_json())

    # return credentials
    return creds

if __name__ == '__main__':
    get_creds()