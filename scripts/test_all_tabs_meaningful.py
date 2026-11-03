from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
sid = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

meta = service.spreadsheets().get(spreadsheetId=sid).execute()
banner_pattern = re.compile(r'CAUSAS?\s*(?:A[ÑN]O)?\s*(\d{4})', re.IGNORECASE)

for s in meta['sheets']:
    title = s['properties']['title']
    if 'Gráfico' in title or 'Grafico' in title:
        continue
    res = service.spreadsheets().values().get(spreadsheetId=sid, range=f"'{title}'!A1:Z500").execute()
    rows = res.get('values', [])
    
    last_meaningful = 1
    has_banners = False
    banners = []
    
    for i, r in enumerate(rows, 1):
        line = ' '.join(str(c) for c in r).strip()
        m = banner_pattern.search(line)
        if m:
            has_banners = True
            banners.append((i, int(m.group(1))))
            last_meaningful = i
        else:
            # Check if row is meaningful data
            # Has at least 2 non-empty cells OR has 1 cell with more than 3 chars (not just a stray counter)
            non_empty = [str(c).strip() for c in r if str(c).strip()]
            if len(non_empty) >= 2 or (len(non_empty) == 1 and not non_empty[0].isdigit()):
                last_meaningful = i
            elif len(non_empty) == 1 and non_empty[0].isdigit() and int(non_empty[0]) <= 20 and i <= 25:
                # Early row with just index
                last_meaningful = i
                
    print(f"[{title}] total_rows={len(rows)} | has_banners={has_banners} | last_meaningful={last_meaningful} | banners={banners[-2:] if banners else []}")
