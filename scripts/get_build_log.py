import urllib.request
import json
import zipfile
import io

# Get job ID
url = 'https://api.github.com/repos/Lordkall/pget-causas-trujillo/actions/runs/41443192716/jobs'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    job_id = data['jobs'][0]['id']

print('Job ID:', job_id)
# Download job log
log_url = f'https://api.github.com/repos/Lordkall/pget-causas-trujillo/actions/jobs/{job_id}/logs'
req2 = urllib.request.Request(log_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req2) as resp:
        log_text = resp.read().decode('utf-8', errors='replace')
        # find 'Build Android Release APK' or 'FAILURE' or 'error'
        lines = log_text.splitlines()
        print(f"Total log lines: {len(lines)}")
        # print last 80 lines
        for l in lines[-80:]:
            print(l)
except Exception as e:
    print('Error downloading log:', e)
