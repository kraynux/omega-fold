<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licenza MIT (vedi il file LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Analizzatore della struttura di siti/directory (locale e remoto)**

> Realizzato da **kraynux** per **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Pagina ufficiale: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Anteprime: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-utilizzo)

🌐 Interfaccia e report esportati disponibili in **17 lingue** — vedi [Lingue dell'interfaccia](#lingue-dellinterfaccia).  
**Lingue:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** è uno strumento TUI + CLI che analizza la struttura di una directory locale o di un sito remoto (crawl HTTP limitato da salvaguardie): albero completo, statistiche per estensione/famiglia di file, mappa dei link (interni/esterni, di ogni tipo), rilevamento dei link interrotti. Strumento della suite `omega-`, strutturato in Clean Architecture — vedi `docs/ARCHITECTURE.md` per tutti i dettagli tecnici.

## 1. Visione e perimetro

### Cosa fa Omega-fold

- Analizza una directory locale (`os.walk` reale) o esegue il crawl di un sito remoto in ampiezza (BFS), limitato da salvaguardie rigorose.
- Costruisce l'albero completo (file/directory, profondità, dimensione) e lo classifica per famiglia (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — vedi [§4](#4-famiglie-di-file).
- Estrae tutti i link (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) da ogni pagina/file HTML, li classifica (interno assoluto/relativo, esterno, ancora, `mailto:`/`tel:`/`javascript:`/`data:`) e ne verifica l'esistenza — vedi [§5](#5-link-e-verifica).
- Calcola statistiche: ripartizione per estensione/famiglia, file più grandi, file con più link in uscita, domini esterni più collegati.
- Presenta il risultato in TUI (Textual) o in CLI scriptabile, con tre esportazioni (JSON, testo, HTML con 5 temi).
- Conserva una cronologia persistente delle scansioni (SQLite), consultabile e ripetibile.

### Cosa non fa Omega-fold

- Analisi dei contenuti o SEO (titoli, meta description, densità delle parole chiave).
- Crawl senza salvaguardie — profondità, numero di pagine e ritardo tra le richieste sempre attivi.
- Rendering JavaScript lato client (la pagina viene recuperata così come servita, non eseguita in un browser headless).
- Scansione attiva delle vulnerabilità, fuzzing, forza bruta.
- Dashboard web.

## 2. Installazione

### Prerequisiti

- Python 3.10+
- Connessione a Internet, per le dipendenze
- Per la TUI: un font [Nerd Font](https://www.nerdfonts.com/) installato nel terminale, per l'icona dell'intestazione — senza, quel carattere appare come un quadrato vuoto (stesso limite di un emoji, ma molto più diffuso tra gli utenti del terminale). La sua assenza non incide sul funzionamento; è puramente estetica.

### Installazione

```bash
[ -d omega-fold ] && echo "ℹ️ Già estratto qui, passaggio saltato." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea l'ambiente virtuale `.venv` se non esiste già.
2. Installa le dipendenze (`vendor/omega-lib/` poi `pip install -e .`; `pyproject.toml` resta l'unica fonte di verità).
3. Rende eseguibili `omega-fold.sh` e `install.sh`.
4. Aggiunge l'alias `fold` a `~/.bashrc` e `~/.zshrc` (senza duplicati se già presente).

### Dipendenze

Dichiarate in `pyproject.toml` (nessun `requirements.txt`):
- `omega-lib`: libreria condivisa della suite (temi di esportazione, `ConfidenceLevel`) — inclusa in `vendor/omega-lib/`
- `httpx`: verifica sincrona dei link esterni (`LinkChecker`)
- `aiohttp`: crawl HTTP asincrono (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: estrazione dei link HTML
- `jinja2`: template per l'esportazione HTML
- Dipendenze di sviluppo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Utilizzo

### Modalità interattiva (TUI)

Consigliata per l'uso quotidiano — avviata senza argomenti:

```bash
./omega-fold.sh
```
se hai creato l'alias, digita semplicemente `fold` nel terminale:
```bash
fold
```

Percorso: schermata iniziale (si chiude con un tasto o un clic) → menu principale (Scansiona / Cronologia / Impostazioni / Aiuto) → inserimento della destinazione, del tipo (locale/remoto), della modalità (statica/dinamica) e delle salvaguardie del crawl remoto, ogni campo con la sua etichetta esplicita → scansione (indicatore indeterminato, registro delle operazioni in tempo reale, pulsante Annulla in qualsiasi momento) → dettaglio della scansione (ripartizione per famiglia e per estensione, albero, link interrotti, esportazione) → cronologia (vedi dettaglio, **esporta direttamente** senza passare dal dettaglio, ripeti) e impostazioni dal menu principale. L'adattamento al terminale (colori, dimensioni, degradazione strutturale) è automatico.

#### Scorciatoie da tastiera

| Tasto | Azione |
|---|---|
| `↑` / `↓` | Spostarsi tra gli elementi di una schermata |
| `Tab` / `Maiusc+Tab` | Spostarsi tra i campi di un modulo |
| `Esc` | Tornare alla schermata precedente (conferma di uscita nella schermata iniziale) |
| `t` | Tema successivo (applicato subito, senza conferma) |
| `r` | Aggiornare il rilevamento del terminale |
| `a` | Mostrare l'aiuto |
| `q` | Uscire (con conferma) |

### Lingue dell'interfaccia

L'interfaccia è disponibile in 17 lingue: francese, inglese, spagnolo, portoghese (Brasile), italiano, tedesco, olandese, polacco, russo, cinese semplificato, vietnamita, thailandese, indonesiano, giapponese, coreano, hindi e arabo. La scelta si fa nelle Impostazioni («Langue / Language») e vale dopo il riavvio dell'interfaccia; la variabile `OMEGA_FOLD_LANG` (per esempio `OMEGA_FOLD_LANG=it ./omega-fold.sh`) impone una lingua per una sessione. Avviato da omega-suite, omega-fold usa la lingua della suite. In una console di testo Linux (TTY), le lingue con scrittura non latina vengono mostrate in inglese per la sessione. La riga di comando resta in francese.

### Modalità scriptabile (CLI)

Qualsiasi sottocomando attiva la modalità CLI:

```bash
# Scansione locale (albero + link interni)
./omega-fold.sh scan /var/www/miosito --type local

# Scansione locale in modalità dinamica (verifica anche i link esterni via HTTP)
./omega-fold.sh scan /var/www/miosito --type local --mode dynamic

# Scansione remota (crawl BFS dall'URL di partenza)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Cronologia (filtrabile per destinazione)
./omega-fold.sh history --target /var/www/miosito --limit 20

# Dettaglio di una scansione (testo, JSON o HTML) — 5 temi di esportazione a scelta
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

Opzioni di `scan`:

| Opzione | Predefinito | Effetto |
|---|---|---|
| `--type` | *(obbligatorio)* | `local` o `distant` (remoto) |
| `--mode` | `static` | `static` (link esterni non verificati) o `dynamic` (verificati via HTTP) |
| `--max-depth` | `5` | Profondità massima seguita (scansione remota) |
| `--max-pages` | `1000` | Numero massimo di pagine esplorate (scansione remota) |
| `--delay` | `100` | Ritardo (ms) tra due richieste (scansione remota) |
| `--user-agent` | `omega-fold/0.1` | Intestazione `User-Agent` inviata (scansione remota) |
| `--respect-robots` | disattivato | Rispetta `robots.txt` (scansione remota) |

Per una scansione remota, una destinazione senza schema (`example.org`) viene completata automaticamente in `https://example.org` — non serve indicarlo, salvo per forzare esplicitamente `http://`.

Se il sito ha più pagine di `--max-pages` (1000 per impostazione predefinita), la scansione si ferma al limite ma lo segnala esplicitamente: `scan.status` vale `completed_truncated` invece di `completed`, con un avviso visibile nel riepilogo CLI, nella schermata di dettaglio della TUI e nell'esportazione HTML — il numero di file riportato non è quindi la dimensione reale del sito; rilanciare con un `--max-pages` più alto per una copertura completa.

Se l'alias è stato creato da `install.sh`, `fold scan ...` funziona da qualsiasi punto del terminale, senza il prefisso `./omega-fold.sh`.

## 4. Famiglie di file

Ogni file è classificato in una famiglia in base alla sua estensione (vince la prima corrispondenza) — dettaglio completo e tabella estensione per estensione: `docs/FAMILIES.md`.

| Famiglia | Esempi di estensioni |
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
| `other` | tutto il resto |

## 5. Link e verifica

### Classificazione

Ogni link trovato (`href`/`src`/`action`) viene classificato, in quest'ordine di priorità:

| Tipo | Riconosciuto quando | Esempio |
|---|---|---|
| `empty` | Stringa vuota | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Schema speciale | `mailto:x@y.z` |
| `anchor` | Inizia direttamente con `#` (ancora pura) | `#section` |
| `external` | `http://`, `https://` o `//` (relativo al protocollo) | `https://example.org` |
| `absolute` | Inizia con `/` | `/img/logo.png` |
| `relative` | Tutto il resto | `img/logo.png`, `../page.html` |

`absolute` e `relative` sono le due forme di un link **interno** — un link `page.html#section` resta `relative` (il frammento finale non lo rende una semplice ancora: porta davvero a un'altra risorsa).

### Verifica

- **Link interno**: sempre verificato rispetto all'insieme dei percorsi realmente trovati durante la scansione (nessuna richiesta di rete) — `absolute` risolto rispetto alla radice della scansione, `relative` con separatore risolto rispetto alla directory del file di origine, `relative` senza separatore (solo nome di file) cercato in tutto l'albero. Per una scansione remota, la verifica avviene in un secondo passaggio a crawl terminato, rispetto all'insieme delle pagine realmente visitate con successo — una pagina fuori dalle salvaguardie o bloccata da `robots.txt` resta `unchecked`, mai `broken` per supposizione.
- **Link esterno**: verificato con una richiesta HTTP (HEAD, poi GET se HEAD fallisce) solo in modalità `dynamic` — in modalità `static` resta `unchecked`.

## 6. Salvaguardie del crawl remoto

Sempre attive, mai disattivabili — solo le loro soglie sono regolabili:

- **Profondità** (`--max-depth`): limita solo l'accodamento di nuove pagine da esplorare; i link trovati in una pagina già visitata vengono sempre riportati nel risultato, anche se la pagina a cui puntano non verrà seguita.
- **Numero di pagine** (`--max-pages`): limita il numero totale di pagine visitate, a tutte le profondità.
- **Ritardo** (`--delay`): pausa tra due richieste HTTP consecutive.
- **Stesso dominio**: vengono seguiti solo i link interni verso lo stesso `netloc` dell'URL di partenza — verificato sia sul percorso del link sia sull'URL **effettivamente caricato dopo il reindirizzamento**: un permalink il cui percorso sembra una cartella interna (`/go/xyz`, `/public/nome/`) ma che in realtà reindirizza a un dominio esterno non viene mai trattato come pagina del sito analizzato (il suo contenuto non sarebbe il tuo).
- **`robots.txt`** (`--respect-robots`): rafforza le salvaguardie invece di indebolirle — una pagina vietata non viene mai visitata, i suoi link in uscita restano `unchecked`.

## 7. Architettura

Omega-fold è strutturato in **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), allineata al modello della suite `omega-` (vedi `omega-scan`/`omega-check`/`omega-deep`) e verificata da `import-linter` a ogni modifica. Tutti i dettagli sono in **`docs/ARCHITECTURE.md`**.

Panoramica molto breve:

```text
src/omega_fold/
├── domain/          Logica di business pura: scansioni, albero (tree), link, statistiche, report
├── application/     Casi d'uso (commands/queries) — run_scan (locale/remoto), export_scan_report...
├── ports/           Contratti attesi dall'applicazione (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implementazioni concrete (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    esportatori Jinja2 — Textual NON è qui)
├── interfaces/      tui/ (Textual) e cli/ (scriptabile), con parità funzionale rigorosa
├── app/             Assemblaggio (DependencyContainer, bootstrap, ciclo di vita)
├── core/, shared/   Vocabolario trasversale, utilità non di business
└── plugins/         Struttura predisposta, vuota (nessun asse di estensione confermato)
```

Regole di progettazione:
- `domain/tree/service.py`: aggrega in albero un elenco piatto di file già noto, non fa mai I/O — il percorso reale (`os.walk`) vive in `infrastructure/filesystem/`.
- `domain/scans/policies.py`: salvaguardie del crawl (profondità/pagine/dominio), logica pura testabile senza rete.
- `infrastructure/filesystem/` e `infrastructure/network/`: fanno l'I/O (disco, HTTP), non giudicano mai.
- `infrastructure/exporters/`: leggono il risultato della scansione già assemblato, non ricalcolano mai una statistica.
- `infrastructure/storage/sqlite/`: memorizza solo i dati di origine (`scans`/`files`/`links`) — l'albero e le statistiche vengono ricalcolati in lettura dalle stesse funzioni pure della scansione iniziale (vedi `DECISIONS_ARCHITECTURE.md`, D-011), mai duplicati nel database.

## 8. Esportazioni

I report testo e HTML vengono scritti nella lingua scelta nelle Impostazioni («Lingua delle esportazioni», per impostazione predefinita quella dell'interfaccia); il JSON resta un dato, non tradotto. I report vengono generati in `var/exports/` per impostazione predefinita (percorso di esecuzione ancorato alla cartella del progetto, `$OMEGA_FOLD_VAR_DIR` per sovrascriverlo), oppure nel percorso indicato (`--output`).

### JSON, fonte di verità

Struttura completa del risultato (`Scan` + albero + link + statistiche), rigorosamente serializzabile in JSON.

### Testo, report leggibile compatto

Riepilogo, ripartizione per famiglia, albero ASCII (limitato a 6 livelli di profondità — un report testuale non è pensato per elencare un albero di migliaia di file), elenco dei link interrotti.

### HTML, report web autonomo

5 temi a scelta (`--theme`). La dimensione totale del sito è messa in evidenza per prima (è l'obiettivo principale di un report di scansione) e mostrata in formato leggibile (KB/MB/GB...) ovunque — CLI, TUI, esportazioni — anziché in byte grezzi. Impaginazione dedicata: contenitore, griglia di statistiche, istogramma SVG della ripartizione per famiglia (disegnato a mano, nessuna pesante dipendenza di grafici — stessa tecnica del diagramma di architettura di `omega-deep`), tabelle estensioni/file più grandi. I domini esterni collegati mostrano direttamente i primi 20, il resto in un pannello comprimibile (utile su un sito con centinaia di reindirizzamenti esterni); l'elenco dei link interrotti è compresso per impostazione predefinita.

L'albero è reso in HTML nativo **multilivello**: un `<details>` per directory, solo la radice aperta per impostazione predefinita, ogni sottocartella si espande in modo indipendente al clic (ispirato a uno script di generazione di indici dell'utente) — un browser impagina solo il contenuto aperto, quindi resta utilizzabile anche per un sito con decine di migliaia di file, senza JavaScript.

## 9. Cronologia

Ogni scansione viene salvata (SQLite, `var/db/omega-fold.db`). Cronologia consultabile per destinazione (`omega-fold history --target ...`), dettaglio di una scansione passata (`omega-fold show <scan_id>`), o dal menu Cronologia della TUI (ripetizione inclusa).

## 10. Compatibilità con i terminali

La TUI (Textual) rileva automaticamente le capacità del terminale (emulatore, dimensioni) e adatta di conseguenza il suo foglio di stile strutturale (`complete`/`standard`/`reduced`/`mono`), senza opzioni manuali. La modalità CLI resta sempre in testo semplice, indipendente dal terminale. Politica condivisa da tutta la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profilo secondo l'emulatore rilevato

| Emulatore | Profilo iniziale |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH datato | `mono` |
| Emulatore non riconosciuto | `reduced` (ripiego predefinito) |

### Profilo secondo le dimensioni del terminale

| Dimensione minima (colonne × righe) | Tetto del profilo |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| al di sotto | `mono` |

Il profilo finale è **il più restrittivo dei due** (emulatore e dimensioni) — aggiornabile in tempo reale con il tasto `r`.

## 11. Test

```bash
source .venv/bin/activate
lint-imports        # verifica la Dependency Rule (6 contratti)
pytest -q           # 186 test
ruff check src tests
mypy -p omega_fold
```

Struttura: `tests/unit/` (dominio e infrastruttura senza I/O reale — esportatori, grafico SVG, markup della schermata iniziale TUI), `tests/integration/` (filesystem reale via `tmp_path`, server HTTP fittizio `pytest-httpserver`, database SQLite reale, CLI end-to-end), `tests/tui/` (navigazione via `Pilot`, strutturale — nessuna verifica visiva autodichiarata, vedi `docs/ARCHITECTURE.md` §Interfaccia TUI).

## 12. Fuori perimetro

- Analisi dei contenuti/SEO
- Rendering JavaScript lato client
- Crawl senza salvaguardie
- Scansione attiva delle vulnerabilità, fuzzing, forza bruta
- Dashboard web

---

> Omega-fold — Mappare una struttura, verificarne i link, non indovinare mai ciò che non è stato visitato.
