import os
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_DIR = "Topics/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# We will use Wikipedia API to get the exact image file URLs
def get_wiki_image_url(filename):
    query_url = f"https://en.wikipedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    headers = {'User-Agent': 'BPSC_Topics_Downloader/1.0'}
    req = urllib.request.Request(query_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data['query']['pages']
            for page_id in pages:
                if 'imageinfo' in pages[page_id]:
                    return pages[page_id]['imageinfo'][0]['url']
    except Exception as e:
        print(f"Error fetching metadata for {filename}: {e}")
    return None

FILES_TO_DOWNLOAD = {
    "parliament.jpg": "New Indian Parliament Building (Sansad Bhavan).jpg",
    "g20.jpg": "G20 Delhi Summit Group Photo.jpg",
    "bilateral.jpg": "Narendra Modi with Joe Biden in September 2023.jpg"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for local_name, wiki_name in FILES_TO_DOWNLOAD.items():
    print(f"Resolving direct URL for: {wiki_name}...")
    direct_url = get_wiki_image_url(wiki_name)
    if direct_url:
        path = os.path.join(IMAGE_DIR, local_name)
        print(f"Downloading from {direct_url} to {path}...")
        try:
            req = urllib.request.Request(direct_url, headers=headers)
            with urllib.request.urlopen(req) as response:
                with open(path, 'wb') as f:
                    f.write(response.read())
            print(f"  Successfully downloaded {local_name} ({os.path.getsize(path)} bytes)")
        except Exception as e:
            print(f"  Failed to download {local_name} from {direct_url}: {e}")
    else:
        print(f"Could not resolve URL for {wiki_name}")
EOF
