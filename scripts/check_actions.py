import urllib.request
import json
import time

url = 'https://api.github.com/repos/Lordkall/pget-causas-trujillo/actions/runs'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

for _ in range(25):
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            runs = data.get('workflow_runs', [])
            if runs:
                r = runs[0]
                status = r['status']
                conclusion = r.get('conclusion')
                print(f"Status: {status} | Conclusion: {conclusion}")
                if status == 'completed':
                    print("Build finished with conclusion:", conclusion)
                    if conclusion == 'success':
                        print("APK Build Successful!")
                    break
    except Exception as e:
        print("Error checking:", e)
    time.sleep(12)
