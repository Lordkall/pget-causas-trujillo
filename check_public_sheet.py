import urllib.request

urls = [
    "https://docs.google.com/spreadsheets/d/1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg/export?format=csv&gid=928732016",
    "https://docs.google.com/spreadsheets/d/1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg/gviz/tq?tqx=out:csv&gid=928732016"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            print(f"Success for {url[:60]}...:\nFirst 500 chars:")
            print(content[:500])
            break
    except Exception as e:
        print(f"Failed for {url[:60]}: {e}")

