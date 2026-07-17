#!/usr/bin/env python3
"""
Shuffle MCQ answer keys across A/B/C/D for Block 10 topics (97-106).

This script:
1. Reads each MCQ JSON sidecar (mcq/NN_topic.json)
2. For each question, randomly shuffles the options
3. Updates the 'answer' field to the new position of the correct option
4. Writes back the JSON
5. Updates the HTML file:
   a. Re-orders the option labels (A/B/C/D) to match the shuffled options
   b. Updates the `const answers = {...}` block
   c. Updates the explanation text "Correct Answer: (X)"
   d. Updates the option text in the HTML labels
"""

import json
import os
import re
import random

random.seed(42)  # Reproducible shuffle

TOPICS_DIR = os.path.join(os.path.dirname(__file__), "Topics")
MCQ_DIR = os.path.join(TOPICS_DIR, "mcq")

# Map of topic number -> JSON filename
TOPIC_FILES = {
    97: "97_prehistory.json",
    98: "98_indus_valley.json",
    99: "99_vedic_age.json",
    100: "100_mahajanapadas.json",
    101: "101_buddhism_jainism.json",
    102: "102_mauryan_empire.json",
    103: "103_post_mauryan.json",
    104: "104_gupta_empire.json",
    105: "105_post_gupta_sangam.json",
    106: "106_art_literature.json",
}

# Map of topic number -> HTML filename
HTML_FILES = {
    97: "97_prehistory.html",
    98: "98_indus_valley.html",
    99: "99_vedic_age.html",
    100: "100_mahajanapadas.html",
    101: "101_buddhism_jainism.html",
    102: "102_mauryan_empire.html",
    103: "103_post_mauryan.html",
    104: "104_gupta_empire.html",
    105: "105_post_gupta_sangam.html",
    106: "106_art_literature.html",
}


def shuffle_json(json_path):
    """Shuffle options in JSON sidecar, return list of (old_correct_idx, new_correct_idx, shuffled_options)."""
    with open(json_path, "r") as f:
        data = json.load(f)

    results = []
    for i, q in enumerate(data):
        old_correct = q["answer"]
        old_options = q["options"]
        correct_text = old_options[old_correct]

        # Create shuffled order
        indices = list(range(len(old_options)))
        random.shuffle(indices)
        new_options = [old_options[idx] for idx in indices]
        new_correct = new_options.index(correct_text)

        q["options"] = new_options
        q["answer"] = new_correct
        results.append((old_correct, new_correct, new_options))

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return results


def update_html(html_path, shuffle_results):
    """Update HTML file with shuffled answers."""
    with open(html_path, "r") as f:
        content = f.read()

    # 1. Update option labels for each question
    for i, (old_correct, new_correct, new_options) in enumerate(shuffle_results, 1):
        # Find the mcq-block for question i
        # Pattern: <div class="mcq-block" id="qN"> ... </div>
        q_pattern = re.compile(
            r'(<div class="mcq-block" id="q' + str(i) + r'">.*?)(</div>\s*</div>)',
            re.DOTALL
        )

        match = q_pattern.search(content)
        if not match:
            # Try alternative pattern
            q_pattern = re.compile(
                r'(id="q' + str(i) + r'".*?)(</div>\s*</div>\s*(?=  </div>|<div class="mcq-block|$))',
                re.DOTALL
            )
            match = q_pattern.search(content)

        if match:
            q_content = match.group(1)

            # Replace each option label
            for opt_idx, opt_text in enumerate(new_options):
                opt_letter = chr(65 + opt_idx)  # A, B, C, D
                # Match: <label class="mcq-option"><input type="radio" name="qN" value="X"> X. text</label>
                opt_pattern = re.compile(
                    r'(<label class="mcq-option"><input type="radio" name="q' + str(i) +
                    r'" value=")[abcd]("> )[A-D]\. .*?(</label>)'
                )
                # We need to replace them one by one in order
                # Use a different approach - find all option labels and replace sequentially

            # Find all option labels for this question
            opt_label_pattern = re.compile(
                r'(<label class="mcq-option"><input type="radio" name="q' + str(i) +
                r'" value=")([abcd])("> )([A-D])(\. )(.*?)(</label>)'
            )

            new_q_content = q_content
            opt_matches = list(opt_label_pattern.finditer(new_q_content))

            if len(opt_matches) == len(new_options):
                # Replace from end to beginning to preserve offsets
                for j in range(len(opt_matches) - 1, -1, -1):
                    m = opt_matches[j]
                    opt_letter = chr(65 + j)  # A, B, C, D
                    opt_value = chr(97 + j)    # a, b, c, d
                    new_label = (
                        m.group(1) + opt_value + m.group(3) +
                        opt_letter + m.group(5) + new_options[j] + m.group(7)
                    )
                    new_q_content = (
                        new_q_content[:m.start()] + new_label + new_q_content[m.end():]
                    )

                # Replace the question content
                content = content[:match.start()] + new_q_content + content[match.end():]

    # 2. Update the answers object
    answers_pattern = re.compile(
        r'(const answers = \{)\s*' +
        r'(q1:.*?q25:.*?)' +
        r'(\s*\})',
        re.DOTALL
    )

    ans_match = answers_pattern.search(content)
    if ans_match:
        # Build new answers string
        ans_parts = []
        for i, (old_correct, new_correct, _) in enumerate(shuffle_results, 1):
            ans_letter = chr(97 + new_correct)  # a, b, c, d
            ans_parts.append(f"q{i}: '{ans_letter}'")

        new_answers = ", ".join(ans_parts[:10]) + ",\n  " + ", ".join(ans_parts[10:20]) + ",\n  " + ", ".join(ans_parts[20:])
        content = content[:ans_match.start()] + "const answers = {\n  " + new_answers + "\n}" + content[ans_match.end():]

    # 3. Update explanation "Correct Answer: (X)"
    for i, (old_correct, new_correct, _) in enumerate(shuffle_results, 1):
        old_letter = chr(65 + old_correct)
        new_letter = chr(65 + new_correct)

        # Pattern: ✅ <strong>Correct Answer: (X)</strong>
        exp_pattern = re.compile(
            r'(id="exp' + str(i) + r'">✅ <strong>Correct Answer: \()' +
            re.escape(old_letter) +
            r'(\)</strong>)'
        )
        content = exp_pattern.sub(r'\g<1>' + new_letter + r'\g<2>', content)

    with open(html_path, "w") as f:
        f.write(content)


def main():
    print("=" * 60)
    print("Shuffling MCQ answer keys for Block 10 (topics 97-106)")
    print("=" * 60)

    for topic_num in sorted(TOPIC_FILES.keys()):
        json_file = TOPIC_FILES[topic_num]
        html_file = HTML_FILES[topic_num]

        json_path = os.path.join(MCQ_DIR, json_file)
        html_path = os.path.join(TOPICS_DIR, html_file)

        if not os.path.exists(json_path):
            print(f"  ✗ Topic {topic_num}: JSON not found ({json_path})")
            continue
        if not os.path.exists(html_path):
            print(f"  ✗ Topic {topic_num}: HTML not found ({html_path})")
            continue

        results = shuffle_json(json_path)

        # Count distribution
        dist = [0, 0, 0, 0]
        for _, new_correct, _ in results:
            dist[new_correct] += 1

        update_html(html_path, results)

        print(f"  ✓ Topic {topic_num}: {dist[0]}A {dist[1]}B {dist[2]}C {dist[3]}D")

    print()
    print("Done! All answer keys shuffled.")


if __name__ == "__main__":
    main()