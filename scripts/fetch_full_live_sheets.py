import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

def fetch_all():
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = meta.get('sheets', [])

    print(f"Total sheets found: {len(sheets)}")

    # Mapeo de headerRow por pestaña según pget_tabs_list
    # (1-based headerRow: la fila de encabezado es 1 o 2, los datos empiezan después)
    # Por defecto para casi todas es fila 1, excepto Inspectoría-Valera que tiene título en fila 1 y encabezados en fila 2
    header_rows = {
        'INSPECTORÍA-VALERA': 2,
        'INSPECTORIA-VALERA': 2,
    }

    all_tabs_data = {}
    total_causes = 0

    for s in sheets:
        title = s['properties']['title']
        if 'Gráfico' in title or 'Grafico' in title:
            continue

        h_row = header_rows.get(title.strip().upper(), 1)
        start_row = h_row + 1

        print(f"Fetching sheet '{title}' from row {start_row}...")
        res = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"'{title}'!A{start_row}:Z5000"
        ).execute()

        raw_rows = res.get('values', [])
        # Filtrar filas vacías
        valid_rows = [r for r in raw_rows if any(str(c).strip() for c in r)]
        all_tabs_data[title] = valid_rows
        total_causes += len(valid_rows)
        print(f"  -> {len(valid_rows)} causas extraídas.")

    print(f"\nTotal causas consolidadas en todas las pestañas: {total_causes}")

    # Guardar en assets/pget_all_rows.json
    with open('assets/pget_all_rows.json', 'w', encoding='utf-8') as f:
        json.dump(all_tabs_data, f, ensure_ascii=False, separators=(',', ':'))
    print("Guardado exitoso en assets/pget_all_rows.json")

if __name__ == '__main__':
    fetch_all()

