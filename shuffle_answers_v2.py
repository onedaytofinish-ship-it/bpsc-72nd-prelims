#!/usr/bin/env python3
"""
Shuffle MCQ answer keys across A/B/C/D for any topic.

Usage: python3 shuffle_answers_v2.py [topic_numbers...]
If no arguments, shuffles all topics with >15/25 'a' answers.
"""

import json
import os
import re
import glob
import random
import sys

random.seed(42)

TOPICS_DIR = os.path.join(os.path.dirname(__file__), "Topics")
MCQ_DIR = os.path.join(TOPICS_DIR, "mcq")


def find_files(topic_num):
    """Find HTML and JSON files for a topic number."""
    html_files = glob.glob(os.path.join(TOPICS_DIR, f"{topic_num}_*.html"))
    json_files = glob.glob(os.path.join(MCQ_DIR, f"{topic_num}_*.json"))
    if html_files and json_files:
        return html_files[0], json_files[0]
    return None, None


def get_answer_distribution(html_path):
    """Get the count of a/b/c/d answers from HTML."""
    content = open(html_path).read()
    ans_match = re.search(r'const answers = \{(.*?)\}', content, re.DOTALL)
    if not ans_match:
        return None
    ans_text = ans_match.group(1)
    answers = re.findall(r"q(\d+): '([abcd])'", ans_text)
    dist = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    for _, letter in answers:
        dist[letter] += 1
    return dist


def shuffle_topic(topic_num):
    """Shuffle answers for a single topic."""
    html_path, json_path = find_files(topic_num)
    if not html_path:
        print(f"  ✗ Topic {topic_num}: files not found")
        return False

    # Check if needs shuffling
    dist = get_answer_distribution(html_path)
    if dist and dist['a'] <= 10:
        print(f"  ✓ Topic {topic_num}: already balanced ({dist['a']}A {dist['b']}B {dist['c']}C {dist['d']}D) — skipping")
        return True

    # Load JSON
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

    # Update HTML
    with open(html_path, "r") as f:
        content = f.read()

    # 1. Update option labels for each question
    for i, (old_correct, new_correct, new_options) in enumerate(results, 1):
        # Find all option labels for this question
        opt_label_pattern = re.compile(
            r'(<label class="mcq-option"><input type="radio" name="q' + str(i) +
            r'" value=")([abcd])("> )([A-D])(\. )(.*?)(</label>)'
        )

        opt_matches = list(opt_label_pattern.finditer(content))
        if len(opt_matches) == len(new_options):
            # Replace from end to beginning to preserve offsets
            for j in range(len(opt_matches) - 1, -1, -1):
                m = opt_matches[j]
                opt_letter = chr(65 + j)
                opt_value = chr(97 + j)
                new_label = (
                    m.group(1) + opt_value + m.group(3) +
                    opt_letter + m.group(5) + new_options[j] + m.group(7)
                )
                content = content[:m.start()] + new_label + content[m.end():]

    # 2. Update the answers object
    answers_pattern = re.compile(
        r'(const answers = \{)\s*' +
        r'(q1:.*?q25:.*?)' +
        r'(\s*\})',
        re.DOTALL
    )

    ans_match = answers_pattern.search(content)
    if ans_match:
        ans_parts = []
        for i, (old_correct, new_correct, _) in enumerate(results, 1):
            ans_letter = chr(97 + new_correct)
            ans_parts.append(f"q{i}: '{ans_letter}'")

        new_answers = ", ".join(ans_parts[:10]) + ",\n  " + ", ".join(ans_parts[10:20]) + ",\n  " + ", ".join(ans_parts[20:])
        content = content[:ans_match.start()] + "const answers = {\n  " + new_answers + "\n}" + content[ans_match.end():]

    # 3. Update explanation "Correct Answer: (X)"
    for i, (old_correct, new_correct, _) in enumerate(results, 1):
        old_letter = chr(65 + old_correct)
        new_letter = chr(65 + new_correct)

        exp_pattern = re.compile(
            r'(id="exp' + str(i) + r'">✅ <strong>Correct Answer: \()' +
            re.escape(old_letter) +
            r'(\)</strong>)'
        )
        content = exp_pattern.sub(r'\g<1>' + new_letter + r'\g<2>', content)

    with open(html_path, "w") as f:
        f.write(content)

    dist = [0, 0, 0, 0]
    for _, new_correct, _ in results:
        dist[new_correct] += 1
    print(f"  ✓ Topic {topic_num}: shuffled to {dist[0]}A {dist[1]}B {dist[2]}C {dist[3]}D")
    return True


def main():
    if len(sys.argv) > 1:
        topics = [int(x) for x in sys.argv[1:]]
    else:
        # Auto-find topics needing shuffling
        print("Auto-detecting topics with >15/25 'a' answers...")
        topics = []
        for n in range(1, 160):
            html_path, _ = find_files(n)
            if not html_path:
                continue
            dist = get_answer_distribution(html_path)
            if dist and dist['a'] > 15:
                topics.append(n)
        if not topics:
            print("No topics need shuffling.")
            return

    print(f"Shuffling {len(topics)} topics: {topics}")
    print("=" * 60)

    for topic_num in topics:
        shuffle_topic(topic_num)

    print("\nDone!")


if __name__ == "__main__":
    main()