from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
sid = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

def test_find_insert_position(tab_title, target_year):
    res = service.spreadsheets().values().get(spreadsheetId=sid, range=f"'{tab_title}'!A1:Z200").execute()
    rows = res.get('values', [])
    print(f"\n--- Checking {tab_title} for Year {target_year} (total {len(rows)} rows) ---")
    
    banner_pattern = re.compile(r'CAUSAS?\s*(?:A[ÑN]O)?\s*(\d{4})', re.IGNORECASE)
    
    banners = []
    last_meaningful_row = 1
    
    for i, r in enumerate(rows, 1):
        line = ' '.join(str(c) for c in r).strip()
        m = banner_pattern.search(line)
        if m:
            year = int(m.group(1))
            banners.append((i, year, line))
            last_meaningful_row = i
        elif any(str(c).strip() for c in r):
            # check if row is just trailing numbers in col A
            col0 = str(r[0]).strip() if len(r) > 0 else ''
            rest = [str(c).strip() for c in r[1:]]
            if any(rest):
                last_meaningful_row = i
            elif col0 and not col0.isdigit():
                last_meaningful_row = i
            elif col0.isdigit() and int(col0) <= 20 and i <= 20:
                last_meaningful_row = i

    print("Found banners:", banners)
    print("Last meaningful row:", last_meaningful_row)
    
    # Check if target_year banner exists
    existing = [b for b in banners if b[1] == target_year]
    if existing:
        banner_row = existing[0][0]
        # Find next banner
        later_banners = [b for b in banners if b[0] > banner_row]
        next_banner_row = later_banners[0][0] if later_banners else last_meaningful_row + 1
        print(f"Banner for {target_year} exists at row {banner_row}. Insert after {next_banner_row - 1}")
    else:
        print(f"Banner for {target_year} DOES NOT EXIST. Needs new banner at row {last_meaningful_row + 1}, then cause at row {last_meaningful_row + 2}")

test_find_insert_position('JUZGADOS DE MUNICIPIOS ORDINARI', 2026)
test_find_insert_position('CORTE CONTENCIOSO ADMIN.', 2026)
