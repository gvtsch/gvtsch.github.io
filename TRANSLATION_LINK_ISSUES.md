# Translation Link Issues - Fallstricke bei Übersetzungs-Links

Dieses Dokument listet alle bekannten Probleme mit den `translations:` Frontmatter-Links auf.

## Problem 1: Ordnernamen mit Leerzeichen werden nicht slugifiziert

Quartz konvertiert Ordnernamen mit Leerzeichen zu Bindestrichen in der URL:
- Datei: `Decision Tree and Random Forest/file.md`
- URL: `/Decision-Tree-and-Random-Forest/file`

**Betroffene Dateien:**

### Decision Tree and Random Forest
- `de/blog/Decision Tree and Random Forest/2023-02-20-Theorie und Formeln hinter dem Entscheidungsbaum.md`
  - Falsch: `en/blog/Decision Tree and Random Forest/Theory-and-formulas-behind-the-decision-tree`
  - Richtig: `en/blog/Decision-Tree-and-Random-Forest/Theory-and-formulas-behind-the-decision-tree`

- `de/blog/Decision Tree and Random Forest/2023-02-09-Der Random Forrest.md`
  - Falsch: `en/blog/Decision Tree and Random Forest/The-Random-Forrest`
  - Richtig: `en/blog/Decision-Tree-and-Random-Forest/The-Random-Forrest`

- `de/blog/Decision Tree and Random Forest/2023-01-16-Der Entscheidungsbaum.md`
  - Falsch: `en/blog/Decision Tree and Random Forest/The-Decision-Tree`
  - Richtig: `en/blog/Decision-Tree-and-Random-Forest/The-Decision-Tree`

### Advent of Code 2025
- Alle Dateien in `en/blog/Advent of Code 2025/` und `de/blog/Advent of Code 2025/`
  - Ordnername wird zu `Advent-of-Code-2025` in der URL

### LangChain
- Alle Dateien in `en/blog/LangChain/` und `de/blog/LangChain/`
  - Ordnername bleibt `LangChain` (kein Leerzeichen, also OK)

### LangGraph
- `en/blog/LangGraph/LangGraph.md` und `de/blog/LangGraph/LangGraph.md`
  - Ordnername bleibt `LangGraph` (OK)

## Problem 2: Sonderzeichen in Dateinamen

Quartz konvertiert bestimmte Zeichen:
- Leerzeichen → Bindestrich (`-`)
- `&` → `-and-`
- `%` → `-percent`
- `?` und `#` werden entfernt

**Beispiele:**
- `Docker, Compose & Codespaces.md` → `Docker,-Compose--and--Codespaces`
- `Day 22 (& 21) - Sabotage Detection.md` → `Day-22-(-and--21)---Sabotage-Detection`

## Problem 3: Deutsche Umlaute und Sonderzeichen

- `ü`, `ä`, `ö`, `ß` werden NICHT konvertiert, bleiben in der URL
- `—` (em-dash) bleibt erhalten

**Beispiele:**
- `Eine Übersicht.md` → `Eine-Übersicht`

## Lösung

Das Skript `fix_translation_slugs.py` korrigiert diese Probleme automatisch:

```bash
# Dry-run (zeigt was geändert würde)
python3 fix_translation_slugs.py --dry-run

# Tatsächlich ändern
python3 fix_translation_slugs.py
```

## Quartz Slugify-Regeln (aus quartz/util/path.ts)

```javascript
function sluggify(s: string): string {
  return s
    .split("/")
    .map((segment) =>
      segment
        .replace(/\s/g, "-")      // Leerzeichen → Bindestrich
        .replace(/&/g, "-and-")   // & → -and-
        .replace(/%/g, "-percent") // % → -percent
        .replace(/\?/g, "")       // ? entfernen
        .replace(/#/g, ""),       // # entfernen
    )
    .join("/")
    .replace(/\/$/, "")
}
```

## Checkliste für neue Artikel

Wenn du einen neuen Artikel mit Übersetzung erstellst:

1. [ ] Prüfe, ob der Ordnername Leerzeichen enthält → slugifizieren
2. [ ] Prüfe, ob der Dateiname Sonderzeichen enthält (`&`, `%`, `?`, `#`) → slugifizieren
3. [ ] Verwende immer Anführungszeichen um den Slug-Wert im Frontmatter
4. [ ] Teste den Link nach dem Build

**Beispiel für korrektes Frontmatter:**
```yaml
---
title: "Mein Artikel"
translations:
  de: "de/blog/Ordner-Name/Datei-Name"
  en: "en/blog/Folder-Name/File-Name"
---
```
