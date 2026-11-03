import urllib.request
import json
import zipfile
import io
import os
import subprocess
import time

def get_token():
    try:
        remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
        if '@' in remote and '://' in remote:
            return remote.split('://')[1].split('@')[0]
    except Exception:
        pass
    return os.environ.get('GITHUB_TOKEN', '')

TOKEN = get_token()
REPO = 'Lordkall/pget-causas-trujillo'
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Mozilla/5.0'
}

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return fp

opener = urllib.request.build_opener(NoRedirectHandler)

def monitor_and_download(target_sha=None):
    print("Checking workflow runs for Lordkall/pget-causas-trujillo...")
    runs_url = f'https://api.github.com/repos/{REPO}/actions/runs?per_page=5'
    
    target_run = None
    for attempt in range(40):
        try:
            req = urllib.request.Request(runs_url, headers=HEADERS)
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                runs = data.get('workflow_runs', [])
                if runs:
                    latest = runs[0]
                    head_sha = latest.get('head_sha', '')[:7]
                    status = latest.get('status')
                    conclusion = latest.get('conclusion')
                    run_id = latest.get('id')
                    print(f"[{attempt+1}] Run ID: {run_id} | SHA: {head_sha} | Status: {status} | Conclusion: {conclusion}")
                    
                    if status == 'completed':
                        if target_sha is None or head_sha.startswith(target_sha[:7]):
                            target_run = latest
                            break
        except Exception as e:
            print(f"Attempt {attempt+1} error checking runs: {e}")
        
        time.sleep(12)
        
    if not target_run:
        print("Timeout waiting for run completion.")
        return False
        
    conclusion = target_run.get('conclusion')
    run_id = target_run.get('id')
    if conclusion != 'success':
        print(f"Workflow run {run_id} finished with conclusion: {conclusion}")
        return False
        
    print(f"\nRun {run_id} SUCCEEDED! Fetching artifacts...")
    artifacts_url = f'https://api.github.com/repos/{REPO}/actions/runs/{run_id}/artifacts'
    req_art = urllib.request.Request(artifacts_url, headers=HEADERS)
    with urllib.request.urlopen(req_art) as resp:
        art_data = json.loads(resp.read().decode('utf-8'))
        artifacts = art_data.get('artifacts', [])
        
    apk_art = None
    for a in artifacts:
        print(f"Found artifact: {a['name']} ({a['size_in_bytes']} bytes)")
        if 'apk' in a['name'].lower():
            apk_art = a
            break
            
    if not apk_art:
        print("No APK artifact found!")
        return False
        
    download_url = apk_art['archive_download_url']
    print(f"Downloading APK artifact from {download_url}...")
    req_redirect = urllib.request.Request(download_url, headers=HEADERS)
    try:
        resp = opener.open(req_redirect)
        azure_url = resp.headers.get('Location')
    except Exception as e:
        azure_url = getattr(e, 'headers', {}).get('Location')

    if not azure_url:
        print("Could not obtain redirect URL.")
        return False

    req_blob = urllib.request.Request(azure_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_blob) as resp:
        zip_bytes = resp.read()

    os.makedirs('build_output', exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        for name in z.namelist():
            if name.endswith('.apk'):
                apk_bytes = z.read(name)
                dest = os.path.join('build_output', 'PGET-Causas-Juridicas.apk')
                with open(dest, 'wb') as f:
                    f.write(apk_bytes)
                print(f"SAVED APK: {dest} ({len(apk_bytes):,} bytes)")
                return True
                
    return False

if __name__ == '__main__':
    monitor_and_download()
