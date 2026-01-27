#!/usr/bin/env python3
"""
Fix translation slugs in frontmatter to use proper URL-safe slugs.

Quartz converts filenames to slugs using these rules:
- Spaces → hyphens
- & → -and-
- % → -percent
- ? and # are removed
- .md extension is removed
"""

import os
import re
from pathlib import Path


def slugify(text: str) -> str:
    """Convert a filename/path to a Quartz-compatible slug."""
    # Process each segment separately
    segments = text.split("/")
    slugified = []
    for segment in segments:
        s = segment
        s = re.sub(r'\s', '-', s)  # spaces to hyphens
        s = s.replace('&', '-and-')  # & to -and-
        s = s.replace('%', '-percent')  # % to -percent
        s = s.replace('?', '')  # remove ?
        s = s.replace('#', '')  # remove #
        # Remove .md extension if present
        if s.endswith('.md'):
            s = s[:-3]
        slugified.append(s)
    return '/'.join(slugified).rstrip('/')


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single markdown file and fix translation slugs."""
    content = filepath.read_text(encoding='utf-8')

    # Check if file has frontmatter
    if not content.startswith('---'):
        return False

    # Find the frontmatter section more carefully
    # Look for the closing --- on its own line
    lines = content.split('\n')
    if lines[0].strip() != '---':
        return False

    # Find the closing ---
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return False

    frontmatter_lines = lines[1:end_idx]
    body_lines = lines[end_idx+1:]
    frontmatter = '\n'.join(frontmatter_lines)
    body = '\n'.join(body_lines)

    # Check if there's a translations section
    if 'translations:' not in frontmatter:
        return False

    # Find and fix translation values
    modified = False
    new_lines = []
    in_translations = False

    for line in frontmatter_lines:
        if line.strip() == 'translations:':
            in_translations = True
            new_lines.append(line)
            continue

        if in_translations:
            # Check if we're still in the translations block
            if line and not line.startswith(' ') and not line.startswith('\t'):
                in_translations = False
                new_lines.append(line)
                continue

            # Process translation line (e.g., "  en: en/blog/Some Article")
            match = re.match(r'^(\s+)(en|de):\s*(.+)$', line)
            if match:
                indent = match.group(1)
                lang = match.group(2)
                value = match.group(3).strip()

                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                # Slugify the value
                slugified = slugify(value)

                if slugified != value:
                    print(f"  {lang}: {value}")
                    print(f"    → {slugified}")
                    modified = True
                    line = f'{indent}{lang}: "{slugified}"'

            new_lines.append(line)
        else:
            new_lines.append(line)

    if modified and not dry_run:
        new_frontmatter = '\n'.join(new_lines)
        new_content = f'---\n{new_frontmatter}\n---\n{body}'
        filepath.write_text(new_content, encoding='utf-8')

    return modified


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix translation slugs in markdown frontmatter')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    parser.add_argument('--path', default='content', help='Path to content directory')
    args = parser.parse_args()

    content_path = Path(args.path)
    if not content_path.exists():
        print(f"Error: Path '{content_path}' does not exist")
        return 1

    print(f"Scanning {content_path} for markdown files...")
    if args.dry_run:
        print("(Dry run - no files will be modified)\n")

    modified_count = 0
    total_count = 0

    for md_file in content_path.rglob('*.md'):
        total_count += 1
        rel_path = md_file.relative_to(content_path)

        try:
            if process_file(md_file, args.dry_run):
                print(f"\n[Modified] {rel_path}")
                modified_count += 1
        except Exception as e:
            print(f"[Error] {rel_path}: {e}")

    print(f"\n{'Would modify' if args.dry_run else 'Modified'} {modified_count} of {total_count} files")
    return 0


if __name__ == '__main__':
    exit(main())
