import re
import ast

with open('prototype.html', 'r', encoding='utf-8') as f:
    html = f.read()

lawyers_block = re.search(r'let lawyers = (\[[\s\S]*?\]);', html).group(1)
# Remove comments
lawyers_block = re.sub(r'//.*', '', lawyers_block)
# Quote unquoted keys
py_block = re.sub(r'(\b\w+\b):', r"'\1':", lawyers_block)
py_block = py_block.replace('true', 'True').replace('false', 'False')

lawyers_list = ast.literal_eval(py_block)
active = [l for l in lawyers_list if l['activo']]
print('Active count:', len(active))
for i, l in enumerate(active, 1):
    print(f"{i}. {l['nombre']} | C.I. {l['cedula']} | {l['cargo']}")
