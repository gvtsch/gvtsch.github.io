#!/usr/bin/env python3
"""
Automatically fix broken translation links.
"""

from pathlib import Path
import re

def extract_translations(file_path):
    """Extract translations field from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content

        frontmatter = parts[1]
        translations = {}
        in_translations = False

        for line in frontmatter.split('\n'):
            if line.strip().startswith('translations:'):
                in_translations = True
                continue
            if in_translations:
                if line.startswith('  ') and ':' in line:
                    lang, path = line.strip().split(':', 1)
                    translations[lang.strip()] = path.strip()
                else:
                    break

        return translations if translations else None, content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

def find_actual_file(content_dir, broken_path):
    """Try to find the actual file by testing various path variants."""
    # Try original path first
    test_path = content_dir / f"{broken_path}.md"
    if test_path.exists():
        return broken_path

    # Replace hyphens with spaces
    path_with_spaces = broken_path.replace('-', ' ')
    test_path = content_dir / f"{path_with_spaces}.md"
    if test_path.exists():
        return path_with_spaces

    # Try to find similar files
    parts = Path(broken_path).parts
    if len(parts) > 1:
        directory = content_dir / Path(*parts[:-1])
        if directory.exists():
            filename_pattern = parts[-1].lower()
            for candidate in directory.glob("*.md"):
                candidate_name = candidate.stem.lower()
                # Check if it's a close match
                if candidate_name.replace(' ', '-') == filename_pattern.replace('-', ' '):
                    relative = str(candidate.relative_to(content_dir)).replace('.md', '')
                    return relative

    return None

def update_translation_link(file_path, old_translation, new_translation, lang):
    """Update a translation link in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace the specific translation line
        pattern = f"(translations:\\s*\\n(?:.*\\n)*?)  {lang}: {re.escape(old_translation)}"
        replacement = f"\\g<1>  {lang}: {new_translation}"

        new_content = re.sub(pattern, replacement, content)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    content_dir = Path("/Users/christophkempkes/Coding/gvtsch.github.io/content")

    # Find all markdown files
    all_files = list(content_dir.glob("de/blog/**/*.md")) + list(content_dir.glob("en/blog/**/*.md"))

    print("=" * 80)
    print("FIXING TRANSLATION LINKS")
    print("=" * 80)

    fixed_count = 0
    unfixable = []

    for file_path in sorted(all_files):
        translations, content = extract_translations(file_path)
        if translations is None or content is None:
            continue

        file_fixed = False
        relative_path = str(file_path.relative_to(content_dir)).replace('.md', '')

        for lang, target_path in translations.items():
            target_file = content_dir / f"{target_path}.md"

            if not target_file.exists():
                # Try to find the actual file
                actual_path = find_actual_file(content_dir, target_path)

                if actual_path:
                    print(f"\n📄 {relative_path}")
                    print(f"   Fixing {lang} link:")
                    print(f"   Old: {target_path}")
                    print(f"   New: {actual_path}")

                    if update_translation_link(file_path, target_path, actual_path, lang):
                        fixed_count += 1
                        file_fixed = True
                    else:
                        print(f"   ⚠️  Failed to update file")
                else:
                    unfixable.append({
                        'file': relative_path,
                        'lang': lang,
                        'broken_path': target_path
                    })

    print("\n" + "=" * 80)
    print(f"SUMMARY: Fixed {fixed_count} translation links")
    print("=" * 80)

    if unfixable:
        print(f"\n⚠️  Could not fix {len(unfixable)} links (files not found):")
        for item in unfixable[:10]:  # Show first 10
            print(f"   {item['file']} -> {item['broken_path']}")
        if len(unfixable) > 10:
            print(f"   ... and {len(unfixable) - 10} more")

    print("\n✓ Done! Run validate_translations.py to verify.")

if __name__ == "__main__":
    main()
