#!/usr/bin/env python3
"""Download topic-relevant images from Wikimedia Commons — with rate limiting.
Uses direct upload.wikimedia.org URLs (thumb URLs) to avoid API rate limits.
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

# Direct Wikimedia Commons thumb URLs (800px) — no API needed
# Format: (local_filename, full_wikimedia_url)
# These are constructed from known Commons file paths
FILES = [
    # Block 7: Biology
    ("cell_structure.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Animal_Cell.svg/800px-Animal_Cell.svg.png"),
    ("mitosis_diagram.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Major_events_in_mitosis.svg/600px-Major_events_in_mitosis.svg.png"),
    ("human_heart.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Heart_anterior_external.jpg/400px-Heart_anterior_external.jpg"),
    ("human_digestive_system.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Digestive_system_without_labels.svg/500px-Digestive_system_without_labels.svg.png"),
    ("vitamin_sources.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Vitamins_diagram.svg/600px-Vitamins_diagram.svg.png"),
    ("food_pyramid.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/USDA_MyPlate_green.png/400px-USDA_MyPlate_green.png"),
    ("bacteria_diagram.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Prokaryote_cell_diagram.svg/600px-Prokaryote_cell_diagram.svg.png"),
    ("vaccine_vial.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Vaccination_Inside.jpg/400px-Vaccination_Inside.jpg"),
    ("blood_cells.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Red_blood_cells.jpg/400px-Red_blood_cells.jpg"),
    ("antibody_diagram.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Antibody.svg/500px-Antibody.svg.png"),
    ("dna_helix.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBase.png/600px-DNA_Structure%2BKey%2BLabelled.pn_NoBase.png"),
    ("mendel_pea.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Mendels_seed_plants.svg/600px-Mendels_seed_plants.svg.png"),
    ("photosynthesis_diagram.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Simple_photosynthesis.svg/600px-Simple_photosynthesis.svg.png"),
    ("leaf_structure.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Leaf_anatomy.svg/600px-Leaf_anatomy.svg.png"),
    ("five_kingdoms.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Biological_classification_Linnaeus.svg/600px-Biological_classification_Linnaeus.svg.png"),
    ("ecosystem_diagram.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Energy_flow_through_ecosystem.jpg/600px-Energy_flow_through_ecosystem.jpg"),

    # Block 10: Ancient History
    ("mohenjodaro_great_bath.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Great_Bath_of_Mohenjodaro.jpg/600px-Great_Bath_of_Mohenjodaro.jpg"),
    ("dancing_girl_mohenjodaro.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Dancing_girl_of_Mohenjodaro.jpg/400px-Dancing_girl_of_Mohenjodaro.jpg"),
    ("rigveda_manuscript.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Rigveda_MS2097.jpg/400px-Rigveda_MS2097.jpg"),
    ("ashoka_lion_capital.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Lion_Capital_of_Ashoka.jpg/400px-Lion_Capital_of_Ashoka.jpg"),
    ("gandhara_buddha.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Standing_Buddha_Gandhara.jpg/400px-Standing_Buddha_Gandhara.jpg"),
    ("kushana_kanishka_coin.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/KanishkaI.jpg/400px-KanishkaI.jpg"),
    ("iron_pillar_delhi.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Iron_pillar_of_Delhi.jpg/400px-Iron_pillar_of_Delhi.jpg"),
    ("nalanda_ruins.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Nalanda_University_Illustration.jpg/600px-Nalanda_University_Illustration.jpg"),
    ("mahabalipuram_temple.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Shore_Temple_Mahabalipuram.jpg/600px-Shore_Temple_Mahabalipuram.jpg"),
    ("ajanta_painting.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Ajanta_wall_painting.jpg/600px-Ajanta_wall_painting.jpg"),
    ("sanchi_stupa.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Sanchi_Stupa.jpg/600px-Sanchi_Stupa.jpg"),

    # Block 15: Medieval History
    ("qutub_minar.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Qutub_Minar_View.jpg/400px-Qutub_Minar_View.jpg"),
    ("nizamuddin_dargah.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Nizamuddin_Dargah.jpg/600px-Nizamuddin_Dargah.jpg"),
    ("babur_portrait.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Babur_%28Emperor%29.jpg/400px-Babur_%28Emperor%29.jpg"),
    ("akbar_portrait.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Akbar_Mughal_emperor.jpg/400px-Akbar_Mughal_emperor.jpg"),
    ("shivaji_portrait.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Shivaji_portrait.jpg/400px-Shivaji_portrait.jpg"),
    ("hampi_vijayanagara.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Hampi_Virupaksha_Temple.jpg/600px-Hampi_Virupaksha_Temple.jpg"),
    ("sher_shah_tomb.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Tomb_of_Sher_Shah_Suri.jpg/600px-Tomb_of_Sher_Shah_Suri.jpg"),
    ("rohtas_fort.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Rohtas_Fort.jpg/600px-Rohtas_Fort.jpg"),
]

downloaded = 0
skipped = 0
failed = 0

for local_name, url in FILES:
    path = os.path.join(IMAGE_DIR, local_name)
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f"SKIP (exists): {local_name} ({os.path.getsize(path):,} bytes)")
        skipped += 1
        continue

    print(f"Downloading: {local_name}...", end=" ")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        size = os.path.getsize(path)
        if size < 2000:
            print(f"TOO SMALL ({size} bytes) — likely 404")
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

    time.sleep(0.3)  # gentle rate limiting

print(f"\n=== Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed ===")