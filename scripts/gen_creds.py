import json, base64

with open('credentials.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

minified = json.dumps(d)
b64_str = base64.b64encode(minified.encode('utf-8')).decode('ascii')

content = f'''import 'dart:convert';

// Credenciales oficiales de la Procuraduria General del Estado Trujillo (codificadas)
// Servicio: dataasuntosj@data-asuntos-juridicos.iam.gserviceaccount.com
const String _pgetEncodedCreds = '{b64_str}';

String get pgetOfficialCredentialsJson {{
  final bytes = base64.decode(_pgetEncodedCreds);
  return utf8.decode(bytes);
}}
'''

with open('lib/services/pget_credentials.dart', 'w', encoding='utf-8') as f:
    f.write(content)

print("lib/services/pget_credentials.dart generated with base64 encoding!")
