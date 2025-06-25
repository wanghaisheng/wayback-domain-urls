# query.py
import requests
import urllib.parse
import sys
import os

def get_unique_paths(domain: str, limit: int = 10000) -> set:
    url = "https://web.archive.org/cdx/search/cdx"
    params = {
        "url": f"{domain}/*",
        "output": "json",
        "fl": "original",
        "collapse": "urlkey",
        "limit": str(limit)
    }
    
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()[1:]  # skip header
    path_set = set()

    for [full_url] in data:
        parsed = urllib.parse.urlparse(full_url)
        path = parsed.path.split("#")[0]
        if path:
            path_set.add(path)

    return path_set

if __name__ == "__main__":
    domain = sys.argv[1]
    clean_name = domain.replace("https://", "").replace("http://", "").replace("/", "").strip()
    paths = get_unique_paths(clean_name)

    os.makedirs("result", exist_ok=True)
    with open(f"result/{clean_name}.txt", "w", encoding="utf-8") as f:
        for path in sorted(paths):
            f.write(path + "\n")
