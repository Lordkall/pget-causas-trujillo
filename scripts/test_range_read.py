from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
sid = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

# Test inserting row at 14 in JUZGADOS DE MUNICIPIOS ORDINARI
# Using values.update or batchUpdate insertDimension
# In gsheets Dart package: ws.values.insertRow(index, values) uses spreadsheets.values.update with range or insertRow
print("Testing live check...")
res = service.spreadsheets().values().get(spreadsheetId=sid, range="'JUZGADOS DE MUNICIPIOS ORDINARI'!A13:A16").execute()
print("Current rows 13-16 in JUZGADOS:", res.get('values', []))
