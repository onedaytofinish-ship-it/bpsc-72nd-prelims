#!/usr/bin/env python3
"""
Fix the last MCQ block (Q25) missing closing </div> tags.
The Q25 block is followed by </div> (section close) and then a new section.
We need to add </div></div> before the section close.
"""

import os
import re
import glob

TOPICS_DIR = os.path.join(os.path.dirname(__file__), "Topics")


def fix_last_block(html_path):
    with open(html_path, "r") as f:
        content = f.read()

    # Find Q25 explanation, then the section closing
    # Pattern: ...explanation text...\n\n</div>\n\n<div class="section">
    # Need: ...explanation text...\n    </div>\n  </div>\n\n</div>\n\n<div class="section">

    # The Q25 block is the last one, followed by the section close </div>
    # We need to insert 2 closing divs before the section close

    # Find: id="exp25" ... content ... \n\n</div> (this is the section close)
    # Replace with: id="exp25" ... content ... \n    </div>\n  </div>\n\n</div>

    # Pattern: the exp25 content followed by a blank line and </div>
    pattern = re.compile(
        r'(id="exp25">[^<]*(?:<[^/][^>]*>[^<]*)*.*?)'  # exp25 content
        r'(\n\n</div>\s*\n\n<div class="section">)',  # section close + new section
        re.DOTALL
    )

    match = pattern.search(content)
    if not match:
        # Try simpler pattern
        pattern = re.compile(
            r'(id="exp25">.*?)\n(\n</div>\s*\n)',
            re.DOTALL
        )
        match = pattern.search(content)

    if match:
        # Insert the two missing closing divs
        content = content[:match.end(1)] + '\n    </div>\n  </div>' + content[match.start(2):]
        with open(html_path, "w") as f:
            f.write(content)
        return True
    return False


def main():
    for n in range(97, 107):
        files = glob.glob(os.path.join(TOPICS_DIR, f"{n}_*.html"))
        if not files:
            continue
        result = fix_last_block(files[0])
        print(f"  {'✓' if result else '✗'} Topic {n}: {'Fixed Q25' if result else 'No fix needed/failed'}")

    # Verify
    import re
    print("\nVerification:")
    for n in range(97, 107):
        files = glob.glob(os.path.join(TOPICS_DIR, f"{n}_*.html"))
        content = open(files[0]).read()
        opens = len(re.findall(r'<div', content))
        closes = len(re.findall(r'</div>', content))
        print(f"  Topic {n}: div opens={opens} closes={closes} diff={opens-closes}")


if __name__ == "__main__":
    main()