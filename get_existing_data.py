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
    range="'JUZGADOS DE MUNICIPIOS ORDINARI'!A1:R100"
).execute()

rows = result.get('values', [])
print("Total rows:", len(rows))
abogados = set()
for r in rows[1:]:
    if len(r) > 7 and r[7].strip():
        abogados.add(r[7].strip())
print("Abogados existentes en la hoja:", list(abogados))

