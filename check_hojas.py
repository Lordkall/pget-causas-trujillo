import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

for name in ['Hoja 1', 'Hoja 2', 'Hoja1']:
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{name}'!A1:E5").execute()
        print(f"Tab '{name}': {res.get('values', [])}")
    except Exception as e:
        print(f"Error {name}: {e}")

