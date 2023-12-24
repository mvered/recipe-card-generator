### Recipe Card PDF Builder ###

# GLOBAL VARIABLES
DOC_ID = "14d17GFFmJWBle__sCoo7CGIoEJf7OXdgBcynSv7bBVE"


# Libraries
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Get Data
def get_creds():
    """
    Checks if credentials already exist (in a token.json file), otherwise prompts log-in.
    """
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
      )
        creds = flow.run_local_server(port=0)
    
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())


def main():
    """
    gets recipe info from google docs and turns it into a pdf
    """
    get_creds()

if __name__ == "__main__":
    main()