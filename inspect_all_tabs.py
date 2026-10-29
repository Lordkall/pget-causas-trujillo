import json
import io
import sys

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

tab_info = []

for s in sheets:
    props = s.get('properties', {})
    title = props.get('title')
    sheet_id = props.get('sheetId')
    
    if 'gráfico' in title.lower() or 'grafico' in title.lower():
        continue
        
    try:
        res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{title}'!A1:Z6"
        ).execute()
        rows = res.get('values', [])
    except Exception as e:
        print(f"Error reading {title}: {e}")
        rows = []
        
    tab_info.append({
        'title': title,
        'gid': sheet_id,
        'rows': rows
    })

# Output as JSON so we can analyze programmatically
with open('all_tabs_structure.json', 'w', encoding='utf-8') as f:
    json.dump(tab_info, f, ensure_ascii=False, indent=2)

print(f"Successfully inspected {len(tab_info)} tabs and wrote to all_tabs_structure.json")

