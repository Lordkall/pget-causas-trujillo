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

for sheet in sheet_names:
    if sheet == 'Gráfico1':
        continue
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{sheet}'").execute()
        rows = res.get('values', [])
        if not rows: continue
        
        # Determine lawyer col
        lawyer_cols = []
        for r in rows[:3]:
            for idx, cell in enumerate(r):
                c_u = str(cell).upper()
                if 'ABG' in c_u or 'RESPONSABLE' in c_u or 'ABOGAD' in c_u or 'ASIGNAD' in c_u:
                    if idx not in lawyer_cols:
                        lawyer_cols.append(idx)
        
        # Check values in lawyer_cols
        for r_idx, r in enumerate(rows):
            for col_idx in lawyer_cols:
                if len(r) > col_idx and r[col_idx]:
                    val = str(r[col_idx]).strip()
                    val_u = val.upper()
                    if any(t in val_u for t in ['MARIA', 'ANGELES', 'ROXANA', 'ROXXANA', 'MERCADO']):
                        print(f"[{sheet}] Row {r_idx+1} Col {col_idx+1}: '{val}'")
    except Exception as e:
        print(f"Error {sheet}: {e}")

