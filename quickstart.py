# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START docs_quickstart]
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly", 
"https://www.googleapis.com/auth/drive.photos.readonly"]

# The ID of a sample document.
DOC_ID = "14d17GFFmJWBle__sCoo7CGIoEJf7OXdgBcynSv7bBVE"


def main():
  """Shows basic usage of the Sheets API.
  Prints the sheet IDs and titles of a sample spreadsheet.
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

  try:
    service = build("sheets", "v4", credentials=creds)

    # Retrieve the documents contents from the Docs service.
    sheet_metadata = service.spreadsheets().get(spreadsheetId=DOC_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    sheet_list = []
    for sheet in sheets:
      title = sheet.get("properties", {}).get("title")
      sheet_id = sheet.get("properties", {}).get("sheetId", 0)
      sheet_list.append((sheet_id, title))

    print("List of Sheets:")
    for entry in sheet_list:
      # Print columns A and E, which correspond to indices 0 and 4.
      print(f"Sheet ID: {entry[0]}, Title: {entry[1]}")

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
# [END docs_quickstart]