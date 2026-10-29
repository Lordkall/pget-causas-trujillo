import json

with open('cleaned_tab_definitions.json', 'r', encoding='utf-8') as f:
    tabs = json.load(f)

dart_code = '''import 'package:flutter/material.dart';

class PgetTab {
  final String title;
  final int gid;
  final int headerRow;
  final String category;
  final IconData icon;
  final List<String> columns;

  const PgetTab({
    required this.title,
    required this.gid,
    required this.headerRow,
    required this.category,
    required this.icon,
    required this.columns,
  });
}

// Lista oficial de todas las pestañas de la Procuraduría General del Estado Trujillo
// (Excepto Gráfico1)
final List<PgetTab> pgetTabsList = [
'''

def get_category_and_icon(title):
    t = title.upper()
    if 'MUNICIPIO' in t or 'CIVIL' in t:
        return 'Juzgados Municipales y Civiles', 'Icons.gavel'
    elif 'CONTENCIOSO' in t:
        return 'Contencioso Administrativo', 'Icons.account_balance'
    elif 'NIÑ' in t or 'PROTECCION' in t:
        return 'Protección de Niños, Niñas y Adolescentes', 'Icons.family_restroom'
    elif 'PENAL' in t or 'FISCAL' in t or 'VEH' in t:
        return 'Circuito Penal y Fiscalías', 'Icons.policy'
    elif 'LABORAL' in t or 'INSPECTOR' in t or 'CALIFICACION' in t:
        return 'Laboral e Inspectorías del Trabajo', 'Icons.work'
    elif 'AGRARIO' in t:
        return 'Materia Agraria y Tierras', 'Icons.agriculture'
    elif 'SUPREMO' in t or 'TSJ' in t:
        return 'Tribunal Supremo de Justicia', 'Icons.shield'
    else:
        return 'General PGET', 'Icons.folder'

for t in tabs:
    cat, icon = get_category_and_icon(t['title'])
    dart_code += f"  PgetTab(\n"
    dart_code += f"    title: '{t['title']}',\n"
    dart_code += f"    gid: {t['gid']},\n"
    dart_code += f"    headerRow: {t['headerRow']},\n"
    dart_code += f"    category: '{cat}',\n"
    dart_code += f"    icon: {icon},\n"
    dart_code += f"    columns: [\n"
    for col in t['columns']:
        # escape single quotes
        c_esc = col.replace("'", "\\'")
        dart_code += f"      '{c_esc}',\n"
    dart_code += f"    ],\n"
    dart_code += f"  ),\n"

dart_code += '''];
'''

with open('d:/data abogados/lib/models/pget_tab.dart', 'w', encoding='utf-8') as f:
    f.write(dart_code)

print("lib/models/pget_tab.dart written successfully!")

