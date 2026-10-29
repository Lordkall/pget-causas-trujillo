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

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range="'JUZGADOS DE MUNICIPIOS ORDINARI'!A1:R4"
).execute()

rows = result.get('values', [])
print("TOTAL ROWS READ:", len(rows))
for i, r in enumerate(rows):
    print(f"\n--- ROW {i+1} ({len(r)} cols) ---")
    for col_idx, val in enumerate(r):
        print(f"[{col_idx}] {val}")

