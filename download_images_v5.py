#!/usr/bin/env python3
"""Retry failed downloads with corrected file names and longer delays."""
import os
import urllib.request
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "Topics", "images")

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Corrected file names for ones that 404'd + retry 429s
FILES = [
    # Corrected Commons names
    ("human_heart.jpg", "DesarguesFoxTrotHeart.jpg"),  # alternative heart image
    ("vitamin_sources.jpg", "Vitamins_diagram.svg"),
    ("food_pyramid.png", "MyPlate.png"),
    ("vaccine_vial.jpg", "Vial_of_influenza_vaccine.jpg"),
    ("dna_helix.png", "DNA_ORT_02ed02.gif"),
    ("mendel_pea.png", "Mendel-seven-characters.svg"),
    ("photosynthesis_diagram.png", "Photosynthesis.gif"),
    ("five_kingdoms.png", "Five_Kingdoms.png"),
    ("ecosystem_diagram.png", "Ecosystem_3D_diagram.jpg"),
    ("mohenjodaro_great_bath.jpg", "Mohenjodaro_The_Great_Bath.jpg"),
    ("dancing_girl_mohenjodaro.jpg", "Dancing_girl_of_Mohenjodaro.jpg"),
    ("gandhara_buddha.jpg", "Gandhara_Buddha.jpg"),
    ("nalanda_ruins.jpg", "Nalanda_01.jpg"),
    ("ajanta_painting.jpg", "Ajanta_painting.jpg"),
    # Retries for 429s
    ("sanchi_stupa.jpg", "Sanchi_Stupa.jpg"),
    ("nizamuddin_dargah.jpg", "Nizamuddin_Dargah.jpg"),
    ("hampi_vijayanagara.jpg", "Hampi_Virupaksha_Temple.jpg"),
    ("rohtas_fort.jpg", "Rohtas_Fort.jpg"),
    # Babur/Akbar - try alternate names
    ("babur_portrait.jpg", "Babur_(Padshah).jpg"),
    ("akbar_portrait.jpg", "Jalaluddin_Muhammad_Akbar.jpg"),
]

downloaded = 0
skipped = 0
failed = 0

for local_name, commons_name in FILES:
    path = os.path.join(IMAGE_DIR, local_name)
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f"SKIP (exists): {local_name} ({os.path.getsize(path):,} bytes)")
        skipped += 1
        continue

    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{commons_name}?width=800"
    print(f"Downloading: {local_name} from {commons_name}...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        size = os.path.getsize(path)
        if size < 2000:
            print(f"TOO SMALL ({size} bytes)")
            os.remove(path)
            failed += 1
        else:
            print(f"OK ({size:,} bytes)")
            downloaded += 1
    except Exception as e:
        print(f"FAILED: {e}")
        if os.path.exists(path):
            os.remove(path)
        failed += 1

    time.sleep(2.0)  # longer delay to avoid 429

print(f"\n=== Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed ===")