import json, base64, re

with open('lib/services/pget_credentials.dart', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r"_pgetEncodedCreds = '([^']+)'", text)
b64 = m.group(1)
decoded = base64.b64decode(b64).decode('utf-8')
d = json.loads(decoded)
print('Keys in decoded json:', list(d.keys()))
print('client_email:', d.get('client_email'))
print('private_key has newlines:', '\n' in d.get('private_key', ''))
print('private_key prefix:', repr(d.get('private_key', '')[:40]))
