import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheet_names = [s['properties']['title'] for s in meta['sheets']]
print('All sheets in document:', sheet_names)

terms = ['MARIA', 'ANGELES', 'ROXANA', 'ROXXANA', 'MERCADO']

for sheet in sheet_names:
    if sheet == 'Gráfico1':
        continue
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{sheet}'").execute()
        rows = res.get('values', [])
        # Check rows
        matches_in_sheet = []
        for r_idx, r in enumerate(rows):
            for c_idx, val in enumerate(r):
                v_str = str(val).strip().upper()
                for term in terms:
                    if term in v_str:
                        matches_in_sheet.append((r_idx + 1, c_idx + 1, str(val).strip()))
                        break
        if matches_in_sheet:
            print(f"\n=== Sheet: {sheet} ({len(rows)} rows) - Found {len(matches_in_sheet)} matches ===")
            for r_num, c_num, val in matches_in_sheet:
                print(f"  Row {r_num}, Col {c_num}: {val}")
    except Exception as e:
        print(f"Error reading {sheet}: {e}")

