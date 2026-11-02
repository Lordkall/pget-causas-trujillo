import urllib.request
import json

url = 'https://api.github.com/repos/Lordkall/pget-causas-trujillo/check-runs?check_suite_id='
# Get check suites
url_suite = 'https://api.github.com/repos/Lordkall/pget-causas-trujillo/commits/2c9a5f8/check-suites'
req = urllib.request.Request(url_suite, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        suites = data.get('check_suites', [])
        for s in suites:
            suite_id = s['id']
            runs_url = f'https://api.github.com/repos/Lordkall/pget-causas-trujillo/check-suites/{suite_id}/check-runs'
            req2 = urllib.request.Request(runs_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2) as resp2:
                data2 = json.loads(resp2.read().decode('utf-8'))
                for cr in data2.get('check_runs', []):
                    print('Check run:', cr['name'], '->', cr['conclusion'])
                    print('Output Title:', cr.get('output', {}).get('title'))
                    print('Output Summary:', cr.get('output', {}).get('summary'))
                    print('Output Text:', cr.get('output', {}).get('text'))
                    # annotations
                    annot_url = cr.get('output', {}).get('annotations_url')
                    if annot_url:
                        req3 = urllib.request.Request(annot_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req3) as resp3:
                            annots = json.loads(resp3.read().decode('utf-8'))
                            for a in annots:
                                print('  Annotation:', a.get('message'))
except Exception as e:
    print('Error:', e)
