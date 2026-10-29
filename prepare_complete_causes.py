import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'

meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
sheet_names = [s['properties']['title'] for s in meta['sheets'] if s['properties']['title'] != 'Gráfico1']

with open('cleaned_tab_definitions.json', 'r', encoding='utf-8') as f:
    tabs_def = json.load(f)

tabs_map = {t['title']: t for t in tabs_def}

causes_by_tab = {}
all_years = set()

def extract_year(text):
    m = re.findall(r'\b(199\d|20[0-3]\d)\b', text)
    return m[-1] if m else ''

for sheet in sheet_names:
    t_def = tabs_map.get(sheet)
    if not t_def:
        continue
    
    header_row = t_def['headerRow']
    cols = [c.upper() for c in t_def['columns']]
    
    # Identify indices
    exp_idx = -1
    dem_idx = -1
    dmd_idx = -1
    mot_idx = -1
    abg_idx = -1
    est_idx = -1
    fec_idx = -1
    act_idx = -1
    
    for idx, c in enumerate(cols):
        if 'EXPEDIENTE' in c or 'INVESTIGACION' in c:
            if exp_idx == -1: exp_idx = idx
        if any(k in c for k in ['DEMANDANTE', 'QUERELLANTE', 'SOLICITANTE']):
            if dem_idx == -1: dem_idx = idx
        if any(k in c for k in ['DEMANDADO', 'QUERELLADO', 'IMPUTADO', 'SOLICITADO']):
            if dmd_idx == -1: dmd_idx = idx
        if any(k in c for k in ['MOTIVO', 'DELITO', 'ACCION', 'OBJETO']):
            if mot_idx == -1: mot_idx = idx
        if any(k in c for k in ['ABG', 'ABOGAD', 'RESPONSABLE']):
            if abg_idx == -1: abg_idx = idx
        if 'ESTADO' in c and 'ADSCRITO' not in c:
            if est_idx == -1: est_idx = idx
        if 'FECHA' in c:
            if fec_idx == -1: fec_idx = idx
        if any(k in c for k in ['ACTUACION', 'OBSERVACION']):
            if act_idx == -1: act_idx = idx

    print(f"Fetching '{sheet}'...")
    try:
        res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{sheet}'").execute()
        rows = res.get('values', [])
    except Exception as e:
        print(f"Error {sheet}: {e}")
        rows = []
        
    data_rows = rows[header_row:] if len(rows) > header_row else []
    
    # Filter valid rows
    valid_rows = []
    for r_num, r in enumerate(data_rows, start=header_row + 1):
        if not r or not any(str(x).strip() for x in r):
            continue
        row_str = " ".join(str(x) for x in r).strip()
        if len(r) <= 2 and ('CAUSA' in row_str.upper() or row_str.isdigit()):
            continue
            
        def get_v(idx):
            return str(r[idx]).strip() if idx >= 0 and idx < len(r) and r[idx] is not None else ''
            
        exp = get_v(exp_idx)
        mot = get_v(mot_idx) or 'Causa Registrada'
        abg = get_v(abg_idx)
        dmd = get_v(dmd_idx)
        est = get_v(est_idx) or 'ACTIVA'
        fec = get_v(fec_idx)
        act = get_v(act_idx)
        
        if not exp and not abg and not dmd:
            continue
            
        yr = extract_year(f"{fec} {exp} {row_str}")
        if yr:
            all_years.add(yr)
            
        valid_rows.append({
            'row_index': r_num,
            'expediente': exp if exp else f"REG-{r_num}",
            'motivo': mot,
            'demandado': dmd,
            'abogado': abg if abg else 'Sin asignar',
            'estado': est,
            'fecha': fec,
            'year': yr,
            'actuaciones': act[:120] if act else ''
        })
        
    # We want a healthy selection: include rows with Roxanna / Maria Ojeda / Samantha / Diana etc.
    # plus the latest rows and early rows (up to 60 rows per tab)
    special_rows = [r for r in valid_rows if any(k in r['abogado'].upper() for k in ['ROXANNA', 'ROXANA', 'OJEDA', 'ANGELES', 'ANDREINA', 'KLEIVER', 'VALERO'])]
    other_rows = [r for r in valid_rows if r not in special_rows]
    
    # Combine special rows with latest and first rows
    selected = special_rows + other_rows[:35] + other_rows[-15:]
    # deduplicate by row_index
    seen = set()
    final_tab_rows = []
    for item in selected:
        if item['row_index'] not in seen:
            seen.add(item['row_index'])
            final_tab_rows.append(item)
            
    final_tab_rows.sort(key=lambda x: x['row_index'])
    causes_by_tab[sheet] = final_tab_rows
    print(f"  -> Processed {len(final_tab_rows)} causes for {sheet} (including {len(special_rows)} special lawyer rows)")

sorted_years = sorted(list(all_years), reverse=True)

with open('compact_causes_by_tab.json', 'w', encoding='utf-8') as f:
    json.dump({'causes_by_tab': causes_by_tab, 'years': sorted_years}, f, ensure_ascii=False, indent=2)

print("\nSuccessfully updated compact_causes_by_tab.json!")
print("Years discovered:", sorted_years[:10], "...", sorted_years[-5:])

