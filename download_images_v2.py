#!/usr/bin/env python3
"""Download topic-relevant images from Wikipedia/Wikimedia Commons for Blocks 7, 10, 15.
Fixes the image mismatch issue identified in the audit.
"""
import os
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

IMAGE_DIR = os.path.join(os.path.dirname(__file__), "Topics", "images")
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_wiki_image_url(filename):
    """Resolve a Wikipedia File: name to a direct upload.wikimedia.org URL."""
    query_url = (
        "https://en.wikipedia.org/w/api.php?action=query"
        "&titles=File:" + urllib.parse.quote(filename) +
        "&prop=imageinfo&iiprop=url&format=json"
    )
    headers = {'User-Agent': 'BPSC_Topics_Downloader/1.0 (educational project)'}
    req = urllib.request.Request(query_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data['query']['pages']
            for page_id in pages:
                if 'imageinfo' in pages[page_id]:
                    return pages[page_id]['imageinfo'][0]['url']
    except Exception as e:
        print(f"  Error fetching metadata for {filename}: {e}")
    return None

# (local_filename, Wikipedia_File_name) — curated for topical relevance
FILES_TO_DOWNLOAD = [
    # === Block 7: Biology (69-72) ===
    # Topic 69 — Cell division
    ("cell_structure.png", "Animal Cell.svg"),
    ("mitosis_diagram.png", "Major_events_in_mitosis.svg"),
    # Topic 70 — Human body systems
    ("human_heart.jpg", "Heart_anterior_external.jpg"),
    ("human_digestive_system.png", "Digestive_system_without_labels.svg"),
    # Topic 71 — Nutrition and vitamins
    ("vitamin_chart.png", "Vitamins_diagram.svg"),
    ("food_pyramid.png", "MyPlate.png"),
    # Topic 72 — Diseases and pathogens
    ("bacteria_diagram.png", "Gram_Stain_Animated.gif"),
    ("vaccine_vial.jpg", "Vaccine_vial_and_syringe.jpg"),
    # Topic 73 — Blood, immunity, vaccines
    ("blood_cells.jpg", "Red_blood_cells.jpg"),
    ("antibody_diagram.png", "Antibody.svg"),
    # Topic 74 — Genetics
    ("dna_double_helix.png", "DNA_Structure+Key+Labelled.pn_NoBase.png"),
    ("mendel_pea.png", "Mendels_seed_plants.svg"),
    # Topic 75 — Plant physiology
    ("photosynthesis_diagram.png", "Simple_photosynthesis.svg"),
    ("leaf_structure.png", "Leaf_anatomy.svg"),
    # Topic 76 — Classification
    ("five_kingdoms.png", "Biological_classification_Linnaeus.svg"),
    ("bacteria_microscope.jpg", "EscherichiaColi_NIAID.jpg"),
    # Topic 77 — Biotech and ecology
    ("ecosystem_diagram.png", "Energy_flow_through_ecosystem.jpg"),
    ("crispr_diagram.png", "CRISPR_Cas9_Overview.jpg"),

    # === Block 10: Ancient History (97-106) ===
    # Topic 97 — Prehistory (already has correct images, but adding one more)
    ("stone_age_tools_detail.jpg", "Flint_tools_DS50.jpg"),
    # Topic 98 — Indus Valley
    ("mohenjodaro_great_bath.jpg", "Great_Bath_of_Mohenjodaro.jpg"),
    ("dancing_girl_mohenjodaro.jpg", "Dancing_girl_of_Mohenjodaro.jpg"),
    # Topic 99 — Vedic Age
    ("vedic_altar.png", "Vedic_fire_altar.png"),
    ("rigveda_manuscript.jpg", "Rigveda_MS2097.jpg"),
    # Topic 100 — Mahajanapadas
    ("pataliputra_ruins.jpg", "Pataliputra_ruins.jpg"),
    ("magadha_map.png", "Magadha_ancient_boundaries.png"),
    # Topic 101 — Buddhism & Jainism (already correct, adding one)
    ("sarnath_lion_capital.jpg", "Lion_Capital_of_Ashoka.jpg"),
    # Topic 102 — Mauryan Empire
    ("ashoka_pillar_sarnath.jpg", "Lion_Capital_of_Ashoka.jpg"),
    ("chandragupta_maurya.jpg", "Chandragupta_Maurya_artistic_depiction.jpg"),
    # Topic 103 — Post-Mauryan
    ("gandhara_buddha.jpg", "Standing_Buddha_Gandhara.jpg"),
    ("kushana_coin.jpg", "KanishkaI.jpg"),
    # Topic 104 — Gupta Empire
    ("iron_pillar_delhi.jpg", "Iron_pillar_of_Delhi.jpg"),
    ("nalanda_university.jpg", "Nalanda_University_Illustration.jpg"),
    # Topic 105 — Post-Gupta & Sangam
    ("harsha_coin.jpg", "Harsha_Vardhana_coin.jpg"),
    ("mahabalipuram_shore_temple.jpg", "Shore_Temple_Mahabalipuram.jpg"),
    # Topic 106 — Art & Literature
    ("ajanta_painting.jpg", "Ajanta_wall_painting.jpg"),
    ("sanchi_stupa.jpg", "Sanchi_Stupa.jpg"),

    # === Block 15: Medieval History (137-142) ===
    # Topic 137 — Early medieval (Rajputs, Cholas)
    ("rajput_warrior.jpg", "Rajput_warrior_painting.jpg"),
    ("chola_map.png", "Chola_Dynasty_map.png"),
    # Topic 138 — Delhi Sultanate
    ("qutub_minar.jpg", "Qutub_Minar_View.jpg"),
    ("alauddin_khalji.jpg", "Alauddin_Khalji.jpg"),
    # Topic 139 — Bhakti & Sufi
    ("nizamuddin_dargah.jpg", "Nizamuddin_Dargah.jpg"),
    ("kabir_das.jpg", "Kabir.jpg"),
    # Topic 140 — Mughal Empire
    ("babur_portrait.jpg", "Babur_(Emperor).jpg"),
    ("akbar_portrait.jpg", "Akbar_Mughal_emperor.jpg"),
    # Topic 141 — South & Marathas
    ("shivaji_portrait.jpg", "Shivaji_portrait.jpg"),
    ("vijayanagara_ruins.jpg", "Hampi_Virupaksha_Temple.jpg"),
    # Topic 142 — Bihar Medieval (Sher Shah Suri)
    ("sher_shah_tomb.jpg", "Sher_Shah_Suri_Tomb_Sasaram.jpg"),
    ("rohtas_fort.jpg", "Rohtas_Fort.jpg"),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

downloaded = 0
skipped = 0
failed = 0

for local_name, wiki_name in FILES_TO_DOWNLOAD:
    path = os.path.join(IMAGE_DIR, local_name)
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        print(f"SKIP (exists): {local_name}")
        skipped += 1
        continue

    print(f"Resolving: {wiki_name}...")
    direct_url = get_wiki_image_url(wiki_name)
    if direct_url:
        print(f"  Downloading → {path}")
        try:
            req = urllib.request.Request(direct_url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(path, 'wb') as f:
                    f.write(response.read())
            size = os.path.getsize(path)
            if size < 1000:
                print(f"  WARNING: {local_name} only {size} bytes (likely error page)")
                os.remove(path)
                failed += 1
            else:
                print(f"  OK: {local_name} ({size:,} bytes)")
                downloaded += 1
        except Exception as e:
            print(f"  FAILED download {local_name}: {e}")
            failed += 1
    else:
        print(f"  Could not resolve URL for {wiki_name}")
        failed += 1

print(f"\n=== Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed ===")