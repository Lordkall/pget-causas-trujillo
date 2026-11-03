from google.oauth2 import service_account
from googleapiclient.discovery import build
import re

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
sid = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

meta = service.spreadsheets().get(spreadsheetId=sid).execute()
for s in meta['sheets']:
    title = s['properties']['title']
    if 'Gráfico' in title or 'Grafico' in title:
        continue
    rows = service.spreadsheets().values().get(spreadsheetId=sid, range=f"'{title}'!A1:E30").execute().get('values', [])
    banners = []
    for i, r in enumerate(rows, 1):
        txt = ' '.join(str(c) for c in r)
        if re.search(r'CAUSAS?\s*(?:A[ÑN]O)?\s*\d{4}', txt, re.IGNORECASE):
            banners.append((i, txt.strip()))
    print(f"Sheet: {title} -> {len(rows)} rows, Banners: {banners}")
