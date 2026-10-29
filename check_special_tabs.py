import json

with open('all_tabs_structure.json', 'r', encoding='utf-8') as f:
    tabs = json.load(f)

for t in tabs:
    title = t['title']
    rows = t['rows']
    if title in ['PROTECCION DE NIÑOS, NIÑAS Y AD', 'CONTENCIOSO', 'AGRARIO', 'LABORAL', 'TRIBUNAL SUPREMO-JUZGADOS', 'Hoja 1', 'Hoja 2', 'Hoja1']:
        print(f"\n=== TAB: {title} ===")
        for i, r in enumerate(rows[:5]):
            print(f"Row {i+1}: {r}")

