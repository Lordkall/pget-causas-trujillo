import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="'CONTENCIOSO TRUJILLO'!A1:Z355").execute()
rows = res.get('values', [])
print(f"Total rows in CONTENCIOSO TRUJILLO: {len(rows)}")

header = rows[0]
print("Header:", header)

for r_idx in range(195, 255):
    if r_idx < len(rows):
        r = rows[r_idx]
        print(f"Row {r_idx+1}: {[str(x)[:30] for x in r[:10]]}")

