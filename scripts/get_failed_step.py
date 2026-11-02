import urllib.request
import json

url = 'https://api.github.com/repos/Lordkall/pget-causas-trujillo/actions/runs/41443192716/jobs'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    for j in data.get('jobs', []):
        print('Job:', j['name'], '-> Conclusion:', j['conclusion'])
        for s in j.get('steps', []):
            print(f"  Step: {s['name']} | Conclusion: {s['conclusion']}")
