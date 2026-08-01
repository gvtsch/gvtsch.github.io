#!/usr/bin/env python3
"""
Fix Advent of Code translation links.
Maps shortened links (Day-01) to full file names (Day 01 - Local LLM).
"""

from pathlib import Path
import re

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

def build_advent_mapping(content_dir, lang):
    """Build mapping from Day-XX to full file names."""
    advent_dir = content_dir / f"{lang}/blog/Advent of Code 2025"
    if not advent_dir.exists():
        return {}

    mapping = {}
    for file in advent_dir.glob("Day *.md"):
        # Extract day number
        match = re.match(r'Day (\d+)', file.stem)
        if match:
            day_num = match.group(1)
            short_key = f"Day-{day_num}"
            full_path = f"{lang}/blog/Advent of Code 2025/{file.stem}"
            mapping[short_key] = full_path

    # Also add the main file
    main_file = advent_dir / "Advent of Code 2025.md"
    if main_file.exists():
        mapping["Advent-of-Code-2025"] = f"{lang}/blog/Advent of Code 2025/Advent of Code 2025"

    return mapping

def extract_translations(file_path):
    """Extract translations field from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

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

        return translations if translations else None
    except Exception as e:
        return None

def main():
    content_dir = Path("/Users/christophkempkes/Coding/gvtsch.github.io/content")

    # Build mappings for both languages
    de_mapping = build_advent_mapping(content_dir, "de")
    en_mapping = build_advent_mapping(content_dir, "en")

    print("=" * 80)
    print("FIXING ADVENT OF CODE TRANSLATION LINKS")
    print("=" * 80)
    print(f"\nBuilt mapping for {len(de_mapping)} DE files and {len(en_mapping)} EN files")

    # Find all Advent of Code files
    de_files = list((content_dir / "de/blog/Advent of Code 2025").glob("*.md"))
    en_files = list((content_dir / "en/blog/Advent of Code 2025").glob("*.md"))
    all_files = de_files + en_files

    fixed_count = 0

    for file_path in sorted(all_files):
        translations = extract_translations(file_path)
        if translations is None:
            continue

        relative_path = str(file_path.relative_to(content_dir)).replace('.md', '')

        for lang, target_path in translations.items():
            # Check if this is a shortened Advent of Code link
            if "Advent" in target_path:
                # Extract the shortened part
                parts = target_path.split('/')
                if len(parts) >= 3:
                    short_name = parts[-1]

                    # Look up in appropriate mapping
                    mapping = de_mapping if lang == "de" else en_mapping

                    if short_name in mapping:
                        correct_path = mapping[short_name]

                        if correct_path != target_path:
                            print(f"\n📄 {relative_path}")
                            print(f"   Fixing {lang} link:")
                            print(f"   Old: {target_path}")
                            print(f"   New: {correct_path}")

                            if update_translation_link(file_path, target_path, correct_path, lang):
                                fixed_count += 1

    print("\n" + "=" * 80)
    print(f"SUMMARY: Fixed {fixed_count} Advent of Code translation links")
    print("=" * 80)

if __name__ == "__main__":
    main()
