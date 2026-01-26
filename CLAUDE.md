# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Quartz v4 static site generator instance - a tool for publishing digital gardens and notes as a website. Quartz transforms markdown content into a fully-featured website with features like graph visualization, search, backlinks, and more.

**Key characteristics:**
- The `content` directory is a git submodule (separate repository: gvtsch.github.io-content)
- Uses TypeScript, Preact (React alternative), and ESBuild
- Plugin-based architecture with transformers, filters, and emitters
- Automatically deploys to GitHub Pages on push to `v4` branch
- **Dual-language support (EN/DE)**: Custom LanguageSwitcher component with translation mappings in frontmatter

## Development Commands

```bash
# Build the site
npx quartz build

# Build and serve locally with hot reload
npx quartz build --serve

# Type checking and formatting
npm run check         # TypeScript check + Prettier check
npm run format        # Format with Prettier

# Run tests (uses Node's built-in test runner via tsx)
npm test

# Run a single test file
npx tsx --test quartz/components/languageSwitcher.test.ts

# Performance profiling
npm run profile
```

## Architecture

### Core Configuration Files

- **quartz.config.ts**: Main site configuration
  - Site metadata (title, analytics, locale)
  - Theme configuration (typography, colors for light/dark mode)
  - Ignore patterns for files to exclude
  - Plugin pipeline configuration

- **quartz.layout.ts**: Page layout and component placement
  - `sharedPageComponents`: Components used on all pages (head, header, footer)
  - `defaultContentPageLayout`: Layout for individual content pages
  - `defaultListPageLayout`: Layout for list pages (tags, folders)
  - Components are placed in `beforeBody`, `left`, `right` sections
  - Explorer `filterFn` handles language-based content filtering

### Plugin System

Plugins are organized into three categories:

1. **Transformers** (`quartz/plugins/transformers/`): Process markdown and content
   - Parse frontmatter, add syntax highlighting, handle different markdown flavors (GFM, Obsidian)
   - Process LaTeX, create table of contents, resolve links
   - Execute during markdown parsing phase

2. **Filters** (`quartz/plugins/filters/`): Determine which content to include
   - Remove drafts, filter explicit content
   - Execute after transformation, before emission

3. **Emitters** (`quartz/plugins/emitters/`): Generate output files
   - Create HTML pages, RSS feeds, sitemaps
   - Handle assets, static files, redirects
   - Generate OG images, 404 pages

**Plugin registration:** Import from `./quartz/plugins` and configure in `quartz.config.ts` under the `plugins` object.

### Component System

Components (`quartz/components/`) are Preact components that render UI elements. Each component can have:
- Main TSX component file
- `*.inline.ts` script in `scripts/` for client-side JavaScript (runs before or after DOM loaded)
- `*.scss` styles in `styles/`

Components are configured in `quartz.layout.ts` and can be passed options when instantiated.

### Dual-Language System

The site supports English and German content with language switching:

- **Content structure**: Language-specific content lives in `en/` and `de/` folders within the content submodule
- **LanguageSwitcher component** (`quartz/components/LanguageSwitcher.tsx`): Toggle button with flag icons
- **Translation mappings**: Defined in frontmatter via `translations` field:
  ```yaml
  translations:
    de: "de/beispiel-artikel"
    en: "en/example-article"
  ```
- **i18n strings**: UI translations in `quartz/i18n/locales/` (en-US.ts, de-DE.ts)
- **Locale persistence**: Stored in localStorage, used by Explorer filter and Graph

Key files for language features:
- `quartz/components/LanguageSwitcher.tsx` - Component
- `quartz/components/scripts/languageSwitcher.inline.ts` - Client-side logic
- `quartz/components/styles/languageSwitcher.scss` - Styles
- `quartz/i18n/locales/definition.ts` - Type definitions for translations
- `quartz/plugins/transformers/frontmatter.ts` - Processes translation mappings

### Build Process

Entry point: `quartz/bootstrap-cli.mjs` → `quartz/build.ts`

Build pipeline:
1. Parse markdown files from content folders using transformers
2. Filter content based on filter plugins
3. Emit output files (HTML, assets, etc.) using emitter plugins
4. Output goes to `public/` directory

The build system uses:
- `chokidar` for file watching in dev mode
- `workerpool` for parallel processing
- `esbuild` for bundling JavaScript/CSS
- `unified`/`remark`/`rehype` for markdown processing

### Content Structure

- Content lives in a **git submodule** at `content/`
- Markdown files with optional frontmatter
- Assets and attachments are processed by the Assets emitter plugin

### Important Notes

- **Submodule management**: When updating content, remember to commit both the content submodule and the main repository
- **Build output**: The `public/` directory is generated and should not be edited directly
- **Hot reload**: When using `--serve`, the dev server watches for changes and rebuilds automatically
- **Custom OG Images**: The `CustomOgImages` plugin can be commented out to speed up build time (noted in quartz.config.ts:91)
- **Date handling**: Dates are pulled from frontmatter, git history, or filesystem (priority: frontmatter → git → filesystem)
- **Link resolution**: Uses shortest path resolution for internal links

## Deployment

Automatic deployment via GitHub Actions (`.github/workflows/deploy.yml`):
- Triggers on push to `v4` branch
- Checks out code with full git history and submodules
- Runs `npm ci` and `npx quartz build`
- Deploys `public/` directory to GitHub Pages

Manual deployment: Run `npx quartz build` and push the resulting `public/` directory to your hosting provider.
