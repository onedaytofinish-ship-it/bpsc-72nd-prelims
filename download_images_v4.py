#!/usr/bin/env python3
"""Download images via Wikipedia Special:FilePath (redirects to original file).
No API calls needed — no rate limiting issues.
"""
import os
import urllib.request
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "Topics", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Special:FilePath redirects to the original full-size file on Commons
# Format: (local_filename, Commons_file_name)
FILES = [
    # Block 7: Biology
    ("human_heart.jpg", "Heart_anterior_external.jpg"),
    ("vitamin_sources.jpg", "Vitamins_diagram.svg"),
    ("food_pyramid.png", "USDA_MyPlate_green.png"),
    ("bacteria_diagram.png", "Prokaryote_cell_diagram.svg"),
    ("vaccine_vial.jpg", "Vaccination_Inside.jpg"),
    ("dna_helix.png", "DNA_Structure+Key+Labelled.pn_NoBase.png"),
    ("mendel_pea.png", "Mendels_seed_plants.svg"),
    ("photosynthesis_diagram.png", "Simple_photosynthesis.svg"),
    ("leaf_structure.png", "Leaf_anatomy.svg"),
    ("five_kingdoms.png", "Biological_classification_Linnaeus.svg"),
    ("ecosystem_diagram.png", "Energy_flow_through_ecosystem.jpg"),

    # Block 10: Ancient History
    ("mohenjodaro_great_bath.jpg", "Great_Bath_of_Mohenjodaro.jpg"),
    ("dancing_girl_mohenjodaro.jpg", "Dancing_girl_of_Mohenjodaro.jpg"),
    ("rigveda_manuscript.jpg", "Rigveda_MS2097.jpg"),
    ("ashoka_lion_capital.jpg", "Lion_Capital_of_Ashoka.jpg"),
    ("gandhara_buddha.jpg", "Standing_Buddha_Gandhara.jpg"),
    ("kushana_kanishka_coin.jpg", "KanishkaI.jpg"),
    ("iron_pillar_delhi.jpg", "Iron_pillar_of_Delhi.jpg"),
    ("nalanda_ruins.jpg", "Nalanda_University_Illustration.jpg"),
    ("mahabalipuram_temple.jpg", "Shore_Temple_Mahabalipuram.jpg"),
    ("ajanta_painting.jpg", "Ajanta_wall_painting.jpg"),
    ("sanchi_stupa.jpg", "Sanchi_Stupa.jpg"),

    # Block 15: Medieval History
    ("qutub_minar.jpg", "Qutub_Minar_View.jpg"),
    ("nizamuddin_dargah.jpg", "Nizamuddin_Dargah.jpg"),
    ("babur_portrait.jpg", "Babur_(Emperor).jpg"),
    ("akbar_portrait.jpg", "Akbar_Mughal_emperor.jpg"),
    ("shivaji_portrait.jpg", "Shivaji_portrait.jpg"),
    ("hampi_vijayanagara.jpg", "Hampi_Virupaksha_Temple.jpg"),
    ("sher_shah_tomb.jpg", "Tomb_of_Sher_Shah_Suri.jpg"),
    ("rohtas_fort.jpg", "Rohtas_Fort.jpg"),
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
    print(f"Downloading: {local_name}...", end=" ", flush=True)
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

    time.sleep(0.5)

print(f"\n=== Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed ===")