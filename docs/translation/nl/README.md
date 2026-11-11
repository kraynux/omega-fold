<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT-licentie (zie het bestand LICENSE) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-fold.png" alt="Omega-Fold" width="512">
</div>

#  OMEGA-FOLD

**Structuuranalyse van sites/mappen (lokaal en op afstand)**

> Gemaakt door [kraynux](https://github.com/kraynux) voor [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Officiële pagina: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Voorbeelden: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-gebruik)

🌐 Interface en geëxporteerde rapporten beschikbaar in **17 talen** — zie [Talen van de interface](#talen-van-de-interface).  
**Talen:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** is een TUI- en CLI-tool die de structuur van een lokale map of van een externe site analyseert (HTTP-crawl begrensd door veiligheidsgrenzen): volledige boomstructuur, statistieken per extensie/bestandsfamilie, overzicht van links (intern/extern, alle soorten), opsporing van kapotte links. Tool van de suite `omega-`, opgebouwd volgens Clean Architecture — zie `docs/ARCHITECTURE.md` voor alle technische details.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/nl/omega-fold/D.png" width="24%" />
</p>

## 1. Visie en reikwijdte

### Wat Omega-fold doet

- Scant een lokale map (echte `os.walk`) of crawlt een externe site in de breedte (BFS), begrensd door strikte veiligheidsgrenzen.
- Bouwt de volledige boomstructuur op (bestanden/mappen, diepte, grootte) en deelt die in per familie (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — zie [§4](#4-bestandsfamilies).
- Haalt alle links (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) uit elke HTML-pagina/elk HTML-bestand, deelt ze in (intern absoluut/relatief, extern, anker, `mailto:`/`tel:`/`javascript:`/`data:`) en controleert of ze bestaan — zie [§5](#5-links-en-controle).
- Berekent statistieken: verdeling per extensie/familie, grootste bestanden, bestanden met de meeste uitgaande links, meest gelinkte externe domeinen.
- Toont het resultaat in de TUI (Textual) of in een scriptbare CLI, met drie exports (JSON, tekst, HTML met 5 thema's).
- Bewaart een blijvende geschiedenis van scans (SQLite), raadpleegbaar en opnieuw uit te voeren.

### Wat Omega-fold niet doet

- Inhouds- of SEO-analyse (titels, metabeschrijvingen, trefwoorddichtheid).
- Crawlen zonder veiligheidsgrenzen — diepte, aantal pagina's en wachttijd tussen verzoeken zijn altijd actief.
- JavaScript-rendering aan de clientzijde (de pagina wordt opgehaald zoals ze geserveerd wordt, niet uitgevoerd in een headless browser).
- Actief scannen op kwetsbaarheden, fuzzing, brute force.
- Webdashboard.

## 2. Installatie

### Vereisten

- Python 3.10+
- Internetverbinding, voor de afhankelijkheden
- Voor de TUI: een [Nerd Font](https://www.nerdfonts.com/) geïnstalleerd in de terminal, voor het pictogram in de kop — zonder dit lettertype verschijnt dat teken als een leeg vakje (dezelfde beperking als bij een emoji, maar veel breder beschikbaar bij terminalgebruikers). Het ontbreken ervan heeft geen invloed op de werking, het is puur cosmetisch.

### Installatie

```bash
[ -d omega-fold ] && echo "ℹ️ Hier al uitgepakt, stap overgeslagen." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Maakt de virtuele omgeving `.venv` aan als die nog niet bestaat.
2. Installeert de afhankelijkheden (`vendor/omega-lib/` en daarna `pip install -e .`; `pyproject.toml` blijft de enige bron van waarheid).
3. Maakt `omega-fold.sh` en `install.sh` uitvoerbaar.
4. Voegt de alias `fold` toe aan `~/.bashrc` en `~/.zshrc` (zonder dubbel als hij er al staat).

### Afhankelijkheden

Gedeclareerd in `pyproject.toml` (geen `requirements.txt`):
- `omega-lib`: gedeelde bibliotheek van de suite (exportthema's, `ConfidenceLevel`) — meegeleverd in `vendor/omega-lib/`
- `httpx`: synchrone controle van externe links (`LinkChecker`)
- `aiohttp`: asynchrone HTTP-crawl (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: extractie van HTML-links
- `jinja2`: templates voor de HTML-export
- Ontwikkelafhankelijkheden (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Gebruik

### Interactieve modus (TUI)

Aanbevolen voor dagelijks gebruik — gestart zonder argumenten:

```bash
./omega-fold.sh
```
als u de alias hebt aangemaakt, typ dan gewoon `fold` in de terminal:
```bash
fold
```

Verloop: startscherm (sluit met een toets of een klik) → hoofdmenu (Scannen / Geschiedenis / Instellingen / Help) → invoer van het doel, het type (lokaal/op afstand), de modus (statisch/dynamisch) en de veiligheidsgrenzen van de crawl op afstand, elk veld met een eigen duidelijk label → scan (onbepaalde voortgangsbalk, live verslag van de bewerkingen, knop Annuleren op elk moment) → details van de scan (verdeling per familie en per extensie, boomstructuur, kapotte links, export) → geschiedenis (details bekijken, **direct exporteren** zonder via de details te gaan, opnieuw uitvoeren) en instellingen vanuit het hoofdmenu. De aanpassing aan de terminal (kleuren, grootte, structurele vereenvoudiging) gebeurt automatisch.

#### Sneltoetsen

| Toets | Actie |
|---|---|
| `↑` / `↓` | Tussen de elementen van een scherm bewegen |
| `Tab` / `Shift+Tab` | Tussen de velden van een formulier bewegen |
| `Esc` | Terug naar het vorige scherm (bevestiging om af te sluiten op het startscherm) |
| `t` | Volgend thema (direct toegepast, zonder bevestiging) |
| `r` | Terminaldetectie vernieuwen |
| `a` | Help tonen |
| `q` | Afsluiten (met bevestiging) |

### Talen van de interface

De interface is beschikbaar in 17 talen: Frans, Engels, Spaans, Portugees (Brazilië), Italiaans, Duits, Nederlands, Pools, Russisch, vereenvoudigd Chinees, Vietnamees, Thai, Indonesisch, Japans, Koreaans, Hindi en Arabisch. De keuze gebeurt in de Instellingen („Langue / Language”) en geldt na een herstart van de interface; de variabele `OMEGA_FOLD_LANG` (bijvoorbeeld `OMEGA_FOLD_LANG=nl ./omega-fold.sh`) legt voor één sessie een taal op. Gestart vanuit omega-suite neemt omega-fold de taal van de suite over. Op een Linux-tekstconsole (TTY) worden talen met een niet-Latijns schrift voor die sessie in het Engels getoond. De opdrachtregel blijft in het Frans.

### Contact en ondersteuning

De hulp (toets `a`) biedt een scherm **Contact en ondersteuning**: *Trakteer op een koffie* (PayPal-pagina van de ontwikkelaar), *Contact opnemen met ondersteuning* (e-mailadres en contactformulier van de site, leesbaar weergegeven), *Mij aanmelden als gebruiker (anoniem)* en *Updates controleren*. De aanmelding is vrijwillig, standaard uitgeschakeld en wordt maar één keer verzonden: ze dient alleen om de gebruikers te tellen en, als u dat wilt, hun continent of land (gesloten lijsten, nooit vrije tekst). Ze verzendt een willekeurig gekozen sleutel, de naam van de software (`omega-fold`) en de versie; nooit een naam, een machinenaam, een instelling, een doel of een resultaat. Het IP-adres wordt niet opgeslagen in de aanmeldingen, maar gaat, zoals bij elk bezoek, door de beveiligingscontroles en het logboek van de ontvangende server. Intrekken kan op elk moment vanuit hetzelfde scherm (*Mij niet meer aanmelden*). De updatecontrole leest alleen de lijst van versies die op de site gepubliceerd zijn, en nooit zonder klik.

### Scriptbare modus (CLI)

Elke subopdracht activeert de CLI-modus:

```bash
# Lokale scan (boomstructuur + interne links)
./omega-fold.sh scan /var/www/mijnsite --type local

# Lokale scan in dynamische modus (controleert ook externe links via HTTP)
./omega-fold.sh scan /var/www/mijnsite --type local --mode dynamic

# Scan op afstand (BFS-crawl vanaf de start-URL)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Geschiedenis (te filteren op doel)
./omega-fold.sh history --target /var/www/mijnsite --limit 20

# Details van een scan (tekst, JSON of HTML) — keuze uit 5 exportthema's
./omega-fold.sh show <scan_id> --format html --theme omega-base --output rapport.html
```

Opties van `scan`:

| Optie | Standaard | Effect |
|---|---|---|
| `--type` | *(verplicht)* | `local` of `distant` (op afstand) |
| `--mode` | `static` | `static` (externe links niet gecontroleerd) of `dynamic` (gecontroleerd via HTTP) |
| `--max-depth` | `5` | Maximale gevolgde diepte (scan op afstand) |
| `--max-pages` | `1000` | Maximaal aantal gecrawlde pagina's (scan op afstand) |
| `--delay` | `100` | Wachttijd (ms) tussen twee verzoeken (scan op afstand) |
| `--user-agent` | `omega-fold/0.1` | Verzonden `User-Agent`-header (scan op afstand) |
| `--respect-robots` | uitgeschakeld | Respecteert `robots.txt` (scan op afstand) |

Bij een scan op afstand wordt een doel zonder schema (`example.org`) automatisch aangevuld tot `https://example.org` — u hoeft het alleen op te geven om uitdrukkelijk `http://` af te dwingen.

Heeft de site meer pagina's dan `--max-pages` (standaard 1000), dan stopt de scan bij de grens, maar meldt dit uitdrukkelijk: `scan.status` is dan `completed_truncated` in plaats van `completed`, met een zichtbare waarschuwing in de CLI-samenvatting, het detailscherm van de TUI en de HTML-export — het gemelde aantal bestanden is dan niet de echte omvang van de site; start opnieuw met een hogere `--max-pages` voor volledige dekking.

Als de alias door `install.sh` is aangemaakt, werkt `fold scan ...` overal in de terminal, zonder het voorvoegsel `./omega-fold.sh`.

## 4. Bestandsfamilies

Elk bestand wordt op basis van zijn extensie in een familie ingedeeld (de eerste overeenkomst wint) — volledige details en een tabel per extensie: `docs/FAMILIES.md`.

| Familie | Voorbeelden van extensies |
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
| `other` | al het overige |

## 5. Links en controle

### Indeling

Elke gevonden link (`href`/`src`/`action`) wordt ingedeeld in deze volgorde van voorrang:

| Type | Herkend wanneer | Voorbeeld |
|---|---|---|
| `empty` | Lege tekenreeks | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Speciaal schema | `mailto:x@y.z` |
| `anchor` | Begint direct met `#` (puur anker) | `#section` |
| `external` | `http://`, `https://` of `//` (protocolrelatief) | `https://example.org` |
| `absolute` | Begint met `/` | `/img/logo.png` |
| `relative` | Al het overige | `img/logo.png`, `../page.html` |

`absolute` en `relative` zijn de twee vormen van een **interne** link — een link `page.html#section` blijft `relative` (het fragment aan het eind maakt er geen gewoon anker van; hij gaat echt naar een andere bron).

### Controle

- **Interne link**: altijd gecontroleerd tegen de verzameling paden die tijdens de scan echt gevonden zijn (geen netwerkverzoek) — `absolute` opgelost vanaf de wortel van de scan, `relative` met scheidingsteken opgelost vanaf de map van het bronbestand, `relative` zonder scheidingsteken (alleen bestandsnaam) gezocht in de hele boom. Bij een scan op afstand gebeurt de controle in een tweede ronde na afloop van de crawl, tegen de verzameling pagina's die echt met succes bezocht zijn — een pagina buiten de veiligheidsgrenzen of geblokkeerd door `robots.txt` blijft `unchecked`, nooit `broken` op basis van een aanname.
- **Externe link**: gecontroleerd met een HTTP-verzoek (HEAD, daarna GET als HEAD mislukt), alleen in modus `dynamic` — in modus `static` blijft hij `unchecked`.

## 6. Veiligheidsgrenzen van de crawl op afstand

Altijd actief, nooit uit te schakelen — alleen hun drempels zijn instelbaar:

- **Diepte** (`--max-depth`): begrenst alleen het in de wachtrij zetten van nieuwe te crawlen pagina's; links die op een al bezochte pagina gevonden worden, staan altijd in het resultaat, ook als de pagina waarnaar ze verwijzen niet gevolgd wordt.
- **Aantal pagina's** (`--max-pages`): begrenst het totale aantal bezochte pagina's, over alle diepten.
- **Wachttijd** (`--delay`): pauze tussen twee opeenvolgende HTTP-verzoeken.
- **Zelfde domein**: alleen interne links naar dezelfde `netloc` als de start-URL worden gevolgd — gecontroleerd zowel op het pad van de link als op de URL die **na omleiding echt geladen** is: een permalink waarvan het pad op een interne map lijkt (`/go/xyz`, `/public/naam/`) maar die in werkelijkheid naar een extern domein omleidt, wordt nooit behandeld als een pagina van de gescande site (de inhoud zou niet de uwe zijn).
- **`robots.txt`** (`--respect-robots`): versterkt de veiligheidsgrenzen in plaats van ze te verzwakken — een verboden pagina wordt nooit bezocht, haar uitgaande links blijven `unchecked`.

## 7. Architectuur

Omega-fold is opgebouwd volgens **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), afgestemd op het sjabloon van de suite `omega-` (zie `omega-scan`/`omega-check`/`omega-deep`) en bij elke wijziging gecontroleerd door `import-linter`. Alle details staan in **`docs/ARCHITECTURE.md`**.

Zeer kort overzicht:

```text
src/omega_fold/
├── domain/          Pure bedrijfslogica: scans, boomstructuur (tree), links, statistieken, rapporten
├── application/     Use cases (commands/queries) — run_scan (lokaal/op afstand), export_scan_report...
├── ports/           Contracten die de applicatie verwacht (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Concrete implementaties (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2-exporteurs — Textual staat hier NIET)
├── interfaces/      tui/ (Textual) en cli/ (scriptbaar), met strikte functionele gelijkwaardigheid
├── app/             Samenstelling (DependencyContainer, bootstrap, levenscyclus)
├── core/, shared/   Gedeeld vocabulaire, niet-bedrijfsmatige hulpmiddelen
└── plugins/         Structuur aanwezig, leeg (geen bevestigde uitbreidingsas)
```

Ontwerpregels:
- `domain/tree/service.py`: voegt een al bekende platte lijst van bestanden samen tot een boom, doet nooit I/O — het echte doorlopen (`os.walk`) zit in `infrastructure/filesystem/`.
- `domain/scans/policies.py`: veiligheidsgrenzen van de crawl (diepte/pagina's/domein), pure logica, zonder netwerk te testen.
- `infrastructure/filesystem/` en `infrastructure/network/`: doen de I/O (schijf, HTTP), oordelen nooit.
- `infrastructure/exporters/`: lezen het al samengestelde scanresultaat, herberekenen nooit een statistiek.
- `infrastructure/storage/sqlite/`: slaat alleen de brongegevens op (`scans`/`files`/`links`) — de boomstructuur en de statistieken worden bij het lezen opnieuw berekend door dezelfde pure functies als de oorspronkelijke scan (zie `DECISIONS_ARCHITECTURE.md`, D-011), nooit gedupliceerd in de database.

## 8. Exports

Tekst- en HTML-rapporten worden geschreven in de taal die in de Instellingen gekozen is („Taal van de exports”, standaard die van de interface); JSON blijft data en wordt niet vertaald. De rapporten worden standaard aangemaakt in `var/exports/` (runtimepad verankerd in de projectmap, `$OMEGA_FOLD_VAR_DIR` om het te overschrijven), of op het opgegeven pad (`--output`).

### JSON, de bron van waarheid

Volledige structuur van het resultaat (`Scan` + boomstructuur + links + statistieken), strikt JSON-serialiseerbaar.

### Tekst, compact leesbaar rapport

Samenvatting, verdeling per familie, ASCII-boom (beperkt tot 6 niveaus diep — een tekstrapport is niet bedoeld om een boom van duizenden bestanden op te sommen), lijst van kapotte links.

### HTML, zelfstandig webrapport

5 thema's naar keuze (`--theme`). De totale grootte van de site wordt als eerste uitgelicht (dat is het hoofddoel van een scanrapport) en overal — CLI, TUI, exports — in leesbare vorm (kB/MB/GB...) getoond in plaats van in ruwe bytes. Eigen opmaak: container, raster met statistieken, SVG-histogram van de verdeling per familie (met de hand getekend, geen zware grafiekafhankelijkheid — dezelfde techniek als het architectuurdiagram van `omega-deep`), tabellen van extensies/grootste bestanden. Van de gelinkte externe domeinen worden de eerste 20 direct getoond, de rest in een inklapbaar paneel (handig bij een site met honderden externe omleidingen); de lijst van kapotte links is standaard ingeklapt.

De boomstructuur wordt weergegeven als native **meerlaagse** HTML: één `<details>` per map, standaard alleen de wortel open, elke submap klapt onafhankelijk open bij een klik (geïnspireerd op een script van de gebruiker om indexen te maken) — een browser zet alleen de geopende inhoud op, dus het blijft bruikbaar, zelfs voor een site met tienduizenden bestanden, zonder JavaScript.

## 9. Geschiedenis

Elke scan wordt opgeslagen (SQLite, `var/db/omega-fold.db`). Geschiedenis raadpleegbaar per doel (`omega-fold history --target ...`), details van een eerdere scan (`omega-fold show <scan_id>`), of via het menu Geschiedenis van de TUI (opnieuw uitvoeren inbegrepen).

## 10. Compatibiliteit met terminals

De TUI (Textual) detecteert automatisch de mogelijkheden van de terminal (emulator, grootte) en past zijn structurele stijlblad daarop aan (`complete`/`standard`/`reduced`/`mono`), zonder handmatige optie. De CLI-modus blijft altijd platte tekst, onafhankelijk van de terminal. Beleid dat de hele suite `omega-` deelt (`omega-lib`, `terminal/policies.py`).

### Profiel volgens de gedetecteerde emulator

| Emulator | Beginprofiel |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, moderne SSH | `reduced` |
| Linux-TTY, oudere SSH | `mono` |
| Niet herkende emulator | `reduced` (standaard terugvaloptie) |

### Profiel volgens de grootte van de terminal

| Minimale grootte (kolommen × regels) | Profielplafond |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| kleiner | `mono` |

Het uiteindelijke profiel is **het strengste van de twee** (emulator en grootte) — live te vernieuwen met de toets `r`.

## 11. Tests

```bash
source .venv/bin/activate
lint-imports        # controleert de Dependency Rule (6 contracten)
pytest -q           # 186 tests
ruff check src tests
mypy -p omega_fold
```

Structuur: `tests/unit/` (domein en infrastructuur zonder echte I/O — exporteurs, SVG-grafiek, opmaak van het TUI-startscherm), `tests/integration/` (echt bestandssysteem via `tmp_path`, nagebootste HTTP-server `pytest-httpserver`, echte SQLite-database, CLI van begin tot eind), `tests/tui/` (navigatie via `Pilot`, structureel — geen zelf geclaimde visuele controle, zie `docs/ARCHITECTURE.md` §TUI-interface).

## 12. Buiten de reikwijdte

- Inhouds-/SEO-analyse
- JavaScript-rendering aan de clientzijde
- Crawlen zonder veiligheidsgrenzen
- Actief scannen op kwetsbaarheden, fuzzing, brute force
- Webdashboard

---

> Omega-fold — Een structuur in kaart brengen, de links controleren, nooit raden wat niet bezocht is.
