import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = metadata.get('sheets', [])
print("Tabs:")
for s in sheets:
    p = s.get('properties', {})
    print(f"- {p.get('title')} (ID: {p.get('sheetId')})")

