<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT License (see LICENSE file) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Site/directory structure analyzer (local and remote)**

> Built by [kraynux](https://github.com/kraynux) for [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Official page: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Previews: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-usage)

🌐 Interface and exported reports available in **17 languages** — see [Interface languages](#interface-languages).  
**Languages:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** is a TUI + CLI tool that analyzes the structure of a local directory or a remote site (HTTP crawl bounded by safeguards): full tree, statistics per file extension/family, link mapping (internal/external, all types), broken link detection. A tool of the `omega-` suite, structured in Clean Architecture — see `docs/ARCHITECTURE.md` for the full technical details.

## 1. Vision and scope

### What Omega-fold does

- Scans a local directory (real `os.walk`) or crawls a remote site breadth-first (BFS), bounded by strict safeguards.
- Builds the full tree (files/directories, depth, size) and classifies it by family (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — see [§4](#4-file-families).
- Extracts every link (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) from each HTML page/file, classifies them (absolute/relative internal, external, anchor, `mailto:`/`tel:`/`javascript:`/`data:`) and checks that they exist — see [§5](#5-links-and-checking).
- Computes statistics: breakdown by extension/family, largest files, files with the most outgoing links, most linked external domains.
- Presents the result in a TUI (Textual) or a scriptable CLI, with three exports (JSON, text, HTML with 5 themes).
- Keeps a persistent scan history (SQLite) that can be browsed and replayed.

### What Omega-fold does not do

- Content or SEO analysis (titles, meta descriptions, keyword density).
- Crawling without safeguards — depth, page count and delay between requests are always active.
- Client-side JavaScript rendering (the page is fetched as served, not executed in a headless browser).
- Active vulnerability scanning, fuzzing, brute force.
- Web dashboard.

## 2. Installation

### Requirements

- Python 3.10+
- Internet connection, for the dependencies
- For the TUI: a [Nerd Font](https://www.nerdfonts.com/) installed in the terminal, for the header icon — without it, that character renders as an empty box (same limitation as an emoji, but far more widely available among terminal users). Its absence has no effect on how the tool works; it is purely cosmetic.

### Installation

```bash
[ -d omega-fold ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Creates the `.venv` virtual environment if it does not already exist.
2. Installs the dependencies (`vendor/omega-lib/` then `pip install -e .`; `pyproject.toml` remains the single source of truth).
3. Makes `omega-fold.sh` and `install.sh` executable.
4. Adds the `fold` alias to `~/.bashrc` and `~/.zshrc` (no duplicate if already present).

### Dependencies

Declared in `pyproject.toml` (no `requirements.txt`):
- `omega-lib`: the suite's shared library (export themes, `ConfidenceLevel`) — vendored in `vendor/omega-lib/`
- `httpx`: synchronous checking of external links (`LinkChecker`)
- `aiohttp`: asynchronous HTTP crawl (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: HTML link extraction
- `jinja2`: templating for the HTML export
- Development dependencies (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Usage

### Interactive mode (TUI)

Recommended for everyday use — launched without arguments:

```bash
./omega-fold.sh
```
if you created the alias, just type `fold` in the terminal:
```bash
fold
```

Flow: splash screen (closes on a key press or a click) → main menu (Scan / History / Settings / Help) → input of the target, the type (local/remote), the mode (static/dynamic) and the remote crawl safeguards, each field carrying its own explicit label → scan (indeterminate gauge, live log of operations, Cancel button at any time) → scan details (breakdown by family and by extension, tree, broken links, export) → history (view details, **export directly** without going through the details, replay) and settings from the main menu. Adaptation to the terminal (colors, size, structural degradation) is automatic.

#### Keyboard shortcuts

| Key | Action |
|---|---|
| `↑` / `↓` | Move between the items of a screen |
| `Tab` / `Shift+Tab` | Move between the fields of a form |
| `Esc` | Back to the previous screen (exit confirmation on the home screen) |
| `t` | Next theme (applied immediately, no confirmation) |
| `r` | Refresh terminal detection |
| `a` | Show help |
| `q` | Quit (with confirmation) |

### Interface languages

The interface is available in 17 languages: French, English, Spanish, Portuguese (Brazil), Italian, German, Dutch, Polish, Russian, Simplified Chinese, Vietnamese, Thai, Indonesian, Japanese, Korean, Hindi and Arabic. The choice is made in Settings ("Langue / Language") and takes effect after the interface restarts; the `OMEGA_FOLD_LANG` variable (for example `OMEGA_FOLD_LANG=en ./omega-fold.sh`) forces a language for one session. When launched from omega-suite, omega-fold uses the suite's language. On a Linux text console (TTY), languages with a non-Latin script are shown in English for the session. The command line stays in French.

### Scriptable mode (CLI)

Any subcommand triggers CLI mode:

```bash
# Local scan (tree + internal links)
./omega-fold.sh scan /var/www/mysite --type local

# Local scan in dynamic mode (also checks external links over HTTP)
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# Remote scan (BFS crawl from the starting URL)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# History (can be filtered by target)
./omega-fold.sh history --target /var/www/mysite --limit 20

# Scan details (text, JSON or HTML) — choice of 5 export themes
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

`scan` options:

| Option | Default | Effect |
|---|---|---|
| `--type` | *(required)* | `local` or `distant` (remote) |
| `--mode` | `static` | `static` (external links not checked) or `dynamic` (checked over HTTP) |
| `--max-depth` | `5` | Maximum depth followed (remote scan) |
| `--max-pages` | `1000` | Maximum number of crawled pages (remote scan) |
| `--delay` | `100` | Delay (ms) between two requests (remote scan) |
| `--user-agent` | `omega-fold/0.1` | `User-Agent` header sent (remote scan) |
| `--respect-robots` | disabled | Respects `robots.txt` (remote scan) |

For a remote scan, a target without a scheme (`example.org`) is automatically completed to `https://example.org` — no need to specify it unless you want to force `http://` explicitly.

If the site has more pages than `--max-pages` (1000 by default), the scan stops at the limit but reports it explicitly: `scan.status` is `completed_truncated` rather than `completed`, with a visible warning in the CLI summary, the TUI details screen and the HTML export — the reported file count is then not the real size of the site; run again with a higher `--max-pages` for full coverage.

If the alias was created by `install.sh`, `fold scan ...` works from anywhere in the terminal, without the `./omega-fold.sh` prefix.

## 4. File families

Each file is classified into a family according to its extension (first match wins) — full details and an extension-by-extension table: `docs/FAMILIES.md`.

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

## 5. Links and checking

### Classification

Each link found (`href`/`src`/`action`) is classified, in this order of priority:

| Type | Recognized when | Example |
|---|---|---|
| `empty` | Empty string | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Special scheme | `mailto:x@y.z` |
| `anchor` | Starts directly with `#` (pure anchor) | `#section` |
| `external` | `http://`, `https://` or `//` (protocol-relative) | `https://example.org` |
| `absolute` | Starts with `/` | `/img/logo.png` |
| `relative` | Everything else | `img/logo.png`, `../page.html` |

`absolute` and `relative` are the two forms of an **internal** link — a `page.html#section` link stays `relative` (the trailing fragment does not make it a plain anchor; it really navigates to another resource).

### Checking

- **Internal link**: always checked against the set of paths actually found during the scan (no network request) — `absolute` resolved against the scan root, `relative` with a separator resolved against the source file's directory, `relative` without a separator (file name only) searched across the whole tree. For a remote scan, checking happens in a second pass once the crawl is finished, against the set of pages actually visited successfully — a page outside the safeguards or blocked by `robots.txt` stays `unchecked`, never `broken` by assumption.
- **External link**: checked by an HTTP request (HEAD, then GET if HEAD fails) only in `dynamic` mode — in `static` mode, it stays `unchecked`.

## 6. Remote crawl safeguards

Always active, never disableable — only their thresholds can be adjusted:

- **Depth** (`--max-depth`): only limits the queueing of new pages to crawl; links found on an already visited page are always reported in the result, even if the page they target will not be followed.
- **Page count** (`--max-pages`): limits the total number of visited pages, across all depths.
- **Delay** (`--delay`): pause between two consecutive HTTP requests.
- **Same domain**: only internal links to the same `netloc` as the starting URL are followed — checked both on the link's path and on the URL **actually loaded after redirection**: a permalink whose path looks like an internal folder (`/go/xyz`, `/public/name/`) but which actually redirects to an external domain is never treated as a page of the scanned site (its content would not be yours).
- **`robots.txt`** (`--respect-robots`): strengthens the safeguards rather than weakening them — a forbidden page is never visited, its outgoing links stay `unchecked`.

## 7. Architecture

Omega-fold is structured in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), aligned with the `omega-` suite template (see `omega-scan`/`omega-check`/`omega-deep`) and verified by `import-linter` on every change. The full details live in **`docs/ARCHITECTURE.md`**.

Very short overview:

```text
src/omega_fold/
├── domain/          Pure business logic: scans, tree, links, statistics, reports
├── application/     Use cases (commands/queries) — run_scan (local/remote), export_scan_report...
├── ports/           Contracts expected by the application (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Concrete implementations (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2 exporters — Textual is NOT here)
├── interfaces/      tui/ (Textual) and cli/ (scriptable), with strict feature parity
├── app/             Assembly (DependencyContainer, bootstrap, lifecycle)
├── core/, shared/   Cross-cutting vocabulary, non-business utilities
└── plugins/         Structure in place, empty (no confirmed extension axis)
```

Design rules:
- `domain/tree/service.py`: aggregates an already known flat list of files into a tree, never does I/O — the real traversal (`os.walk`) lives in `infrastructure/filesystem/`.
- `domain/scans/policies.py`: crawl safeguards (depth/pages/domain), pure logic testable without a network.
- `infrastructure/filesystem/` and `infrastructure/network/`: do the I/O (disk, HTTP), never judge.
- `infrastructure/exporters/`: read the already assembled scan result, never recompute a statistic.
- `infrastructure/storage/sqlite/`: only stores the source data (`scans`/`files`/`links`) — the tree and statistics are recomputed on read by the same pure functions as the initial scan (see `DECISIONS_ARCHITECTURE.md`, D-011), never duplicated in the database.

## 8. Exports

Text and HTML reports are written in the language chosen in Settings ("Export language", by default the interface language); JSON stays data and is not translated. Reports are generated in `var/exports/` by default (runtime path anchored on the project folder, `$OMEGA_FOLD_VAR_DIR` to override it), or at the given path (`--output`).

### JSON, the source of truth

Full structure of the result (`Scan` + tree + links + statistics), strictly JSON-serializable.

### Text, compact human-readable report

Summary, breakdown by family, ASCII tree (limited to 6 levels of depth — a text report is not meant to list a tree of thousands of files), list of broken links.

### HTML, self-contained web report

5 themes to choose from (`--theme`). The total size of the site is highlighted first (it is the main goal of a scan report) and shown in a readable format (KB/MB/GB...) everywhere — CLI, TUI, exports — rather than in raw bytes. Dedicated layout: container, statistics grid, SVG histogram of the breakdown by family (drawn by hand, no heavy charting dependency — same technique as the architecture diagram of `omega-deep`), extensions/largest files tables. Linked external domains show the first 20 directly and the rest in a collapsible panel (useful on a site with hundreds of external redirects); the list of broken links is collapsed by default.

The tree is rendered in native **multi-level** HTML: one `<details>` per directory, only the root open by default, each subfolder expands independently on click (inspired by an index generation script of the user's) — a browser only lays out the open content, so it stays usable even for a site with tens of thousands of files, without JavaScript.

## 9. History

Each scan is persisted (SQLite, `var/db/omega-fold.db`). History can be browsed by target (`omega-fold history --target ...`), details of a past scan (`omega-fold show <scan_id>`), or from the TUI History menu (replay included).

## 10. Terminal compatibility

The TUI (Textual) automatically detects the terminal's capabilities (emulator, size) and adapts its structural stylesheet accordingly (`complete`/`standard`/`reduced`/`mono`), with no manual flag. CLI mode always stays plain text, independent of the terminal. Policy shared by the whole `omega-` suite (`omega-lib`, `terminal/policies.py`).

### Profile according to the detected emulator

| Emulator | Initial profile |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modern SSH | `reduced` |
| Linux TTY, legacy SSH | `mono` |
| Unrecognized emulator | `reduced` (default fallback) |

### Profile according to the terminal size

| Minimum size (columns × rows) | Profile ceiling |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| below | `mono` |

The final profile is **the more restrictive of the two** (emulator and size) — refreshable live with the `r` key.

## 11. Tests

```bash
source .venv/bin/activate
lint-imports        # checks the Dependency Rule (6 contracts)
pytest -q           # 186 tests
ruff check src tests
mypy -p omega_fold
```

Structure: `tests/unit/` (domain and infrastructure without real I/O — exporters, SVG chart, TUI splash markup), `tests/integration/` (real filesystem via `tmp_path`, fake HTTP server `pytest-httpserver`, real SQLite database, end-to-end CLI), `tests/tui/` (navigation via `Pilot`, structural — no self-claimed visual verification, see `docs/ARCHITECTURE.md` §TUI interface).

## 12. Out of scope

- Content/SEO analysis
- Client-side JavaScript rendering
- Crawling without safeguards
- Active vulnerability scanning, fuzzing, brute force
- Web dashboard

---

> Omega-fold — Map a structure, check its links, never guess what has not been visited.
