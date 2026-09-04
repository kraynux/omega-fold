<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENSE file) -->
<div align="center">
  <img src="docs/assets/omega-fold.png" alt="Omega-Fold" width="256">
</div>

#  OMEGA-FOLD

**Site/directory structure analyzer (local and remote)**

> Developed by **kraynux** for **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Official page: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Previews: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-usage)

**Languages:**  
[Francais](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-fold** is a TUI + CLI tool that analyzes the structure of a local directory or a remote site (HTTP crawling bounded by safeguards): complete tree, statistics by extension/file family, link mapping (internal/external, all types), broken link detection. Fifth tool in the `omega-` suite (after `omega-scan`, `omega-stress`, `omega-check`, and `omega-deep`), structured according to Clean Architecture — see `docs/ARCHITECTURE.md` for complete technical details.

## 1. Vision and scope

### What Omega-fold does

- Scans a local directory (real `os.walk`) or crawls a remote site using BFS, bounded by strict safeguards.
- Builds the complete tree (files/directories, depth, size) and classifies by family (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — see [⁴](#4-file-families).
- Extracts all links (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) from each HTML page/file, classifies them (internal absolute/relative, external, anchor, `mailto:`/`tel:`/`javascript:`/`data:`), and verifies their existence — see [⁵](#5-links-and-verification).
- Calculates statistics: distribution by extension/family, largest files, files with the most outgoing links, most-linked external domains.
- Presents results via TUI (Textual) or scriptable CLI, with three exports (JSON, text, HTML with 5 themes).
- Keeps a persistent scan history (SQLite), replayable and viewable.

### What Omega-fold does not do

- Content or SEO analysis (titles, meta descriptions, keyword density).
- Crawling without safeguards — depth, page count, and request delay are always active.
- Client-side JavaScript rendering (page retrieved as served, not executed in a headless browser).
- Active vulnerability scanning, fuzzing, or brute force.
- Web dashboard.

## 2. Installation

### Prerequisites

- Python 3.10+
- Internet connection for dependencies
- For the TUI: a [Nerd Font](https://www.nerdfonts.com/) installed in the terminal for the header icon — without it, this character appears as an empty square (same limitation as an emoji, but much more widely available among terminal users). Its absence has no effect on operation and is purely cosmetic.

### Installation

```bash
[ -d omega-fold ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs the dependencies (`vendor/omega-lib/` followed by `pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-fold.sh` and `install.sh` executable.
4. Adds the `fold` alias to `~/.bashrc` and `~/.zshrc` (without duplicates if already present).

### Dependencies

Declared in `pyproject.toml` (no `requirements.txt`):
- `omega-lib`: shared suite library (export themes, `ConfidenceLevel`) — vendored in `vendor/omega-lib/`
- `httpx`: synchronous external link verification (`LinkChecker`)
- `aiohttp`: asynchronous HTTP crawling (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: HTML link extraction
- `jinja2`: templating for HTML export
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Usage

### Interactive mode (TUI)

Recommended for daily use — launched without arguments:

```bash
./omega-fold.sh
```
If you created the alias, simply type `fold` in the terminal:
```bash
fold
```

Flow: start screen (closes on a key press or click) → main menu (Scanner / History / Settings / Help) → target input, type (local/remote), mode (static/dynamic), and remote crawl safeguards, each field with its explicit label → scan (indeterminate gauge, live operation log, Cancel button at any time) → scan details (distribution by family and extension, tree, broken links, export) → history (view details, **export directly** without going back through details, replay) and settings from the main menu. Terminal adaptation (colors, size, structural degradation) is automatic.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Move between screen elements |
| `Tab` / `Shift+Tab` | Move between form fields |
| `Esc` | Return to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, without confirmation) |
| `r` | Refresh terminal detection |
| `a` | Display help |
| `q` | Quit (with confirmation) |

### Scriptable mode (CLI)

Any subcommand triggers CLI mode:

```bash
# Local scan (tree + internal links)
./omega-fold.sh scan /var/www/monsite --type local

# Local scan in dynamic mode (also verifies external links via HTTP)
./omega-fold.sh scan /var/www/monsite --type local --mode dynamic

# Remote scan (BFS crawl from starting URL)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# History (filterable by target)
./omega-fold.sh history --target /var/www/monsite --limit 20

# Scan details (text, JSON, or HTML) — 5 export themes available
./omega-fold.sh show <scan_id> --format html --theme omega-base --output rapport.html
```

`scan` options:

| Option | Default | Effect |
|---|---|---|
| `--type` | *(required)* | `local` or `distant` |
| `--mode` | `static` | `static` (external links not verified) or `dynamic` (verified via HTTP) |
| `--max-depth` | `5` | Maximum depth followed (remote scan) |
| `--max-pages` | `1000` | Maximum number of pages crawled (remote scan) |
| `--delay` | `100` | Delay (ms) between two requests (remote scan) |
| `--user-agent` | `omega-fold/0.1` | `User-Agent` header sent (remote scan) |
| `--respect-robots` | disabled | Respects `robots.txt` (remote scan) |

For a remote scan, a target without a scheme (`example.org`) is automatically completed to `https://example.org` — no need to specify it unless you want to force `http://` explicitly.

If the site has more pages than `--max-pages` (1000 by default), the scan stops at the limit but reports it explicitly: `scan.status` is `completed_truncated` rather than `completed`, with a warning visible in the CLI summary, TUI detail screen, and HTML export — the reported file count is then not the actual site size; rerun with a higher `--max-pages` for full coverage.

If the alias was created by `install.sh`, `fold scan ...` works from anywhere in the terminal, without the `./omega-fold.sh` prefix.

## 4. File families

Each file is classified into a family according to its extension (first match wins) — complete details and extension-by-extension table: `docs/FAMILIES.md`.

| Family | Example extensions |
|---|---|
| `images` | `.jpg`, `.png`, `.svg`, `.webp`, `.ico`... |
| `documents` | `.pdf`, `.doc`, `.xlsx`, `.odt`... |
| `code` | `.html`, `.php`, `.js`, `.ts`, `.py`, `.css`... |
| `data` | `.json`, `.xml`, `.yaml`, `.csv`, `.sql`... |
| `archives` | `.zip`, `.tar`, `.gz`, `.7z`... |
| `fonts` | `.ttf`, `.otf`, `.woff`, `.woff2`... |
| `video` | `.mp4`, `.webm`, `.mkv`... |
| `audio` | `.mp3`, `.wav`, `.flac`... |
| `text` | `.txt`, `.md`, `.rst`, `.log` |
| `other` | everything else |

## 5. Links and verification

### Classification

Each found link (`href`/`src`/`action`) is classified, in this order of priority:

| Type | Recognized when | Example |
|---|---|---|
| `empty` | Empty string | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Special scheme | `mailto:x@y.z` |
| `anchor` | Starts directly with `#` (pure anchor) | `#section` |
| `external` | `http://`, `https://`, or `//` (protocol-relative) | `https://example.org` |
| `absolute` | Starts with `/` | `/img/logo.png` |
| `relative` | Everything else | `img/logo.png`, `../page.html` |

`absolute` and `relative` are the two forms of an **internal** link — a link `page.html#section` remains `relative` (the trailing fragment does not make it a simple anchor; it still navigates to another resource).

### Verification

- **Internal link**: always verified against the set of paths actually found during the scan (no network request) — `absolute` resolved against the scan root, `relative` with a separator resolved against the source file's directory, `relative` without a separator (filename only) searched throughout the tree. For a remote scan, verification occurs in a second pass after the crawl is complete, against the set of pages actually visited successfully — a page outside safeguards or blocked by `robots.txt` remains `unchecked`, never assumed `broken`.
- **External link**: verified via an HTTP request (HEAD then GET if HEAD fails) only in `dynamic` mode — in `static` mode, it remains `unchecked`.

## 6. Remote crawl safeguards

Always active, never disableable — only their thresholds are adjustable:

- **Depth** (`--max-depth`): bounds only the queuing of new pages to crawl; links found on an already-visited page are always reported in the result, even if the page they target will not be followed.
- **Page count** (`--max-pages`): bounds the total number of pages visited, across all depths.
- **Delay** (`--delay`): pause between two consecutive HTTP requests.
- **Same domain**: only internal links to the same `netloc` as the starting URL are followed — checked both on the link path and on the URL **actually loaded after redirection**: a permalink whose path resembles an internal folder (`/go/xyz`, `/public/nom/`) but which actually redirects to an external domain is never treated as a page of the scanned site.
- **`robots.txt`** (`--respect-robots`): strengthens safeguards rather than weakening them — a forbidden page is never visited, its outgoing links remain `unchecked`.

## 7. Architecture

Omega-fold is structured according to **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-scan`/`omega-check`/`omega-deep`) and checked by `import-linter` after every change. Full details are in **`docs/ARCHITECTURE.md`**.

Very short overview:

```text
src/omega_fold/
├── domain/          Pure business logic: scans, tree, links, statistics, reports
├── application/     Use cases (commands/queries) — run_scan (local/distant), export_scan_report...
├── ports/           Contracts expected by the application (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Concrete implementations (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2 exporters — Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict functional parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary, non-business utilities
└── plugins/         Structure in place, empty (no confirmed extension axis)
```

Design rules:
- `domain/tree/service.py`: aggregates a flat list of files already known into a tree, never performs I/O — the real traversal (`os.walk`) lives in `infrastructure/filesystem/`.
- `domain/scans/policies.py`: crawl safeguards (depth/pages/domain), pure logic testable without network.
- `infrastructure/filesystem/` and `infrastructure/network/`: perform I/O (disk, HTTP), never make judgments.
- `infrastructure/exporters/`: read the already-assembled scan result, never recalculate a statistic.
- `infrastructure/storage/sqlite/`: stores only source data (`scans`/`files`/`links`) — the tree and statistics are recalculated at read time by the same pure functions as the initial scan (see `DECISIONS_ARCHITECTURE.md`, D-011), never duplicated in the database.

## 8. Exports

Reports are generated in `var/exports/` by default (runtime path anchored to the project directory, `$OMEGA_FOLD_VAR_DIR` to override it), or at the path specified by `--output`.

### JSON, source of truth

Complete result structure (`Scan` + tree + links + statistics), strictly JSON-serializable.

### Text, compact human-readable report

Summary, distribution by family, ASCII tree (bounded to 6 depth levels — a text report is not meant to list a tree of thousands of files), list of broken links.

### HTML, standalone web report

5 themes available (`--theme`). Total site size is highlighted first (this is the primary goal of a scan report) and displayed in a readable format (KB/MB/GB...) everywhere — CLI, TUI, exports — rather than raw bytes. Dedicated layout: container, statistics grid, SVG histogram of distribution by family (hand-drawn, no heavy charting dependency — same technique as the architecture diagram in `omega-deep`), extension/largest files tables. Linked external domains show the first 20 directly, the rest in a collapsible panel; the broken links list is presented collapsed by default.

The tree is rendered in native multi-level HTML: one `<details>` per directory, only the root open by default, each subdirectory expands independently on click — no JavaScript.

## 9. History

Each scan is persisted (SQLite, `var/db/omega-fold.db`). History viewable by target (`omega-fold history --target ...`), details of a past scan (`omega-fold show <scan_id>`), or from the TUI History menu (including replay).

## 10. Terminal compatibility

The TUI (Textual) automatically detects terminal capabilities (emulator, size) and adapts its structural stylesheet accordingly (`complete`/`standard`/`reduced`/`mono`), without a manual flag. CLI mode always remains plain text and independent of the terminal. This policy is shared by the entire `omega-` suite (`omega-lib`, `terminal/policies.py`).

### Profile by detected emulator

| Emulator | Initial profile |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modern SSH | `reduced` |
| Linux TTY, legacy SSH | `mono` |
| Unrecognized emulator | `reduced` (default fallback) |

### Profile by terminal size

| Minimum size (columns × rows) | Profile ceiling |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| below | `mono` |

The final profile is **the more restrictive of the two** (emulator and size) — it can be refreshed live with the `r` key.

## 11. Tests

```bash
source .venv/bin/activate
lint-imports        # checks the Dependency Rule (6 contracts)
pytest -q           # 165 tests
ruff check src tests
mypy -p omega_fold
```

Structure: `tests/unit/` (domain and infrastructure without real I/O — exporters, SVG chart, TUI splash markup), `tests/integration/` (real filesystem via `tmp_path`, fake HTTP server via `pytest-httpserver`, real SQLite database, end-to-end CLI), `tests/tui/` (navigation via `Pilot`, structural — no claimed automated visual verification, see `docs/ARCHITECTURE.md` §TUI Interface).

## 12. Out of scope

- Content/SEO analysis
- Client-side JavaScript rendering
- Crawling without safeguards
- Active vulnerability scanning, fuzzing, brute force
- Web dashboard

---

> Omega-fold — Map a structure, verify its links, and never guess what has not been visited.
