#!/usr/bin/env python3
"""
Fix missing closing </div> tags in MCQ blocks for Block 10 topics (97-106).

Each MCQ block should have this structure:
  <div class="mcq-block" id="qN">
    <div class="mcq-q">...</div>
    <div class="mcq-options">
      <label>...</label>
      <label>...</label>
      <label>...</label>
      <label>...</label>
    </div>
    <div class="mcq-explanation" id="expN">...</div>
  </div>

But the closing </div> for the explanation and the mcq-block are missing.
Each MCQ block is missing 2 closing </div> tags.

This script adds the missing </div> tags before the next mcq-block or the
end of the MCQ section.
"""

import os
import re
import glob

TOPICS_DIR = os.path.join(os.path.dirname(__file__), "Topics")


def fix_html(html_path):
    """Fix missing closing divs in MCQ blocks."""
    with open(html_path, "r") as f:
        content = f.read()

    # Pattern to find each mcq-block and its content up to the next mcq-block
    # or end of MCQ section
    # Each block looks like:
    #   <div class="mcq-block" id="qN">
    #     <div class="mcq-q">...</div>
    #     <div class="mcq-options">...</div>
    #     <div class="mcq-explanation" id="expN">...</div>  <-- missing </div>
    #   </div>  <-- missing

    # Strategy: For each MCQ block, find the explanation div and add 2 closing
    # </div> tags after its content (before the next mcq-block or closing section)

    # Find all mcq-block boundaries
    blocks = list(re.finditer(r'<div class="mcq-block" id="q(\d+)">', content))
    if not blocks:
        return False, "No MCQ blocks found"

    # Find the end of the MCQ section (closing </div> of the section)
    # Look for the section after MCQs (References or footer)
    mcq_section_end = content.find('</div>\n\n<div class="section">')
    if mcq_section_end == -1:
        mcq_section_end = content.find('</div>\n\n<div class="doc-footer">')
    if mcq_section_end == -1:
        mcq_section_end = content.find('</div>\n\n  <div class="doc-footer">')
    if mcq_section_end == -1:
        # Try to find the references section
        mcq_section_end = content.find('📄')
    if mcq_section_end == -1:
        mcq_section_end = len(content)

    fixes_applied = 0

    # Process from end to beginning to preserve offsets
    for i in range(len(blocks) - 1, -1, -1):
        block_start = blocks[i].start()
        q_num = blocks[i].group(1)

        # Find the end of this block (next mcq-block or mcq section end)
        if i + 1 < len(blocks):
            block_end = blocks[i + 1].start()
        else:
            # Last block - find the section close
            # Look for the closing of the MCQ section
            block_end = mcq_section_end

        block_content = content[block_start:block_end]

        # Count div opens and closes in this block
        opens = block_content.count('<div')
        closes = block_content.count('</div>')
        diff = opens - closes

        if diff > 0:
            # Need to add 'diff' closing </div> tags
            # Find the right place to insert them - after the last content
            # before the next block or section close

            # The explanation text ends with a newline before the next block
            # We need to insert </div> tags right before the whitespace preceding
            # the next block

            # Find the last meaningful content in the block
            # Strip trailing whitespace from block_content
            stripped = block_content.rstrip()

            # Calculate the whitespace that follows
            trailing_ws = block_content[len(stripped):]

            # Add the missing closing divs
            closing_divs = '\n    </div>\n  </div>'  # close explanation + mcq-block
            # But only add what's needed
            if diff == 2:
                closing = closing_divs + trailing_ws
            elif diff == 1:
                closing = '\n  </div>' + trailing_ws
            else:
                closing = ('\n  </div>' * diff) + trailing_ws

            new_block_content = stripped + closing

            content = content[:block_start] + new_block_content + content[block_end:]
            fixes_applied += 1

    with open(html_path, "w") as f:
        f.write(content)

    return True, f"Fixed {fixes_applied} blocks"


def main():
    print("=" * 60)
    print("Fixing missing closing </div> tags in MCQ blocks (topics 97-106)")
    print("=" * 60)

    for n in range(97, 107):
        files = glob.glob(os.path.join(TOPICS_DIR, f"{n}_*.html"))
        if not files:
            print(f"  ✗ Topic {n}: HTML not found")
            continue

        html_path = files[0]
        success, msg = fix_html(html_path)
        print(f"  {'✓' if success else '✗'} Topic {n}: {msg}")

    print()
    print("Done! All closing divs fixed.")


if __name__ == "__main__":
    main()