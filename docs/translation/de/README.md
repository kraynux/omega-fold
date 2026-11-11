<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-Lizenz (siehe Datei LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Strukturanalyse für Websites/Verzeichnisse (lokal und entfernt)**

> Entwickelt von [kraynux](https://github.com/kraynux) für [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Offizielle Seite: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Vorschau: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-verwendung)

🌐 Oberfläche und exportierte Berichte in **17 Sprachen** verfügbar — siehe [Sprachen der Oberfläche](#sprachen-der-oberfläche).  
**Sprachen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** ist ein TUI- und CLI-Werkzeug, das die Struktur eines lokalen Verzeichnisses oder einer entfernten Website analysiert (HTTP-Crawl, durch Schutzgrenzen beschränkt): vollständiger Verzeichnisbaum, Statistiken nach Dateiendung/Dateifamilie, Link-Karte (intern/extern, alle Arten), Erkennung defekter Links. Werkzeug der Suite `omega-`, aufgebaut nach Clean Architecture — siehe `docs/ARCHITECTURE.md` für alle technischen Details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/de/omega-fold/D.png" width="24%" />
</p>

## 1. Vision und Umfang

### Was Omega-fold tut

- Durchsucht ein lokales Verzeichnis (echtes `os.walk`) oder crawlt eine entfernte Website in Breitensuche (BFS), begrenzt durch strenge Schutzgrenzen.
- Baut den vollständigen Verzeichnisbaum auf (Dateien/Verzeichnisse, Tiefe, Größe) und ordnet ihn nach Familien (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — siehe [§4](#4-dateifamilien).
- Extrahiert alle Links (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) aus jeder HTML-Seite/-Datei, klassifiziert sie (intern absolut/relativ, extern, Anker, `mailto:`/`tel:`/`javascript:`/`data:`) und prüft, ob sie existieren — siehe [§5](#5-links-und-prüfung).
- Berechnet Statistiken: Verteilung nach Endung/Familie, größte Dateien, Dateien mit den meisten ausgehenden Links, am häufigsten verlinkte externe Domains.
- Zeigt das Ergebnis in der TUI (Textual) oder in der skriptfähigen CLI, mit drei Exporten (JSON, Text, HTML mit 5 Themes).
- Führt einen dauerhaften Scan-Verlauf (SQLite), der eingesehen und wiederholt werden kann.

### Was Omega-fold nicht tut

- Inhalts- oder SEO-Analyse (Titel, Meta-Beschreibungen, Keyword-Dichte).
- Crawlen ohne Schutzgrenzen — Tiefe, Seitenzahl und Pause zwischen Anfragen sind immer aktiv.
- Clientseitiges JavaScript-Rendering (die Seite wird so geholt, wie sie ausgeliefert wird, nicht in einem Headless-Browser ausgeführt).
- Aktives Schwachstellen-Scannen, Fuzzing, Brute Force.
- Web-Dashboard.

## 2. Installation

### Voraussetzungen

- Python 3.10+
- Internetverbindung, für die Abhängigkeiten
- Für die TUI: eine im Terminal installierte [Nerd Font](https://www.nerdfonts.com/), für das Symbol in der Kopfzeile — ohne sie erscheint dieses Zeichen als leeres Kästchen (dieselbe Einschränkung wie bei einem Emoji, aber unter Terminal-Nutzern viel weiter verbreitet). Ihr Fehlen hat keine Auswirkung auf die Funktion, es ist rein kosmetisch.

### Installation

```bash
[ -d omega-fold ] && echo "ℹ️ Hier bereits entpackt, Schritt übersprungen." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Legt die virtuelle Umgebung `.venv` an, falls sie noch nicht existiert.
2. Installiert die Abhängigkeiten (`vendor/omega-lib/`, dann `pip install -e .`; `pyproject.toml` bleibt die einzige maßgebliche Quelle).
3. Macht `omega-fold.sh` und `install.sh` ausführbar.
4. Fügt den Alias `fold` zu `~/.bashrc` und `~/.zshrc` hinzu (ohne Duplikat, falls schon vorhanden).

### Abhängigkeiten

Deklariert in `pyproject.toml` (kein `requirements.txt`):
- `omega-lib`: gemeinsame Bibliothek der Suite (Export-Themes, `ConfidenceLevel`) — mitgeliefert in `vendor/omega-lib/`
- `httpx`: synchrone Prüfung externer Links (`LinkChecker`)
- `aiohttp`: asynchroner HTTP-Crawl (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: Extraktion der HTML-Links
- `jinja2`: Templates für den HTML-Export
- Entwicklungsabhängigkeiten (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Verwendung

### Interaktiver Modus (TUI)

Empfohlen für den täglichen Gebrauch — ohne Argumente gestartet:

```bash
./omega-fold.sh
```
wenn Sie den Alias angelegt haben, tippen Sie einfach `fold` im Terminal:
```bash
fold
```

Ablauf: Startbildschirm (schließt sich per Tastendruck oder Klick) → Hauptmenü (Scannen / Verlauf / Einstellungen / Hilfe) → Eingabe des Ziels, des Typs (lokal/entfernt), des Modus (statisch/dynamisch) und der Schutzgrenzen für den entfernten Crawl, jedes Feld mit eigener, eindeutiger Beschriftung → Scan (unbestimmte Fortschrittsanzeige, Live-Protokoll der Vorgänge, Schaltfläche Abbrechen jederzeit) → Scan-Details (Verteilung nach Familie und Endung, Verzeichnisbaum, defekte Links, Export) → Verlauf (Details ansehen, **direkt exportieren** ohne Umweg über die Details, wiederholen) und Einstellungen über das Hauptmenü. Die Anpassung an das Terminal (Farben, Größe, strukturelle Reduzierung) erfolgt automatisch.

#### Tastenkürzel

| Taste | Aktion |
|---|---|
| `↑` / `↓` | Zwischen den Elementen eines Bildschirms wechseln |
| `Tab` / `Umschalt+Tab` | Zwischen den Feldern eines Formulars wechseln |
| `Esc` | Zurück zum vorherigen Bildschirm (Bestätigung zum Beenden auf dem Startbildschirm) |
| `t` | Nächstes Theme (sofort angewendet, ohne Bestätigung) |
| `r` | Terminalerkennung aktualisieren |
| `a` | Hilfe anzeigen |
| `q` | Beenden (mit Bestätigung) |

### Sprachen der Oberfläche

Die Oberfläche ist in 17 Sprachen verfügbar: Französisch, Englisch, Spanisch, Portugiesisch (Brasilien), Italienisch, Deutsch, Niederländisch, Polnisch, Russisch, vereinfachtes Chinesisch, Vietnamesisch, Thailändisch, Indonesisch, Japanisch, Koreanisch, Hindi und Arabisch. Die Auswahl erfolgt in den Einstellungen („Langue / Language“) und gilt nach einem Neustart der Oberfläche; die Variable `OMEGA_FOLD_LANG` (zum Beispiel `OMEGA_FOLD_LANG=de ./omega-fold.sh`) erzwingt eine Sprache für eine Sitzung. Aus omega-suite gestartet, übernimmt omega-fold die Sprache der Suite. Auf einer Linux-Textkonsole (TTY) werden Sprachen mit nicht lateinischer Schrift für die Sitzung auf Englisch angezeigt. Die Kommandozeile bleibt auf Französisch.

### Kontakt und Support

Die Hilfe (Taste `a`) bietet einen Bildschirm **Kontakt und Support**: *Einen Kaffee spendieren* (PayPal-Seite des Entwicklers), *Support kontaktieren* (E-Mail-Adresse und Kontaktformular der Website, im Klartext angezeigt), *Mich als Nutzer melden (anonym)* und *Updates prüfen*. Die Meldung ist freiwillig, standardmäßig deaktiviert und wird nur ein einziges Mal gesendet: Sie dient nur dazu, die Nutzer zu zählen und, wenn gewünscht, ihren Kontinent oder ihr Land (geschlossene Listen, nie Freitext). Gesendet werden ein zufällig gezogener Schlüssel, der Name der Software (`omega-fold`) und ihre Version; nie ein Name, ein Rechnername, eine Einstellung, ein Ziel oder ein Ergebnis. Die IP-Adresse wird in den Meldungen nicht gespeichert, durchläuft aber wie jeder Besuch die Sicherheitsprüfungen und das Protokoll des Empfangsservers. Rückzug jederzeit über denselben Bildschirm (*Mich nicht mehr melden*). Die Update-Prüfung liest nur die Liste der auf der Website veröffentlichten Versionen, und nie ohne Klick.

### Skriptfähiger Modus (CLI)

Jeder Unterbefehl aktiviert den CLI-Modus:

```bash
# Lokaler Scan (Verzeichnisbaum + interne Links)
./omega-fold.sh scan /var/www/meineseite --type local

# Lokaler Scan im dynamischen Modus (prüft auch externe Links per HTTP)
./omega-fold.sh scan /var/www/meineseite --type local --mode dynamic

# Entfernter Scan (BFS-Crawl ab der Start-URL)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Verlauf (nach Ziel filterbar)
./omega-fold.sh history --target /var/www/meineseite --limit 20

# Details eines Scans (Text, JSON oder HTML) — 5 Export-Themes zur Auswahl
./omega-fold.sh show <scan_id> --format html --theme omega-base --output bericht.html
```

Optionen von `scan`:

| Option | Standard | Wirkung |
|---|---|---|
| `--type` | *(erforderlich)* | `local` oder `distant` (entfernt) |
| `--mode` | `static` | `static` (externe Links nicht geprüft) oder `dynamic` (per HTTP geprüft) |
| `--max-depth` | `5` | Maximale verfolgte Tiefe (entfernter Scan) |
| `--max-pages` | `1000` | Maximale Anzahl gecrawlter Seiten (entfernter Scan) |
| `--delay` | `100` | Pause (ms) zwischen zwei Anfragen (entfernter Scan) |
| `--user-agent` | `omega-fold/0.1` | Gesendeter `User-Agent`-Header (entfernter Scan) |
| `--respect-robots` | deaktiviert | Beachtet `robots.txt` (entfernter Scan) |

Bei einem entfernten Scan wird ein Ziel ohne Schema (`example.org`) automatisch zu `https://example.org` ergänzt — eine Angabe ist nur nötig, um ausdrücklich `http://` zu erzwingen.

Hat die Website mehr Seiten als `--max-pages` (standardmäßig 1000), hält der Scan an der Grenze an, meldet dies aber ausdrücklich: `scan.status` ist dann `completed_truncated` statt `completed`, mit einer sichtbaren Warnung in der CLI-Zusammenfassung, im Detailbildschirm der TUI und im HTML-Export — die gemeldete Dateianzahl entspricht dann nicht der tatsächlichen Größe der Website; für eine vollständige Abdeckung mit einem höheren `--max-pages` erneut starten.

Wurde der Alias von `install.sh` angelegt, funktioniert `fold scan ...` von überall im Terminal, ohne das Präfix `./omega-fold.sh`.

## 4. Dateifamilien

Jede Datei wird anhand ihrer Endung einer Familie zugeordnet (der erste Treffer gewinnt) — vollständige Details und eine Tabelle Endung für Endung: `docs/FAMILIES.md`.

| Familie | Beispiele für Endungen |
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
| `other` | alles andere |

## 5. Links und Prüfung

### Klassifizierung

Jeder gefundene Link (`href`/`src`/`action`) wird in dieser Rangfolge klassifiziert:

| Typ | Erkannt, wenn | Beispiel |
|---|---|---|
| `empty` | Leere Zeichenkette | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Besonderes Schema | `mailto:x@y.z` |
| `anchor` | Beginnt direkt mit `#` (reiner Anker) | `#section` |
| `external` | `http://`, `https://` oder `//` (protokollrelativ) | `https://example.org` |
| `absolute` | Beginnt mit `/` | `/img/logo.png` |
| `relative` | Alles andere | `img/logo.png`, `../page.html` |

`absolute` und `relative` sind die beiden Formen eines **internen** Links — ein Link `page.html#section` bleibt `relative` (das Fragment am Ende macht ihn nicht zu einem bloßen Anker, er führt tatsächlich zu einer anderen Ressource).

### Prüfung

- **Interner Link**: wird immer gegen die Menge der beim Scan tatsächlich gefundenen Pfade geprüft (keine Netzwerkanfrage) — `absolute` gegen die Wurzel des Scans aufgelöst, `relative` mit Trennzeichen gegen das Verzeichnis der Quelldatei, `relative` ohne Trennzeichen (nur Dateiname) im ganzen Baum gesucht. Bei einem entfernten Scan erfolgt die Prüfung in einem zweiten Durchgang nach Ende des Crawls, gegen die Menge der tatsächlich erfolgreich besuchten Seiten — eine Seite außerhalb der Schutzgrenzen oder durch `robots.txt` gesperrt bleibt `unchecked`, nie aufgrund einer Annahme `broken`.
- **Externer Link**: wird nur im Modus `dynamic` per HTTP-Anfrage geprüft (HEAD, dann GET, falls HEAD fehlschlägt) — im Modus `static` bleibt er `unchecked`.

## 6. Schutzgrenzen des entfernten Crawls

Immer aktiv, nie abschaltbar — nur ihre Schwellenwerte sind einstellbar:

- **Tiefe** (`--max-depth`): begrenzt nur das Einreihen neuer zu crawlender Seiten; Links, die auf einer bereits besuchten Seite gefunden werden, erscheinen immer im Ergebnis, auch wenn die Zielseite nicht weiterverfolgt wird.
- **Seitenzahl** (`--max-pages`): begrenzt die Gesamtzahl besuchter Seiten über alle Tiefen.
- **Pause** (`--delay`): Wartezeit zwischen zwei aufeinanderfolgenden HTTP-Anfragen.
- **Gleiche Domain**: Es werden nur interne Links zum selben `netloc` wie die Start-URL verfolgt — geprüft sowohl am Pfad des Links als auch an der **nach der Weiterleitung tatsächlich geladenen** URL: Ein Permalink, dessen Pfad wie ein internes Verzeichnis aussieht (`/go/xyz`, `/public/name/`), der aber in Wirklichkeit auf eine externe Domain weiterleitet, wird nie als Seite der gescannten Website behandelt (sein Inhalt wäre nicht Ihrer).
- **`robots.txt`** (`--respect-robots`): verschärft die Schutzgrenzen, statt sie abzuschwächen — eine verbotene Seite wird nie besucht, ihre ausgehenden Links bleiben `unchecked`.

## 7. Architektur

Omega-fold ist nach **Clean Architecture** aufgebaut (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), angelehnt an die Vorlage der Suite `omega-` (siehe `omega-scan`/`omega-check`/`omega-deep`) und bei jeder Änderung durch `import-linter` geprüft. Alle Details stehen in **`docs/ARCHITECTURE.md`**.

Sehr kurzer Überblick:

```text
src/omega_fold/
├── domain/          Reine Fachlogik: Scans, Verzeichnisbaum (tree), Links, Statistiken, Berichte
├── application/     Anwendungsfälle (commands/queries) — run_scan (lokal/entfernt), export_scan_report...
├── ports/           Von der Anwendung erwartete Verträge (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Konkrete Implementierungen (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2-Exporter — Textual ist NICHT hier)
├── interfaces/      tui/ (Textual) und cli/ (skriptfähig), mit strikter Funktionsgleichheit
├── app/             Zusammenbau (DependencyContainer, Bootstrap, Lebenszyklus)
├── core/, shared/   Übergreifendes Vokabular, fachfremde Hilfsmittel
└── plugins/         Struktur angelegt, leer (keine bestätigte Erweiterungsachse)
```

Entwurfsregeln:
- `domain/tree/service.py`: fasst eine bereits bekannte flache Dateiliste zu einem Baum zusammen, führt nie E/A aus — das echte Durchlaufen (`os.walk`) liegt in `infrastructure/filesystem/`.
- `domain/scans/policies.py`: Schutzgrenzen des Crawls (Tiefe/Seiten/Domain), reine Logik, ohne Netzwerk testbar.
- `infrastructure/filesystem/` und `infrastructure/network/`: führen die E/A aus (Datenträger, HTTP), bewerten nie.
- `infrastructure/exporters/`: lesen das bereits zusammengesetzte Scan-Ergebnis, berechnen nie eine Statistik neu.
- `infrastructure/storage/sqlite/`: speichert nur die Quelldaten (`scans`/`files`/`links`) — Verzeichnisbaum und Statistiken werden beim Lesen von denselben reinen Funktionen wie beim ersten Scan neu berechnet (siehe `DECISIONS_ARCHITECTURE.md`, D-011), nie in der Datenbank dupliziert.

## 8. Exporte

Text- und HTML-Berichte werden in der in den Einstellungen gewählten Sprache geschrieben („Sprache der Exporte“, standardmäßig die der Oberfläche); JSON bleibt Daten und wird nicht übersetzt. Die Berichte werden standardmäßig in `var/exports/` erzeugt (Laufzeitpfad im Projektordner verankert, mit `$OMEGA_FOLD_VAR_DIR` überschreibbar) oder unter dem angegebenen Pfad (`--output`).

### JSON, die maßgebliche Quelle

Vollständige Struktur des Ergebnisses (`Scan` + Verzeichnisbaum + Links + Statistiken), streng JSON-serialisierbar.

### Text, kompakter lesbarer Bericht

Zusammenfassung, Verteilung nach Familie, ASCII-Baum (auf 6 Ebenen begrenzt — ein Textbericht soll keinen Baum mit Tausenden von Dateien auflisten), Liste der defekten Links.

### HTML, eigenständiger Webbericht

5 Themes zur Auswahl (`--theme`). Die Gesamtgröße der Website wird zuerst hervorgehoben (das ist das Hauptziel eines Scan-Berichts) und überall — CLI, TUI, Exporte — in lesbarer Form (KB/MB/GB...) statt in rohen Bytes angezeigt. Eigenes Layout: Container, Statistikraster, SVG-Histogramm der Verteilung nach Familie (von Hand gezeichnet, keine schwere Diagrammabhängigkeit — dieselbe Technik wie das Architekturdiagramm von `omega-deep`), Tabellen der Endungen und größten Dateien. Bei den verlinkten externen Domains werden die ersten 20 direkt angezeigt, der Rest in einem aufklappbaren Bereich (nützlich bei einer Website mit Hunderten externer Weiterleitungen); die Liste der defekten Links ist standardmäßig eingeklappt.

Der Verzeichnisbaum wird als natives **mehrstufiges** HTML dargestellt: ein `<details>` pro Verzeichnis, standardmäßig nur die Wurzel geöffnet, jeder Unterordner klappt per Klick unabhängig auf (angelehnt an ein Skript des Nutzers zur Index-Erzeugung) — ein Browser setzt nur den geöffneten Inhalt, daher bleibt es selbst bei einer Website mit Zehntausenden von Dateien benutzbar, ohne JavaScript.

## 9. Verlauf

Jeder Scan wird gespeichert (SQLite, `var/db/omega-fold.db`). Verlauf nach Ziel einsehbar (`omega-fold history --target ...`), Details eines früheren Scans (`omega-fold show <scan_id>`) oder über das Menü Verlauf der TUI (inklusive Wiederholung).

## 10. Terminal-Kompatibilität

Die TUI (Textual) erkennt automatisch die Fähigkeiten des Terminals (Emulator, Größe) und passt ihr strukturelles Stylesheet entsprechend an (`complete`/`standard`/`reduced`/`mono`), ohne manuelle Option. Der CLI-Modus bleibt immer einfacher Text, unabhängig vom Terminal. Richtlinie der gesamten Suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil nach erkanntem Emulator

| Emulator | Anfangsprofil |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, modernes SSH | `reduced` |
| Linux-TTY, älteres SSH | `mono` |
| Nicht erkannter Emulator | `reduced` (Standard-Rückfall) |

### Profil nach Terminalgröße

| Mindestgröße (Spalten × Zeilen) | Profil-Obergrenze |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| darunter | `mono` |

Das endgültige Profil ist **das strengere der beiden** (Emulator und Größe) — live aktualisierbar mit der Taste `r`.

## 11. Tests

```bash
source .venv/bin/activate
lint-imports        # prüft die Dependency Rule (6 Verträge)
pytest -q           # 186 Tests
ruff check src tests
mypy -p omega_fold
```

Struktur: `tests/unit/` (Domain und Infrastruktur ohne echte E/A — Exporter, SVG-Diagramm, Markup des TUI-Startbildschirms), `tests/integration/` (echtes Dateisystem über `tmp_path`, simulierter HTTP-Server `pytest-httpserver`, echte SQLite-Datenbank, CLI von Anfang bis Ende), `tests/tui/` (Navigation über `Pilot`, strukturell — keine selbst behauptete visuelle Prüfung, siehe `docs/ARCHITECTURE.md` §TUI-Oberfläche).

## 12. Außerhalb des Umfangs

- Inhalts-/SEO-Analyse
- Clientseitiges JavaScript-Rendering
- Crawlen ohne Schutzgrenzen
- Aktives Schwachstellen-Scannen, Fuzzing, Brute Force
- Web-Dashboard

---

> Omega-fold — Eine Struktur kartieren, ihre Links prüfen, nie erraten, was nicht besucht wurde.
