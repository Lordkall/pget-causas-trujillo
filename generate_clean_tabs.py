import json

with open('all_tabs_structure.json', 'r', encoding='utf-8') as f:
    tabs = json.load(f)

# Hardcoded adjustments based on deep inspection of the rows
tab_defs = []

for t in tabs:
    title = t['title']
    gid = t['gid']
    rows = t['rows']
    
    # Skip Hoja 1, Hoja 2, Hoja1, and Gráfico1
    if title in ['Hoja 1', 'Hoja 2', 'Hoja1'] or 'gráfico' in title.lower() or 'grafico' in title.lower():
        continue
        
    header_row_idx = 1
    cols = []
    
    if title == 'JUZGADOS DE MUNICIPIOS ORDINARI':
        header_row_idx = 1
        cols = rows[0]
    elif title == 'CORTE CONTENCIOSO ADMIN.':
        header_row_idx = 1
        cols = rows[0]
    elif title == 'CONSEJOS DE PROTECCION DE NIÑ@S':
        header_row_idx = 1
        cols = rows[0]
    elif title == 'PROTECCION DE NIÑOS, NIÑAS Y AD':
        header_row_idx = 3
        cols = rows[2]
    elif title == 'CALIFICACIONES NO PROCESADAS':
        header_row_idx = 2
        cols = rows[1]
    elif title == 'CONTENCIOSO TRUJILLO':
        header_row_idx = 1
        cols = rows[0]
    elif title == 'CONTENCIOSO':
        header_row_idx = 2
        cols = rows[1]
    elif title == 'AGRARIO':
        header_row_idx = 2
        cols = rows[1]
    elif title == 'LABORAL':
        header_row_idx = 2
        cols = rows[1]
    elif title == 'TRIBUNAL SUPREMO-JUZGADOS':
        header_row_idx = 3
        cols = rows[2]
    elif title in ['INSPECTORÍA-TRUJILO', 'INSPECTORÍA-VALERA', 'SUB-INSPECTORÍA-BOCONÓ', 'SOLICITUDES - VEHÍCULOS Y OTROS', 'CIRCUITO PENAL', 'FISCALÍAS ORD.-ESP']:
        header_row_idx = 2
        cols = rows[1]
    elif title == 'CIVIL':
        header_row_idx = 1
        cols = rows[0]
    else:
        # Fallback
        header_row_idx = 1
        cols = rows[0] if rows else []

    # Clean cols
    clean_cols = []
    for c in cols:
        val = str(c).replace('\n', ' ').strip()
        if val:
            clean_cols.append(val)
        else:
            clean_cols.append(f"Columna {len(clean_cols)+1}")

    tab_defs.append({
        'title': title,
        'gid': gid,
        'headerRow': header_row_idx,
        'columns': clean_cols
    })

print(f"Prepared {len(tab_defs)} valid tabs.")
with open('cleaned_tab_definitions.json', 'w', encoding='utf-8') as f:
    json.dump(tab_defs, f, ensure_ascii=False, indent=2)

for td in tab_defs:
    print(f"- {td['title']} ({len(td['columns'])} cols, headerRow: {td['headerRow']})")

