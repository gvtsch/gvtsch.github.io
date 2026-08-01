#!/usr/bin/env python3
"""
Validate translation links in blog posts.
Checks if translation links are bidirectional and point to existing files.
"""

from pathlib import Path
import re

def extract_translations(file_path):
    """Extract translations field from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]

        # Extract translations
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
        print(f"Error reading {file_path}: {e}")
        return None

def get_relative_path(file_path, content_dir):
    """Get relative path from content directory."""
    return str(file_path.relative_to(content_dir)).replace('.md', '')

def main():
    content_dir = Path("/Users/christophkempkes/Coding/gvtsch.github.io/content")

    # Find all markdown files
    de_files = list(content_dir.glob("de/blog/**/*.md"))
    en_files = list(content_dir.glob("en/blog/**/*.md"))

    all_files = de_files + en_files

    print("=" * 80)
    print("TRANSLATION VALIDATION REPORT")
    print("=" * 80)

    issues = []
    checked = 0

    for file_path in sorted(all_files):
        relative_path = get_relative_path(file_path, content_dir)
        translations = extract_translations(file_path)

        if translations is None:
            issues.append({
                'type': 'NO_TRANSLATIONS',
                'file': relative_path,
                'message': 'Missing translations field'
            })
            continue

        checked += 1

        # Check each translation link
        for lang, target_path in translations.items():
            # Construct target file path
            target_file = content_dir / f"{target_path}.md"

            if not target_file.exists():
                issues.append({
                    'type': 'BROKEN_LINK',
                    'file': relative_path,
                    'target': target_path,
                    'lang': lang,
                    'message': f'Translation target does not exist: {target_path}'
                })
                continue

            # Check if target links back
            target_translations = extract_translations(target_file)
            if target_translations is None:
                issues.append({
                    'type': 'NO_BACKLINK',
                    'file': relative_path,
                    'target': target_path,
                    'lang': lang,
                    'message': 'Target has no translations field'
                })
                continue

            # Determine expected backlink language
            source_lang = 'de' if relative_path.startswith('de/') else 'en'

            if source_lang not in target_translations:
                issues.append({
                    'type': 'MISSING_BACKLINK',
                    'file': relative_path,
                    'target': target_path,
                    'lang': lang,
                    'message': f'Target does not link back (missing {source_lang} translation)'
                })
                continue

            # Check if backlink points to correct file
            backlink = target_translations[source_lang]
            if backlink != relative_path:
                issues.append({
                    'type': 'WRONG_BACKLINK',
                    'file': relative_path,
                    'target': target_path,
                    'lang': lang,
                    'expected': relative_path,
                    'actual': backlink,
                    'message': f'Target links to wrong file: {backlink} (expected {relative_path})'
                })

    # Print summary
    print(f"\nChecked {checked} files with translations")
    print(f"Found {len(all_files)} total files")
    print(f"Found {len(issues)} issues\n")

    if issues:
        # Group by type
        by_type = {}
        for issue in issues:
            t = issue['type']
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(issue)

        for issue_type, items in sorted(by_type.items()):
            print(f"\n{'=' * 80}")
            print(f"{issue_type}: {len(items)} issues")
            print('=' * 80)

            for issue in sorted(items, key=lambda x: x['file']):
                print(f"\n📄 {issue['file']}")
                print(f"   {issue['message']}")
                if 'target' in issue:
                    print(f"   Target: {issue['target']}")
                if 'expected' in issue and 'actual' in issue:
                    print(f"   Expected: {issue['expected']}")
                    print(f"   Actual: {issue['actual']}")
    else:
        print("\n✅ All translation links are valid!")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
