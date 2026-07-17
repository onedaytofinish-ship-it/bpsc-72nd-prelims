#!/usr/bin/env python3
"""
Generate all remaining Block 7 (Biology) topics (71-77) in one run.
Creates: MCQ JSON sidecar, HTML page, and subpage for each topic.
"""

import json
import os
import re
import random
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
TOPICS_DIR = os.path.join(BASE, "Topics")
MCQ_DIR = os.path.join(TOPICS_DIR, "mcq")
SUBPAGE_DIR = os.path.join(TOPICS_DIR, "subpages")

random.seed(42)

# Read template from existing topic 70
TEMPLATE_HTML = None
with open(os.path.join(TOPICS_DIR, "70_human_body_systems.html"), "r") as f:
    TEMPLATE_HTML = f.read()

# Extract CSS + JS template
CSS_START = TEMPLATE_HTML.find("<style>") 
CSS_END = TEMPLATE_HTML.find("</style>", CSS_START) + len("</style>")
CSS_BLOCK = TEMPLATE_HTML[CSS_START:CSS_END]

# Extract the home-btn style
HOME_BTN_STYLE = '<style>\n.home-btn { position: fixed; top: 12px; left: 12px; z-index: 9999; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 6px 16px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600; font-family: \'Inter\', -apple-system, sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.15); display: inline-flex; align-items: center; gap: 6px; }\n.home-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.25); }\n</style>'

# Extract JS template
JS_START = TEMPLATE_HTML.find("<script>")
JS_END = TEMPLATE_HTML.find("</script>", JS_START) + len("</script>")
JS_BLOCK = TEMPLATE_HTML[JS_START:JS_END]

# Topic definitions - concise but comprehensive
TOPICS = {
    71: {
        "slug": "71_nutrition_vitamins",
        "title": "Nutrition & Vitamins — Vitamins, Deficiency Diseases, Diet",
        "tier": "A",
        "wt": "1.0",
        "expected": "2-3 Qs",
        "bihar_tag": "Bihar: Malnutrition, ICDS, Mid-Day Meal, POSHAN Abhiyan",
        "pyq_tip": "Nutrition & Vitamins: Macronutrients (carbs, proteins, fats) + Micronutrients (vitamins, minerals). Fat-soluble vitamins: A (night blindness), D (rickets), E, K (blood clotting). Water-soluble: B-complex (beriberi B1, pellagra B3, pernicious anaemia B12), C (scurvy). Key minerals: Calcium (bones), Iron (haemoglobin/anaemia), Iodine (goitre), Zinc (immunity). Balanced diet, BMI, malnutrition. Bihar: high malnutrition, stunting, ICDS/Anganwadi, Mid-Day Meal, POSHAN Abhiyan.",
        "sections": [
            {"h3": "A. Macronutrients — Carbohydrates, Proteins, Fats", "tag": "EXAM CORE", "table": [
                ["Nutrient", "Function", "Sources", "Daily Need"],
                ["Carbohydrates", "Main energy source (4 kcal/g)", "Rice, wheat, potatoes, sugar", "~55-60% of calories"],
                ["Proteins", "Building blocks (4 kcal/g), enzymes, muscles", "Meat, fish, eggs, pulses, dairy, soy", "~10-15% of calories"],
                ["Fats", "Energy storage (9 kcal/g), insulation, hormones", "Oil, ghee, butter, nuts, fish", "~20-30% of calories"],
            ]},
            {"h3": "B. Fat-Soluble Vitamins (A, D, E, K)", "tag": "PYQ PATTERN", "table": [
                ["Vitamin", "Function", "Deficiency Disease", "Sources"],
                ["A (Retinol)", "Vision, skin, immunity", "Night blindness, xerophthalmia", "Carrot, liver, milk, eggs, yellow vegetables"],
                ["D (Calciferol)", "Calcium absorption, bone health", "Rickets (children), osteomalacia (adults)", "Sunlight, fish liver oil, milk, eggs"],
                ["E (Tocopherol)", "Antioxidant, skin health", "Rare — neurological issues", "Vegetable oils, nuts, seeds, leafy greens"],
                ["K (Phylloquinone)", "Blood clotting", "Excessive bleeding", "Leafy greens (spinach), cabbage, liver"],
            ]},
            {"h3": "C. Water-Soluble Vitamins (B-Complex, C)", "tag": "EXAM CORE", "table": [
                ["Vitamin", "Function", "Deficiency Disease", "Sources"],
                ["B1 (Thiamine)", "Carbohydrate metabolism, nerves", "Beriberi (nerve/heart damage)", "Whole grains, pulses, pork, yeast"],
                ["B2 (Riboflavin)", "Energy metabolism", "Ariboflavinosis (mouth sores)", "Milk, eggs, green vegetables"],
                ["B3 (Niacin)", "Energy metabolism", "Pellagra (3 Ds: dermatitis, diarrhoea, dementia)", "Meat, fish, peanuts, whole grains"],
                ["B6 (Pyridoxine)", "Amino acid metabolism", "Anaemia, skin issues", "Meat, fish, potatoes, bananas"],
                ["B9 (Folic acid)", "DNA synthesis, RBC formation", "Megaloblastic anaemia, birth defects", "Leafy greens, legumes, liver"],
                ["B12 (Cobalamin)", "Nerve function, RBC formation", "Pernicious anaemia", "Meat, fish, eggs, dairy (NOT in plants)"],
                ["C (Ascorbic acid)", "Collagen synthesis, immunity, antioxidant", "Scurvy (bleeding gums, weak immunity)", "Citrus fruits, amla, guava, peppers"],
            ]},
            {"h3": "D. Key Minerals", "tag": "EXAM PATTERN", "table": [
                ["Mineral", "Function", "Deficiency", "Sources"],
                ["Calcium", "Bones/teeth, muscle contraction", "Osteoporosis, rickets", "Milk, cheese, leafy greens, fish"],
                ["Iron", "Haemoglobin (O2 transport)", "Anaemia (fatigue, pale skin)", "Red meat, spinach, lentils, jaggery"],
                ["Iodine", "Thyroid hormones (metabolism)", "Goitre (enlarged thyroid)", "Iodised salt, seafood, seaweed"],
                ["Zinc", "Immunity, wound healing", "Growth retardation, weak immunity", "Meat, nuts, seeds, legumes"],
                ["Phosphorus", "Bones/teeth, ATP, DNA", "Rare (weak bones)", "Milk, meat, nuts, legumes"],
                ["Potassium", "Nerve/muscle function", "Weakness, heart issues", "Bananas, potatoes, beans"],
            ]},
        ],
        "mcqs": [
            {"q": "Which vitamin deficiency causes night blindness?", "options": ["Vitamin A (retinol — essential for vision, especially night vision)", "Vitamin C", "Vitamin D", "Vitamin B12"], "answer": 0, "explanation": "Vitamin A deficiency causes night blindness (nyctalopia) — difficulty seeing in low light. Severe deficiency → xerophthalmia (dry eyes) → blindness. Vitamin A is found in: carrots, liver, milk, eggs, yellow/orange vegetables (beta-carotene). WHO considers Vitamin A deficiency a major public health problem in developing countries.", "difficulty": "pyq"},
            {"q": "Which vitamin deficiency causes rickets (soft, weak bones in children)?", "options": ["Vitamin D (calciferol — needed for calcium absorption)", "Vitamin A", "Vitamin C", "Vitamin B1"], "answer": 0, "explanation": "Vitamin D deficiency causes rickets in children (soft, weak, deformed bones) and osteomalacia in adults (bone pain, fractures). Vitamin D helps the body absorb calcium from food. Source: sunlight (skin synthesises Vitamin D when exposed to UV), fish liver oil, fortified milk, eggs. India has high VDD despite abundant sunlight (cultural/ clothing factors).", "difficulty": "pyq"},
            {"q": "Scurvy is caused by the deficiency of which vitamin?", "options": ["Vitamin C (ascorbic acid — collagen synthesis, immunity)", "Vitamin B1", "Vitamin D", "Vitamin K"], "answer": 0, "explanation": "Scurvy is caused by Vitamin C (ascorbic acid) deficiency. Symptoms: bleeding gums, loose teeth, skin haemorrhages, weak immunity, poor wound healing. Vitamin C is essential for collagen synthesis (the main structural protein in connective tissue). Sources: citrus fruits (oranges, lemons), amla (Indian gooseberry — richest source), guava, peppers. Scurvy was common among sailors (no fresh fruits on long voyages).", "difficulty": "pyq"},
            {"q": "The disease 'beriberi' is caused by the deficiency of which vitamin?", "options": ["Vitamin B1 (thiamine — carbohydrate metabolism, nerve function)", "Vitamin B12", "Vitamin C", "Vitamin A"], "answer": 0, "explanation": "Beriberi is caused by Vitamin B1 (thiamine) deficiency. Two types: (1) wet beriberi (heart failure, oedema), (2) dry beriberi (nerve damage, muscle wasting). Common in populations eating polished white rice (thiamine is in the outer husk, removed during polishing). Found in: whole grains, pulses, pork, yeast. Eijkman discovered the cause (1929 Nobel Prize).", "difficulty": "pyq"},
            {"q": "Pellagra is caused by the deficiency of which vitamin?", "options": ["Vitamin B3 (niacin — characterised by the '3 Ds': dermatitis, diarrhoea, dementia)", "Vitamin B1", "Vitamin C", "Vitamin D"], "answer": 0, "explanation": "Pellagra is caused by Vitamin B3 (niacin) deficiency. Classic '3 Ds': Dermatitis (skin rash, especially on sun-exposed areas), Diarrhoea, Dementia (confusion, memory loss). If untreated, the 4th D = Death. Common in maize-eating populations (maize has niacin in a bound form not easily absorbed). Sources: meat, fish, peanuts, whole grains. Pellagra was epidemic in the US South (early 1900s).", "difficulty": "pyq"},
            {"q": "Pernicious anaemia is caused by the deficiency of which vitamin?", "options": ["Vitamin B12 (cobalamin — needed for RBC formation; absorption requires intrinsic factor)", "Vitamin B9 (folic acid)", "Iron", "Vitamin C"], "answer": 0, "explanation": "Pernicious anaemia is caused by Vitamin B12 (cobalamin) deficiency. B12 is needed for RBC formation and nerve function. It's only found in animal products (meat, fish, eggs, dairy) — NOT in plant foods. Vegans are at risk. B12 absorption requires 'intrinsic factor' (produced by the stomach). Without it, B12 cannot be absorbed → pernicious anaemia (large, immature RBCs). Treatment: B12 injections.", "difficulty": "bpsc"},
            {"q": "Goitre (enlarged thyroid gland) is caused by the deficiency of which mineral?", "options": ["Iodine (needed for thyroid hormone synthesis — regulates metabolism)", "Iron", "Calcium", "Zinc"], "answer": 0, "explanation": "Goitre (enlarged thyroid gland) is caused by iodine deficiency. Iodine is essential for the thyroid gland to produce hormones (T3, T4) that regulate metabolism. Without enough iodine, the thyroid enlarges (goitre) trying to compensate. Severe deficiency in pregnancy → cretinism (mental retardation in baby). Prevention: iodised salt (National Iodine Deficiency Disorders Control Programme, 1992). Sources: iodised salt, seafood, seaweed.", "difficulty": "pyq"},
            {"q": "Iron deficiency in the human body leads to which condition?", "options": ["Anaemia (low haemoglobin → fatigue, pale skin, shortness of breath)", "Goitre", "Rickets", "Scurvy"], "answer": 0, "explanation": "Iron deficiency causes anaemia — the most common nutritional deficiency worldwide. Iron is the core component of haemoglobin (the protein in RBCs that carries oxygen). Without enough iron, the body cannot produce enough haemoglobin → RBCs are small and pale → reduced oxygen transport → fatigue, pale skin, shortness of breath. Sources: red meat, liver, spinach, lentils, jaggery, dates. Vitamin C enhances iron absorption.", "difficulty": "pyq"},
            {"q": "Vitamin K is essential for which bodily function?", "options": ["Blood clotting (coagulation — activates clotting factors)", "Vision", "Bone growth", "Immunity"], "answer": 0, "explanation": "Vitamin K is essential for blood clotting (coagulation). It activates clotting factors (proteins that stop bleeding). Without Vitamin K, even small cuts would bleed excessively. Vitamin K is also important for bone health. Sources: leafy green vegetables (spinach, kale, cabbage), liver, vegetable oils. Newborns are given Vitamin K injections at birth (they don't have enough yet). 'K' comes from the German 'Koagulation.'", "difficulty": "bpsc"},
            {"q": "Which vitamin is produced by the human skin when exposed to sunlight?", "options": ["Vitamin D (skin synthesises calciferol when exposed to UV-B radiation)", "Vitamin A", "Vitamin C", "Vitamin E"], "answer": 0, "explanation": "Vitamin D is synthesised by the skin when exposed to sunlight (UV-B radiation). The skin converts 7-dehydrocholesterol to Vitamin D3 (cholecalciferol). ~15-30 minutes of sunlight exposure on face and arms, 2-3 times/week, is usually sufficient. Despite abundant sunlight in India, Vitamin D deficiency is common (cultural clothing, indoor lifestyle, pollution). Vitamin D is both a vitamin and a hormone.", "difficulty": "pyq"},
            {"q": "Which of the following is the richest source of Vitamin C?", "options": ["Amla (Indian gooseberry — ~600-700 mg/100g, one of the richest natural sources)", "Orange", "Lemon", "Apple"], "answer": 0, "explanation": "Amla (Indian gooseberry, Phyllanthus emblica) is one of the richest natural sources of Vitamin C (~600-700 mg per 100g — ~20 times more than an orange). Amla is used in Ayurveda (Chyawanprash) and is a key ingredient in many Indian remedies. Other good sources: guava (~228 mg), peppers, citrus fruits. Vitamin C is water-soluble, cannot be stored, must be consumed daily.", "difficulty": "bpsc"},
            {"q": "How many calories are produced per gram of fat in the human body?", "options": ["9 kcal/g (fats provide the most energy per gram — more than 2x carbs/proteins)", "4 kcal/g", "7 kcal/g", "2 kcal/g"], "answer": 0, "explanation": "Fats provide 9 kcal per gram — the highest energy density of all macronutrients. Carbohydrates and proteins each provide 4 kcal/g. Alcohol provides 7 kcal/g (not a nutrient). This is why high-fat foods (oil, ghee, nuts, butter) are calorie-dense. Fats are essential for: energy storage, insulation, hormone production, absorption of fat-soluble vitamins (A, D, E, K).", "difficulty": "bpsc"},
            {"q": "The BMI (Body Mass Index) is calculated using which formula?", "options": ["Weight (kg) / Height² (m²) — normal range is 18.5-24.9", "Weight / Height", "Height / Weight²", "Weight × Height"], "answer": 0, "explanation": "BMI = Weight (kg) / Height (m)². Categories: Underweight <18.5, Normal 18.5-24.9, Overweight 25-29.9, Obese ≥30. BMI is a quick screening tool but doesn't distinguish between muscle and fat. A very muscular person may have high BMI but low body fat. BMI is widely used in health assessments, insurance, and public health surveys.", "difficulty": "bpsc"},
            {"q": "Which vitamin deficiency in pregnant women can cause neural tube defects (spina bifida) in the baby?", "options": ["Vitamin B9 / Folic acid (essential for neural tube development in early pregnancy)", "Vitamin C", "Vitamin D", "Vitamin B12"], "answer": 0, "explanation": "Folic acid (Vitamin B9) deficiency in early pregnancy can cause neural tube defects (NTDs) — such as spina bifida (spine doesn't close properly) and anencephaly (brain doesn't develop). The neural tube closes in the first 28 days of pregnancy (often before a woman knows she's pregnant). WHO recommends 400 μg folic acid daily for women of childbearing age. Sources: leafy greens, legumes, fortified grains.", "difficulty": "bpsc"},
            {"q": "Which mineral is most important for bone and teeth formation?", "options": ["Calcium (the most abundant mineral in the body — 99% stored in bones/teeth)", "Iron", "Iodine", "Sodium"], "answer": 0, "explanation": "Calcium is the most abundant mineral in the human body (~1.2 kg in an adult). 99% is stored in bones and teeth (providing structural strength). Calcium is also essential for: muscle contraction, nerve signalling, blood clotting, and enzyme activation. Vitamin D is needed for calcium absorption. Sources: milk, cheese, yogurt, leafy greens, fish with bones. Deficiency → osteoporosis (brittle bones).", "difficulty": "pyq"},
            {"q": "Proteins are made up of which smaller building blocks?", "options": ["Amino acids (20 standard amino acids; 9 are 'essential' — must come from diet)", "Fatty acids", "Glucose molecules", "Nucleotides"], "answer": 0, "explanation": "Proteins are made of amino acids. There are 20 standard amino acids. 9 are 'essential' (the body cannot synthesise them — must come from diet): histidine, isoleucine, leucine, lysine, methionine, phenylalanine, threonine, tryptophan, valine. Animal proteins (meat, eggs, dairy) are 'complete' (all 9 essential amino acids). Most plant proteins are 'incomplete' (lack one or more) — exception: soy and quinoa are complete.", "difficulty": "bpsc"},
            {"q": "Which of the following is a 'complete protein' (containing all 9 essential amino acids)?", "options": ["Eggs (animal protein — complete; soy and quinoa are the main plant-based complete proteins)", "Rice", "Wheat", "Lentils"], "answer": 0, "explanation": "Eggs are a 'complete protein' — containing all 9 essential amino acids in the right proportions. Animal proteins (meat, fish, eggs, dairy) are generally complete. Most plant proteins are 'incomplete' (lacking one or more essential amino acids). EXCEPTIONS: soy (and soy products like tofu) and quinoa are complete plant proteins. Combining grains + legumes (e.g., rice + dal) also provides all essential amino acids.", "difficulty": "tricky"},
            {"q": "The National Iodine Deficiency Disorders Control Programme (NIDDCP) in India primarily promotes:", "options": ["Use of iodised salt (to prevent goitre and cretinism)", "Iron supplementation", "Vitamin A supplementation", "Calcium supplementation"], "answer": 0, "explanation": "The NIDDCP (launched 1992, revised name) promotes the use of iodised salt to prevent iodine deficiency disorders (IDD): goitre, cretinism (mental retardation), and hypothyroidism. India mandates iodised salt for direct human consumption. Despite this, IDD remains a problem in some areas (especially hilly regions where soil iodine is low). Bihar has IDD-prone districts. Universal Salt Iodisation (USI) is the global strategy.", "difficulty": "bpsc"},
            {"q": "The '3 Ds' of pellagra (Vitamin B3/niacin deficiency) are:", "options": ["Dermatitis, Diarrhoea, Dementia (the 4th D is Death if untreated)", "Dryness, Dizziness, Deafness", "Diabetes, Dental decay, Dementia", "Deformity, Diarrhoea, Deafness"], "answer": 0, "explanation": "The '3 Ds' of pellagra: Dermatitis (skin rash on sun-exposed areas), Diarrhoea (gastrointestinal), Dementia (confusion, memory loss). The 4th D = Death (if untreated). Pellagra is caused by Vitamin B3 (niacin) deficiency. Common in maize-eating populations. The disease was epidemic in the US South (1900s) until Goldberger discovered the dietary cause (niacin). Sources: meat, fish, peanuts, whole grains.", "difficulty": "tricky"},
            {"q": "Which vitamin is a powerful antioxidant that protects cells from oxidative damage?", "options": ["Vitamin E (tocopherol — protects cell membranes from free radical damage)", "Vitamin B1", "Vitamin K", "Vitamin B12"], "answer": 0, "explanation": "Vitamin E (tocopherol) is a powerful antioxidant. It protects cell membranes from oxidative damage caused by free radicals (reactive oxygen species). Free radicals damage cells and are linked to ageing, cancer, and heart disease. Vitamin E is fat-soluble — stored in fat tissues. Sources: vegetable oils (sunflower, safflower), nuts (almonds), seeds, leafy greens. Vitamin C is also an antioxidant (water-soluble).", "difficulty": "bpsc"},
            {"q": "The Mid-Day Meal Scheme in India provides meals to which group?", "options": ["School children (Class 1-8 in government and government-aided schools)", "Pregnant women", "Elderly people", "Hospital patients"], "answer": 0, "explanation": "The Mid-Day Meal Scheme (MDMS) provides free meals to school children (Class 1-8) in government and government-aided schools. Launched in 1995 (revised 2004), it is the world's largest school feeding programme (~12 crore children). Objectives: (1) improve nutrition, (2) increase school enrolment and attendance, (3) reduce dropout rates. Bihar implemented MDMS across all schools. The meal provides ~450 kcal (primary) and ~700 kcal (upper primary) per child per day.", "difficulty": "bpsc"},
            {"q": "POSHAN Abhiyan (National Nutrition Mission) was launched in which year?", "options": ["2018 (by PM Modi — aims to reduce stunting, undernutrition, and anaemia in children and women)", "2010", "2015", "2020"], "answer": 0, "explanation": "POSHAN Abhiyan (Prime Minister's Overarching Scheme for Holistic Nutrition) was launched in March 2018. Targets (by 2022): reduce stunting in children 0-6 years (from 38.4% to 25%), reduce undernutrition, reduce anaemia in children and women. It uses a 'convergence' approach — bringing together ICDS, Health, Water/Sanitation, and Agriculture departments. Bihar is a high-priority state for POSHAN (high malnutrition rates). March is celebrated as POSHAN Maah (nutrition month).", "difficulty": "bpsc"},
            {"q": "Which Indian food is the richest plant-based source of iron?", "options": ["Jaggery (gur — traditional unrefined sugar, ~11 mg iron/100g)", "Rice", "Wheat", "Apple"], "answer": 0, "explanation": "Jaggery (gur) is one of the richest plant-based sources of iron (~11 mg per 100g). It is a traditional Indian sweetener made from sugarcane juice (or date palm). Jaggery also contains other minerals (calcium, magnesium, potassium). In Bihar and other states, jaggery is traditionally given to anaemic women and children. Other good plant sources of iron: spinach, lentils, dates, raisins. Vitamin C enhances iron absorption from plant sources.", "difficulty": "tricky"},
            {"q": "The condition 'kwashiorkor' is caused by:", "options": ["Severe protein deficiency (adequate calories but insufficient protein — swollen belly, oedema)", "Vitamin A deficiency", "Excess fat consumption", "Iron deficiency"], "answer": 0, "explanation": "Kwashiorkor is a form of severe malnutrition caused by protein deficiency (with adequate calorie intake). Symptoms: swollen belly (oedema — fluid accumulation), fatty liver, hair depigmentation, skin lesions, apathy. It typically occurs in children aged 1-4 (weaned from breast milk to a starch-only diet). The name comes from the Ga language of Ghana ('the sickness the older child gets when the next baby is born'). Treatment: gradual refeeding with protein. Marasmus = combined protein + calorie deficiency.", "difficulty": "tricky"},
            {"q": "The condition 'marasmus' differs from kwashiorkor in that marasmus is caused by:", "options": ["Deficiency of both calories AND protein (severe weight loss, 'old person' appearance)", "Protein deficiency only", "Vitamin deficiency only", "Excess calorie intake"], "answer": 0, "explanation": "Marasmus is caused by deficiency of BOTH calories and protein (energy-protein malnutrition). Symptoms: severe weight loss, muscle wasting, 'old person' face, dry skin, no oedema (unlike kwashiorkor). Occurs in infants (often <1 year) who are weaned early or given diluted food. Kwashiorkor = protein deficiency with adequate calories (swollen belly). Marasmus = both protein and calorie deficiency (wasted appearance). Both are forms of Severe Acute Malnutrition (SAM).", "difficulty": "tricky"},
        ],
        "bihar_title": "Bihar — Malnutrition, ICDS, POSHAN Abhiyan",
        "bihar_points": [
            "Malnutrition in Bihar: Bihar has high rates of child malnutrition — stunting (~42%), wasting (~22%), underweight (~33%) (NFHS-5, 2019-21). These rates are above the national average. Malnutrition affects cognitive development, immunity, and future productivity. Bihar's high malnutrition is linked to poverty, poor maternal health, inadequate feeding practices, and limited access to healthcare.",
            "ICDS (Integrated Child Development Services) in Bihar: ICDS provides supplementary nutrition, health check-ups, immunisation, and pre-school education to children 0-6 years and pregnant/lactating women through Anganwadi centres. Bihar has ~80,000+ Anganwadi centres. ICDS is the world's largest early childhood development programme. In Bihar, ICDS is crucial for combating malnutrition.",
            "Mid-Day Meal Scheme (Bihar): Bihar serves mid-day meals to ~1.5 crore children in government schools. The scheme provides ~450-700 kcal per child per day. Bihar has faced challenges in implementation (quality, hygiene, infrastructure) but the scheme has improved school enrolment and nutrition. In 2013, a tragedy in Saran district (23 children died after eating contaminated mid-day meal) led to stronger safety protocols.",
            "POSHAN Abhiyan in Bihar: Bihar is a high-priority state for POSHAN Abhiyan (launched 2018). The scheme targets reducing stunting, undernutrition, and anaemia. Bihar's high malnutrition makes POSHAN implementation critical. The scheme uses Anganwadi centres and community-based approaches. March is celebrated as POSHAN Maah in Bihar with awareness campaigns.",
            "Anaemia in Bihar: anaemia is extremely prevalent in Bihar — ~63% of children 6-59 months and ~63% of women 15-49 are anaemic (NFHS-5). Iron deficiency is the main cause. Government programmes: Iron-Folic Acid (IFA) supplementation for pregnant women and adolescents, weekly IFA tablets in schools. Bihar's anaemia rates are among the highest in India.",
            "Iodine deficiency in Bihar: several districts in Bihar (especially in the northern/Gangetic plains) are iodine-deficient. Goitre was historically common. The National Iodine Deficiency Disorders Control Programme promotes iodised salt in Bihar. Despite progress, non-iodised salt is still used in some rural areas of Bihar.",
        ],
    },
}

# Generate a single topic
def generate_topic(num, data):
    slug = data["slug"]
    title = data["title"]
    
    # Generate JSON sidecar
    json_data = []
    for mcq in data["mcqs"]:
        json_data.append({
            "q": mcq["q"],
            "options": mcq["options"],
            "answer": mcq["answer"],
            "explanation": mcq["explanation"],
            "difficulty": mcq.get("difficulty", "bpsc"),
            "pyq_ref": mcq.get("pyq_ref", None)
        })
    
    json_path = os.path.join(MCQ_DIR, f"{slug}.json")
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Generate HTML
    html = generate_html(num, data, slug, title)
    html_path = os.path.join(TOPICS_DIR, f"{slug}.html")
    with open(html_path, "w") as f:
        f.write(html)
    
    # Generate subpage
    subpage = generate_subpage(num, data, slug, title)
    subpage_path = os.path.join(SUBPAGE_DIR, f"{slug}_detail.html")
    with open(subpage_path, "w") as f:
        f.write(subpage)
    
    print(f"  ✓ Topic {num}: {slug} (JSON + HTML + subpage created)")


def generate_html(num, data, slug, title):
    sections_html = ""
    
    # PYQ box
    sections_html += f'''  <div class="pyq-box">
    <span class="pyq-tag">EXAM TIP</span>
    <strong>{data["pyq_tip"]}</strong>
  </div>

'''
    
    # Images
    sections_html += '''  <div class="img-container">
    <img src="images/bhimbetka.jpg" alt="Biology and nutrition — the science of life">
    <div class="img-caption">Nutrition and vitamins are fundamental to human health. Understanding macronutrients (carbohydrates, proteins, fats) and micronutrients (vitamins, minerals) — and their deficiency diseases — is essential for BPSC and for public health awareness.</div>
  </div>

  <div class="img-container">
    <img src="images/mahavir_mandir_patna.jpg" alt="Bihar's nutrition programmes — ICDS, Mid-Day Meal, POSHAN">
    <div class="img-caption">Bihar faces significant malnutrition challenges — high rates of stunting, wasting, anaemia, and iodine deficiency. Government programmes like ICDS (Anganwadi), Mid-Day Meal, and POSHAN Abhiyan are working to address these challenges across Bihar.</div>
  </div>

'''
    
    # Subpage box
    sections_html += f'''  <div class="subpage-box">
    <strong>💡 Deep-dive ready:</strong> Complete analysis of all vitamins, minerals, deficiency diseases, Bihar nutrition programmes, and 7 exam predictions:
    <a href="subpages/{slug}_detail.html" target="_blank">{title.split("—")[0].strip()} Master Detail →</a>
  </div>

'''
    
    # Section tables
    for sec in data["sections"]:
        table_rows = ""
        for i, row in enumerate(sec["table"]):
            if i == 0:
                table_rows += "    <tr>" + "".join(f"<th>{cell}</th>" for cell in row) + "</tr>\n"
            else:
                table_rows += "    <tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>\n"
        
        sections_html += f'''  <h3>{sec["h3"]} <span class="current-tag">{sec["tag"]}</span></h3>
  <table>
{table_rows}  </table>

'''
    
    # Bihar connection
    bihar_items = "".join(f"      <li>{bp}</li>\n" for bp in data["bihar_points"])
    sections_html += f'''  <div class="bihar-box">
    <div class="bihar-box-title">{data["bihar_title"]}</div>
    <ul>
{bihar_items}    </ul>
  </div>
</div>

'''
    
    # MCQ section
    mcqs_html = ""
    for i, mcq in enumerate(data["mcqs"], 1):
        options_html = ""
        for j, opt in enumerate(mcq["options"]):
            letter = chr(97 + j)
            cap_letter = chr(65 + j)
            options_html += f'      <label class="mcq-option"><input type="radio" name="q{i}" value="{letter}"> {cap_letter}. {opt}</label>\n'
        
        mcqs_html += f'''  <div class="mcq-block" id="q{i}">
    <div class="mcq-q">Q{i}. {mcq["q"]}</div>
    <div class="mcq-options">
{options_html}    </div>
    <div class="mcq-explanation" id="exp{i}">✅ <strong>Correct Answer: (A)</strong> — {mcq["explanation"]}</div>
  </div>

'''
    
    # Build answers object (all 'a' initially, will be shuffled later)
    ans_parts = [f"q{i}: 'a'" for i in range(1, 26)]
    answers_js = ", ".join(ans_parts[:10]) + ",\n  " + ", ".join(ans_parts[10:20]) + ",\n  " + ", ".join(ans_parts[20:])
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{num} - {title.split("—")[0].strip()} | BPSC 72nd Prelims</title>
{CSS_BLOCK}
</head>
<body>
{HOME_BTN_STYLE}
<a href="index.html" class="home-btn">🏠 Home</a>
<a href="index.html" style="display: inline-block; margin-bottom: 20px; color: #2563eb; text-decoration: none; font-weight: 600; font-size: 13px;">← Back to Master Dashboard</a>

<div class="topic-header">
  <div class="topic-number">TOPIC #{num} • TIER {data["tier"]}</div>
  <div class="topic-title">{title}</div>
  <div class="topic-meta">
    <span class="meta-tag">📂 Biology</span>
    <span class="meta-tag">⚖️ Weight: {data["wt"]}</span>
    <span class="meta-tag">🎯 Expected: {data["expected"]}</span>
    <span class="meta-tag">🔶 {data["bihar_tag"]}</span>
  </div>
</div>

<div class="section">
  <div class="section-header"><span class="section-icon">📚</span> Core Content</div>

{sections_html}<div class="section">
  <div class="section-header"><span class="section-icon">✍️</span> MCQ Practice Set — 25 Questions (BPSC Level)</div>
  <p style="font-size:13px; color:#64748b; margin-bottom:16px;">Test your knowledge. Select the best answer for each question, then click "Check Answers" to see your score and explanations.</p>

  <div class="quiz-controls">
    <button class="check-btn" onclick="checkAnswers()">Check Answers</button>
    <button class="reset-btn" onclick="resetQuiz()">Reset</button>
  </div>
  <div class="score-display" id="scoreDisplay">
    Your Score: <span class="score-num" id="scoreNum">0/25</span>
  </div>

{mcqs_html}</div>

<div class="section">
  <div class="section-header"><span class="section-icon">📖</span> References</div>
  <ul class="ref-list">
    <li>NCERT Biology, Class 10 &amp; 11 — Nutrition, Digestion</li>
    <li>NCERT Science, Class 7 &amp; 9 — Nutrition in Animals and Plants</li>
    <li>WHO Nutrition Guidelines</li>
    <li><a href="https://en.wikipedia.org/wiki/Vitamin" target="_blank">Wikipedia: Vitamins</a></li>
  </ul>
</div>

<div class="doc-footer">BPSC 72nd Prelims • Topic {num} — {title.split("—")[0].strip()} • Generated 2026-07-18</div>

<script>
const answers = {{
  {answers_js}
}};
{JS_BLOCK[JS_BLOCK.find("function checkAnswers"):]}
</body>
</html>'''
    
    return full_html


def generate_subpage(num, data, slug, title):
    # Simple subpage with key facts
    sections = ""
    for sec in data["sections"]:
        table_rows = ""
        for i, row in enumerate(sec["table"]):
            if i == 0:
                table_rows += "    <tr>" + "".join(f"<th>{cell}</th>" for cell in row) + "</tr>\n"
            else:
                table_rows += "    <tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>\n"
        sections += f'  <h3>{sec["h3"]}</h3>\n  <table>\n{table_rows}  </table>\n\n'
    
    bihar_items = "".join(f"    <li>{bp}</li>\n" for bp in data["bihar_points"])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{num} Deep Dive — {title.split("—")[0].strip()} | BPSC 72nd Prelims</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', -apple-system, sans-serif; background: #fff; color: #1a1a2e; line-height: 1.7; font-size: 14px; padding: 20px; max-width: 900px; margin: 0 auto; }}
  .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 24px 28px; border-radius: 14px; margin-bottom: 24px; }}
  .header h1 {{ font-size: 22px; font-weight: 800; margin-bottom: 6px; }}
  .header .subtitle {{ font-size: 13px; opacity: 0.85; }}
  .section {{ margin-bottom: 24px; }}
  .section h2 {{ font-size: 18px; font-weight: 700; color: #1a1a2e; border-bottom: 3px solid #e94560; padding-bottom: 8px; margin-bottom: 14px; }}
  h3 {{ font-size: 15px; font-weight: 700; color: #16213e; margin: 14px 0 8px; padding-left: 12px; border-left: 4px solid #e94560; }}
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }}
  th {{ background: #1a1a2e; color: #fff; padding: 10px 12px; text-align: left; font-weight: 600; font-size: 12px; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #e8e8e8; }}
  tr:nth-child(even) {{ background: #f8f9fa; }}
  .bihar-box {{ background: linear-gradient(135deg, #fff5f0, #ffe8dd); border-left: 5px solid #ff6b35; padding: 16px 20px; border-radius: 0 12px 12px 0; margin: 16px 0; }}
  .home-btn {{ position: fixed; top: 12px; left: 12px; z-index: 9999; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 6px 16px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600; font-family: 'Inter', sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.15); display: inline-flex; align-items: center; gap: 6px; }}
  .back-link {{ display: inline-block; margin-bottom: 16px; color: #2563eb; text-decoration: none; font-weight: 600; font-size: 13px; }}
</style>
</head>
<body>
<style>.home-btn {{ position: fixed; top: 12px; left: 12px; z-index: 9999; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 6px 16px; border-radius: 8px; text-decoration: none; font-size: 13px; font-weight: 600; font-family: 'Inter', sans-serif; box-shadow: 0 2px 8px rgba(0,0,0,0.15); display: inline-flex; align-items: center; gap: 6px; }}</style>
<a href="../index.html" class="home-btn">🏠 Home</a>
<a href="../{slug}.html" class="back-link">← Back to Topic {num}</a>

<div class="header">
  <h1>Topic {num} — {title.split("—")[0].strip()}: Deep Dive</h1>
  <div class="subtitle">{title.split("—")[1].strip() if "—" in title else ""}</div>
</div>

<div class="section">
  <h2>1. Key Tables — Vitamins, Minerals, Deficiency Diseases</h2>
{sections}</div>

<div class="section">
  <h2>2. Bihar Connection</h2>
  <div class="bihar-box">
    <div style="font-weight: 700; color: #ff6b35; font-size: 15px; margin-bottom: 8px;">{data["bihar_title"]}</div>
    <ul>
{bihar_items}    </ul>
  </div>
</div>

<div class="section">
  <h2>3. Exam Prediction Summary</h2>
  <ul>
    <li><strong>Most likely (HIGH):</strong> Vitamin-deficiency disease matches (A=night blindness, D=rickets, C=scurvy, B1=beriberi, B3=pellagra, B12=pernicious anaemia, K=blood clotting)</li>
    <li><strong>Likely (MEDIUM):</strong> Minerals (iron=anaemia, iodine=goitre, calcium=bones), BMI formula, Vitamin D from sunlight, fat-soluble vs water-soluble vitamins</li>
    <li><strong>Possible (LOW):</strong> Bihar nutrition programmes (ICDS, MDMS, POSHAN), kwashiorkor/marasmus, folic acid in pregnancy, complete/incomplete proteins</li>
  </ul>
</div>

</body>
</html>'''


def main():
    print("=" * 60)
    print("Generating Block 7 remaining topics (71-77)")
    print("=" * 60)
    
    # For now, only topic 71 is defined - the rest will be added incrementally
    for num, data in sorted(TOPICS.items()):
        generate_topic(num, data)
    
    print("\nDone! Now run shuffle_answers_v2.py and qa_check.py")


if __name__ == "__main__":
    main()