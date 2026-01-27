#!/usr/bin/env python3
"""
Restructure content for dual-language support.

This script:
1. Moves English articles from Blog/ to en/blog/
2. Moves German articles from Blog/Deutsch/ to de/blog/
3. Moves Notes/ to en/notes/
4. Creates de/notes/ placeholders
5. Matches EN/DE article pairs and adds translations frontmatter
6. Creates placeholders for articles without translations
"""

import os
import re
import shutil
from pathlib import Path
from typing import Optional


def slugify(text: str) -> str:
    """Convert a filename/path to a Quartz-compatible slug."""
    segments = text.split("/")
    slugified = []
    for segment in segments:
        s = segment
        s = re.sub(r'\s', '-', s)
        s = s.replace('&', '-and-')
        s = s.replace('%', '-percent')
        s = s.replace('?', '')
        s = s.replace('#', '')
        if s.endswith('.md'):
            s = s[:-3]
        slugified.append(s)
    return '/'.join(slugified).rstrip('/')


def get_title_from_file(filepath: Path) -> Optional[str]:
    """Extract title from frontmatter or filename."""
    try:
        content = filepath.read_text(encoding='utf-8')
        # Try to get title from frontmatter
        if content.startswith('---'):
            match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
        # Fall back to filename
        return filepath.stem
    except:
        return filepath.stem


def normalize_for_matching(text: str) -> str:
    """Normalize text for matching articles across languages."""
    text = text.lower()
    # Remove common prefixes like dates
    text = re.sub(r'^\d{4}-\d{2}-\d{2}-?', '', text)
    # Remove language suffixes
    text = re.sub(r'_de$', '', text)
    text = re.sub(r'_en$', '', text)
    # Remove special chars
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Known article pairs (English filename -> German filename)
# This handles cases where automatic matching won't work
KNOWN_PAIRS = {
    "Docker, Compose & Codespaces.md": "docker_compose_codespaces_de.md",
    "Neural networks explained, using the MNIST example.md": "2024-04-01-Neuronale Netze am Beispiel MNIST.md",
    "Sorting Algorithms with Python.md": "2024-05-19-Sortieralgorithmen mit Python.md",
    "Supervised, Unsupervised and Reinforcement Learning — A brief overview.md": "2023-01-01-Supervised, Unsupervised und Reinforcement Learning - Eine Übersicht.md",
    "Weak AI, strong AI &  Expertsystems.md": "2022-12-30-Schwache KI, starke KI und Expertensysteme.md",
    "The Transformer Architecture I.md": "Transformer_Teil_1_de.md",
    "Job Queue with Python.md": "2024-12-08-Job Scheduling mit Python.md",
    "Logging.md": "Logging_de.md",
    "PINN.md": "PINN_de.md",
}

# Known pairs for LangChain subfolder
KNOWN_LANGCHAIN_PAIRS = {
    "What is LangChain.md": "LangChain_de.md",  # in parent Deutsch folder
    "ReAct.md": "ReAct_de.md",  # in parent Deutsch folder
    "Agents_at_its_limits.md": "Agenten_an_ihren_Grenzen.md",  # in parent Deutsch folder
}

# Known pairs for Decision Tree subfolder
KNOWN_DECISION_TREE_PAIRS = {
    "The Decision Tree.md": "2023-01-16-Der Entscheidungsbaum.md",
    "The Random Forrest.md": "2023-02-09-Der Random Forrest.md",
    "Theory and formulas behind the decision tree.md": "2023-02-20-Theorie und Formeln hinter dem Entscheidungsbaum.md",
}

# Advent of Code pairs (English Day X -> German Tag X)
def get_advent_pair(en_filename: str) -> Optional[str]:
    """Get German equivalent for Advent of Code articles."""
    # Extract day number
    match = re.search(r'Day (\d+)', en_filename)
    if match:
        day = match.group(1)
        # German files use "Tag" instead of "Day"
        # Check for various patterns
        return f"Tag {day}"
    return None


def add_translations_to_frontmatter(filepath: Path, translations: dict) -> None:
    """Add or update translations in frontmatter."""
    content = filepath.read_text(encoding='utf-8')

    if not content.startswith('---'):
        # No frontmatter, create one
        trans_yaml = "translations:\n"
        for lang, slug in translations.items():
            trans_yaml += f'  {lang}: "{slug}"\n'
        content = f"---\n{trans_yaml}---\n{content}"
        filepath.write_text(content, encoding='utf-8')
        return

    lines = content.split('\n')
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_idx = i
            break

    if end_idx is None:
        return

    # Check if translations already exist
    frontmatter = '\n'.join(lines[1:end_idx])
    if 'translations:' in frontmatter:
        # Update existing - for now, skip
        return

    # Add translations before closing ---
    trans_lines = ["translations:"]
    for lang, slug in translations.items():
        trans_lines.append(f'  {lang}: "{slug}"')

    new_lines = lines[:end_idx] + trans_lines + lines[end_idx:]
    filepath.write_text('\n'.join(new_lines), encoding='utf-8')


def create_placeholder(filepath: Path, original_title: str, original_lang: str, translation_slug: str) -> None:
    """Create a placeholder file for missing translation."""
    if original_lang == 'en':
        note_text = f"""> [!note] Diese Seite ist noch nicht auf Deutsch verfügbar
> Eine deutsche Übersetzung dieser Seite ist in Arbeit. In der Zwischenzeit kannst du die [englische Version](/{translation_slug}) lesen."""
        title = original_title  # Keep original title for now
        trans_lang = 'de'
        other_lang = 'en'
    else:
        note_text = f"""> [!note] This page is not yet available in English
> An English translation of this page is in progress. In the meantime, you can read the [German version](/{translation_slug})."""
        title = original_title
        trans_lang = 'en'
        other_lang = 'de'

    content = f"""---
title: "{title}"
translations:
  {other_lang}: "{translation_slug}"
---
{note_text}
"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding='utf-8')


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Restructure content for dual-language support')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--content-path', default='content', help='Path to content directory')
    args = parser.parse_args()

    content_path = Path(args.content_path)
    if not content_path.exists():
        print(f"Error: Content path '{content_path}' does not exist")
        return 1

    dry_run = args.dry_run
    if dry_run:
        print("DRY RUN - No changes will be made\n")

    # Create target directories
    en_blog = content_path / "en" / "blog"
    de_blog = content_path / "de" / "blog"
    en_notes = content_path / "en" / "notes"
    de_notes = content_path / "de" / "notes"

    if not dry_run:
        en_blog.mkdir(parents=True, exist_ok=True)
        de_blog.mkdir(parents=True, exist_ok=True)
        en_notes.mkdir(parents=True, exist_ok=True)
        de_notes.mkdir(parents=True, exist_ok=True)

    # Track what we've processed
    processed_pairs = []
    en_without_de = []
    de_without_en = []

    # 1. Process main Blog/ articles (English)
    print("=== Processing English Blog Articles ===")
    blog_path = content_path / "Blog"
    deutsch_path = blog_path / "Deutsch"

    for md_file in blog_path.glob("*.md"):
        en_name = md_file.name
        print(f"\nEN: {en_name}")

        # Check for known German pair
        de_name = KNOWN_PAIRS.get(en_name)
        de_file = None

        if de_name:
            de_file = deutsch_path / de_name
            if not de_file.exists():
                de_file = None
                print(f"  WARNING: Expected DE file not found: {de_name}")

        # Target paths
        en_target = en_blog / en_name

        if de_file:
            de_target = de_blog / de_file.name

            # Calculate slugs
            en_slug = f"en/blog/{slugify(en_name)}"
            de_slug = f"de/blog/{slugify(de_file.name)}"

            print(f"  DE: {de_file.name}")
            print(f"  EN slug: {en_slug}")
            print(f"  DE slug: {de_slug}")

            if not dry_run:
                # Copy files
                shutil.copy2(md_file, en_target)
                shutil.copy2(de_file, de_target)

                # Add translations
                add_translations_to_frontmatter(en_target, {'de': de_slug})
                add_translations_to_frontmatter(de_target, {'en': en_slug})

            processed_pairs.append((en_name, de_file.name))
        else:
            en_slug = f"en/blog/{slugify(en_name)}"
            de_slug = f"de/blog/{slugify(en_name)}"  # Same name for placeholder

            print(f"  No DE translation found - will create placeholder")
            print(f"  EN slug: {en_slug}")

            if not dry_run:
                shutil.copy2(md_file, en_target)
                add_translations_to_frontmatter(en_target, {'de': de_slug})

                # Create placeholder
                de_target = de_blog / en_name
                title = get_title_from_file(md_file)
                create_placeholder(de_target, title, 'en', en_slug)

            en_without_de.append(en_name)

    # 2. Process Blog subdirectories (LangChain, Advent of Code, etc.)
    print("\n=== Processing Blog Subdirectories ===")
    for subdir in blog_path.iterdir():
        if not subdir.is_dir() or subdir.name == "Deutsch":
            continue

        print(f"\n--- Subdirectory: {subdir.name} ---")
        en_subdir = en_blog / subdir.name
        de_subdir = de_blog / subdir.name

        if not dry_run:
            en_subdir.mkdir(parents=True, exist_ok=True)
            de_subdir.mkdir(parents=True, exist_ok=True)

        for md_file in subdir.glob("*.md"):
            en_name = md_file.name
            print(f"\nEN: {subdir.name}/{en_name}")

            # Check for known pairs
            de_name = None
            de_file = None

            if subdir.name == "LangChain":
                de_name = KNOWN_LANGCHAIN_PAIRS.get(en_name)
                if de_name:
                    de_file = deutsch_path / de_name
            elif subdir.name == "Decision Tree and Random Forest":
                de_name = KNOWN_DECISION_TREE_PAIRS.get(en_name)
                if de_name:
                    de_file = deutsch_path / de_name
            elif subdir.name == "Advent of Code 2025":
                # Check for German Advent of Code
                day_match = get_advent_pair(en_name)
                if day_match:
                    de_advent_path = deutsch_path / "Advent of Code"
                    for de_candidate in de_advent_path.glob("*.md"):
                        if day_match in de_candidate.name:
                            de_file = de_candidate
                            de_name = de_candidate.name
                            break

            en_target = en_subdir / en_name

            if de_file and de_file.exists():
                de_target = de_subdir / de_file.name

                en_slug = f"en/blog/{subdir.name}/{slugify(en_name)}"
                de_slug = f"de/blog/{subdir.name}/{slugify(de_file.name)}"

                print(f"  DE: {de_file.name}")
                print(f"  EN slug: {en_slug}")
                print(f"  DE slug: {de_slug}")

                if not dry_run:
                    shutil.copy2(md_file, en_target)
                    shutil.copy2(de_file, de_target)
                    add_translations_to_frontmatter(en_target, {'de': de_slug})
                    add_translations_to_frontmatter(de_target, {'en': en_slug})

                processed_pairs.append((f"{subdir.name}/{en_name}", f"{subdir.name}/{de_file.name}"))
            else:
                en_slug = f"en/blog/{subdir.name}/{slugify(en_name)}"
                de_slug = f"de/blog/{subdir.name}/{slugify(en_name)}"

                print(f"  No DE translation - will create placeholder")

                if not dry_run:
                    shutil.copy2(md_file, en_target)
                    add_translations_to_frontmatter(en_target, {'de': de_slug})

                    de_target = de_subdir / en_name
                    title = get_title_from_file(md_file)
                    create_placeholder(de_target, title, 'en', en_slug)

                en_without_de.append(f"{subdir.name}/{en_name}")

    # 3. Process remaining German articles (those without English pairs)
    print("\n=== Processing Remaining German Articles ===")
    processed_de_files = set()
    for en_name, de_name in processed_pairs:
        if "/" in de_name:
            processed_de_files.add(de_name.split("/")[-1])
        else:
            processed_de_files.add(de_name)

    for md_file in deutsch_path.glob("*.md"):
        if md_file.name in processed_de_files:
            continue

        print(f"\nDE only: {md_file.name}")

        de_target = de_blog / md_file.name
        de_slug = f"de/blog/{slugify(md_file.name)}"
        en_slug = f"en/blog/{slugify(md_file.name)}"

        print(f"  DE slug: {de_slug}")
        print(f"  Will create EN placeholder")

        if not dry_run:
            shutil.copy2(md_file, de_target)
            add_translations_to_frontmatter(de_target, {'en': en_slug})

            en_target = en_blog / md_file.name
            title = get_title_from_file(md_file)
            create_placeholder(en_target, title, 'de', de_slug)

        de_without_en.append(md_file.name)

    # 4. Process Notes
    print("\n=== Processing Notes ===")
    notes_path = content_path / "Notes"
    if notes_path.exists():
        for md_file in notes_path.glob("*.md"):
            en_name = md_file.name
            print(f"\nNote: {en_name}")

            en_target = en_notes / en_name
            de_target = de_notes / en_name

            en_slug = f"en/notes/{slugify(en_name)}"
            de_slug = f"de/notes/{slugify(en_name)}"

            if not dry_run:
                shutil.copy2(md_file, en_target)
                add_translations_to_frontmatter(en_target, {'de': de_slug})

                title = get_title_from_file(md_file)
                create_placeholder(de_target, title, 'en', en_slug)

    # 5. Create index files
    print("\n=== Creating Index Files ===")

    # Copy existing index.md to en/index.md
    root_index = content_path / "index.md"
    if root_index.exists():
        en_index = content_path / "en" / "index.md"
        de_index = content_path / "de" / "index.md"

        if not dry_run:
            shutil.copy2(root_index, en_index)
            add_translations_to_frontmatter(en_index, {'de': 'de/index'})

            # Create German index placeholder
            de_index_content = """---
title: "Startseite"
translations:
  en: "en/index"
---
> [!note] Deutsche Startseite
> Willkommen! Diese Seite ist die deutsche Version meines Digital Garden.

Wähle eine Kategorie aus dem Explorer links, um zu beginnen.
"""
            de_index.write_text(de_index_content, encoding='utf-8')

        print("Created en/index.md and de/index.md")

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Article pairs processed: {len(processed_pairs)}")
    print(f"EN articles without DE (placeholders created): {len(en_without_de)}")
    print(f"DE articles without EN (placeholders created): {len(de_without_en)}")

    if dry_run:
        print("\nThis was a DRY RUN. Run without --dry-run to make changes.")

    return 0


if __name__ == '__main__':
    exit(main())
