import json

with open('all_tabs_structure.json', 'r', encoding='utf-8') as f:
    tabs = json.load(f)

print(f"Total tabs: {len(tabs)}\n")

for t in tabs:
    title = t['title']
    gid = t['gid']
    rows = t['rows']
    print("=" * 60)
    print(f"TAB: '{title}' (GID: {gid}) - Rows found: {len(rows)}")
    
    header_idx = -1
    headers = []
    
    # Identify header row: usually contains words like Nº, TRIBUNAL, DEMANDANTE, CAUSA, EXPEDIENTE, MOTIVO
    for i, r in enumerate(rows):
        joined = " ".join([str(x) for x in r]).upper()
        if any(keyword in joined for keyword in ['DEMANDANTE', 'EXPEDIENTE', 'MOTIVO', 'TRIBUNAL', 'ABG', 'JUZGADO']):
            header_idx = i
            headers = [str(x).strip() for x in r if str(x).strip()]
            break
            
    if header_idx != -1:
        print(f"  Header row: Row {header_idx + 1}")
        print(f"  Columns ({len(rows[header_idx])}):")
        for col_idx, col_name in enumerate(rows[header_idx]):
            if col_name.strip():
                print(f"    [{col_idx}] {col_name.strip()}")
    else:
        print("  (Could not auto-detect header row, showing first 2 rows):")
        for i, r in enumerate(rows[:2]):
            print(f"    Row {i+1}: {r}")

