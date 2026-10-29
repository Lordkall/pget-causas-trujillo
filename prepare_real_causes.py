import json
import re

with open('full_spreadsheet_dump.json', 'r', encoding='utf-8') as f:
    dump = json.load(f)

tabs = dump['tabs']
all_years = set()

def extract_year(row_text):
    # Search for dates like dd/mm/yyyy or dd-mm-yy or years 1990-2029
    # Look for 4-digit years between 1995 and 2030
    matches = re.findall(r'\b(199\d|20[0-3]\d)\b', row_text)
    if matches:
        return matches[-1] # Usually the most recent or date year
    return None

sample_causes_by_tab = {}

for tab_name, tab_data in tabs.items():
    rows = tab_data['rows']
    sample_causes = []
    
    cols = tab_data['columns']
    exp_idx = -1
    motivo_idx = -1
    dem_idx = -1
    abg_idx = -1
    estado_idx = -1
    fecha_idx = -1
    
    for i, c in enumerate(cols):
        u = c.upper()
        if 'EXPEDIENTE' in u or 'INVESTIGACION' in u: exp_idx = i
        if 'MOTIVO' in u or 'DELITO' in u: motivo_idx = i
        if 'DEMANDADO' in u or 'QUERELLADO' in u or 'IMPUTADO' in u: dem_idx = i
        if 'ABG' in u or 'RESPONSABLE' in u: abg_idx = i
        if 'ESTADO' in u: estado_idx = i
        if 'FECHA' in u: fecha_idx = i

    for r_idx, r in enumerate(rows[:30]): # Take up to 30 real rows per tab
        row_str = " ".join([str(x) for x in r])
        yr = extract_year(row_str)
        if yr: all_years.add(yr)
        
        def g(idx):
            if idx != -1 and idx < len(r) and r[idx]:
                return str(r[idx]).strip()
            return ''
            
        exp = g(exp_idx) or f"EXP-{r_idx+1}"
        motivo = g(motivo_idx) or (r[1] if len(r) > 1 else 'Sin motivo')
        dem = g(dem_idx)
        abg = g(abg_idx) or 'PGET'
        estado = g(estado_idx) or 'ACTIVA'
        fecha = g(fecha_idx) or (yr or '')
        
        sample_causes.append({
            'numero': str(r_idx + 1),
            'expediente': exp,
            'motivo': motivo[:120],
            'demandado': dem[:80],
            'abogado': abg[:50],
            'estado': estado if any(x in estado.upper() for x in ['ACT', 'CERR', 'TRAM']) else 'ACTIVA',
            'fecha': fecha,
            'year': yr or '2020',
            'raw': [str(x).strip() for x in r]
        })
        
    sample_causes_by_tab[tab_name] = sample_causes

print(f"Sample causes generated for {len(sample_causes_by_tab)} tabs.")
print("Years detected:", sorted(list(all_years)))

with open('compact_causes_by_tab.json', 'w', encoding='utf-8') as f:
    json.dump({
        'causes_by_tab': sample_causes_by_tab,
        'years': sorted(list(all_years), reverse=True)
    }, f, ensure_ascii=False, indent=2)

