import json
import base64
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=creds)

with open('cleaned_tab_definitions.json', 'r', encoding='utf-8') as f:
    tabs = json.load(f)

all_tabs_data = {}
all_lawyers = set()

# Also base64 encode the logo
with open('assets/logo_pget.png', 'rb') as img_f:
    logo_base64 = base64.b64encode(img_f.read()).decode('utf-8')

for t in tabs:
    title = t['title']
    header_row = t['headerRow']
    cols = t['columns']
    
    try:
        res = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{title}'!A1:Z100"
        ).execute()
        rows = res.get('values', [])
    except Exception as e:
        print(f"Error {title}: {e}")
        rows = []
        
    data_rows = []
    # Identify lawyer column index
    abg_idx = -1
    for i, col in enumerate(cols):
        u = col.upper()
        if 'ABG' in u or 'RESPONSABLE' in u:
            abg_idx = i
            break
            
    # Process rows after header
    if len(rows) > header_row:
        for r_idx, r in enumerate(rows[header_row:]):
            if not r or not any(str(x).strip() for x in r):
                continue
            # Check if this row is just a year header like "CAUSAS 2014" or "2015"
            row_str = " ".join([str(x) for x in r]).strip()
            if len(r) <= 2 and ('CAUSA' in row_str.upper() or row_str.isdigit()):
                continue
                
            # Extract lawyer if present
            if abg_idx != -1 and len(r) > abg_idx:
                raw_lawyer = str(r[abg_idx]).strip()
                # Clean up prefixes like **ABG., ABG., etc.
                cleaned = re.sub(r'[*]+ABG\.?\s*', '', raw_lawyer, flags=re.IGNORECASE)
                cleaned = re.sub(r'^ABG\.?\s*', '', cleaned, flags=re.IGNORECASE).strip()
                if cleaned and len(cleaned) > 2 and not cleaned.isdigit():
                    # Handle multiple lawyers separated by Y or comma
                    for part in re.split(r'\s+Y\s+|,\s*', cleaned, flags=re.IGNORECASE):
                        p = part.strip().upper()
                        if p and len(p) > 3 and not p.isdigit() and 'CAUSAS' not in p:
                            all_lawyers.add(p)

            # Store clean row
            data_rows.append(r)
            
    all_tabs_data[title] = {
        'title': title,
        'gid': t['gid'],
        'headerRow': header_row,
        'columns': cols,
        'rows': data_rows
    }
    print(f"Tab '{title}': {len(data_rows)} data rows")

print(f"\nALL LAWYERS FOUND ACROSS ENTIRE SPREADSHEET ({len(all_lawyers)}):")
for l in sorted(list(all_lawyers)):
    print(f" - {l}")

with open('full_spreadsheet_dump.json', 'w', encoding='utf-8') as f:
    json.dump({
        'tabs': all_tabs_data,
        'lawyers': sorted(list(all_lawyers)),
        'logo_base64': logo_base64
    }, f, ensure_ascii=False, indent=2)

print("\nDump written to full_spreadsheet_dump.json successfully!")

