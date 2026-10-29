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

raw_lawyer_values = set()

for sheet in sheet_names:
    if sheet == 'Gráfico1':
        continue
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{sheet}'").execute()
        rows = res.get('values', [])
        if not rows: continue
        
        lawyer_cols = []
        for r in rows[:3]:
            for idx, cell in enumerate(r):
                c_u = str(cell).upper()
                if 'ABG' in c_u or 'RESPONSABLE' in c_u or 'ABOGAD' in c_u or 'ASIGNAD' in c_u:
                    if idx not in lawyer_cols:
                        lawyer_cols.append(idx)
        
        for r_idx, r in enumerate(rows[1:]):
            for col_idx in lawyer_cols:
                if len(r) > col_idx and r[col_idx]:
                    val = str(r[col_idx]).strip()
                    if val and len(val) > 2 and not 'ABOGAD' in val.upper() and not 'RESPONSABLE' in val.upper():
                        raw_lawyer_values.add(val)
    except Exception as e:
        print(f"Error {sheet}: {e}")

print(f"Total raw lawyer values across ENTIRE spreadsheet ({len(raw_lawyer_values)} values):")
for v in sorted(raw_lawyer_values):
    print(f"'{v}'")

