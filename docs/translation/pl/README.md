<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencja MIT (zobacz plik LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Analizator struktury stron i katalogów (lokalnie i zdalnie)**

> Stworzone przez **kraynux** dla **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Oficjalna strona: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Zrzuty ekranu: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-użycie)

🌐 Interfejs i eksportowane raporty dostępne w **17 językach** — zobacz [Języki interfejsu](#języki-interfejsu).  
**Języki:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** to narzędzie TUI + CLI, które analizuje strukturę lokalnego katalogu lub zdalnej strony (crawl HTTP ograniczony zabezpieczeniami): pełne drzewo, statystyki według rozszerzeń/rodzin plików, mapa odnośników (wewnętrznych/zewnętrznych, wszystkich rodzajów), wykrywanie niedziałających odnośników. Narzędzie pakietu `omega-`, zbudowane zgodnie z Clean Architecture — pełne szczegóły techniczne w `docs/ARCHITECTURE.md`.

## 1. Wizja i zakres

### Co robi Omega-fold

- Skanuje lokalny katalog (prawdziwe `os.walk`) lub przeszukuje zdalną stronę wszerz (BFS), w granicach ścisłych zabezpieczeń.
- Buduje pełne drzewo (pliki/katalogi, głębokość, rozmiar) i klasyfikuje je według rodzin (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — zobacz [§4](#4-rodziny-plików).
- Wyodrębnia wszystkie odnośniki (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) z każdej strony/pliku HTML, klasyfikuje je (wewnętrzny bezwzględny/względny, zewnętrzny, kotwica, `mailto:`/`tel:`/`javascript:`/`data:`) i sprawdza, czy istnieją — zobacz [§5](#5-odnośniki-i-sprawdzanie).
- Oblicza statystyki: podział według rozszerzeń/rodzin, największe pliki, pliki z największą liczbą odnośników wychodzących, najczęściej linkowane domeny zewnętrzne.
- Przedstawia wynik w TUI (Textual) lub w skryptowalnym CLI, z trzema eksportami (JSON, tekst, HTML z 5 motywami).
- Prowadzi trwałą historię skanów (SQLite), którą można przeglądać i odtwarzać.

### Czego Omega-fold nie robi

- Analizy treści ani SEO (tytuły, metaopisy, gęstość słów kluczowych).
- Przeszukiwania bez zabezpieczeń — głębokość, liczba stron i opóźnienie między żądaniami są zawsze aktywne.
- Renderowania JavaScriptu po stronie klienta (strona jest pobierana tak, jak jest serwowana, a nie wykonywana w przeglądarce headless).
- Aktywnego skanowania podatności, fuzzingu, ataków brute force.
- Panelu WWW.

## 2. Instalacja

### Wymagania

- Python 3.10+
- Połączenie z Internetem, dla zależności
- Dla TUI: czcionka [Nerd Font](https://www.nerdfonts.com/) zainstalowana w terminalu, dla ikony w nagłówku — bez niej ten znak wyświetla się jako puste pole (to samo ograniczenie co przy emoji, ale znacznie częściej dostępne u użytkowników terminala). Jej brak nie wpływa na działanie, ma znaczenie czysto kosmetyczne.

### Instalacja

```bash
[ -d omega-fold ] && echo "ℹ️ Już tu rozpakowano, krok pominięty." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Tworzy środowisko wirtualne `.venv`, jeśli jeszcze nie istnieje.
2. Instaluje zależności (`vendor/omega-lib/`, a potem `pip install -e .`; `pyproject.toml` pozostaje jedynym źródłem prawdy).
3. Nadaje plikom `omega-fold.sh` i `install.sh` prawo wykonywania.
4. Dodaje alias `fold` do `~/.bashrc` i `~/.zshrc` (bez duplikatu, jeśli już istnieje).

### Zależności

Zadeklarowane w `pyproject.toml` (bez `requirements.txt`):
- `omega-lib`: wspólna biblioteka pakietu (motywy eksportu, `ConfidenceLevel`) — dołączona w `vendor/omega-lib/`
- `httpx`: synchroniczne sprawdzanie odnośników zewnętrznych (`LinkChecker`)
- `aiohttp`: asynchroniczny crawl HTTP (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: wyodrębnianie odnośników HTML
- `jinja2`: szablony dla eksportu HTML
- Zależności deweloperskie (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Użycie

### Tryb interaktywny (TUI)

Zalecany do codziennego użytku — uruchamiany bez argumentów:

```bash
./omega-fold.sh
```
jeśli utworzono alias, wystarczy wpisać `fold` w terminalu:
```bash
fold
```

Przebieg: ekran startowy (zamyka się klawiszem lub kliknięciem) → menu główne (Skanuj / Historia / Ustawienia / Pomoc) → wprowadzenie celu, typu (lokalny/zdalny), trybu (statyczny/dynamiczny) i zabezpieczeń zdalnego crawla, każde pole z własną wyraźną etykietą → skan (nieokreślony wskaźnik postępu, bieżący dziennik operacji, przycisk Anuluj w każdej chwili) → szczegóły skanu (podział według rodzin i rozszerzeń, drzewo, niedziałające odnośniki, eksport) → historia (podgląd szczegółów, **bezpośredni eksport** bez przechodzenia przez szczegóły, ponowne uruchomienie) i ustawienia z menu głównego. Dopasowanie do terminala (kolory, rozmiar, uproszczenie struktury) jest automatyczne.

#### Skróty klawiszowe

| Klawisz | Działanie |
|---|---|
| `↑` / `↓` | Przechodzenie między elementami ekranu |
| `Tab` / `Shift+Tab` | Przechodzenie między polami formularza |
| `Esc` | Powrót do poprzedniego ekranu (potwierdzenie wyjścia na ekranie głównym) |
| `t` | Następny motyw (stosowany od razu, bez potwierdzenia) |
| `r` | Odświeżenie wykrywania terminala |
| `a` | Wyświetlenie pomocy |
| `q` | Wyjście (z potwierdzeniem) |

### Języki interfejsu

Interfejs jest dostępny w 17 językach: francuskim, angielskim, hiszpańskim, portugalskim (Brazylia), włoskim, niemieckim, niderlandzkim, polskim, rosyjskim, chińskim uproszczonym, wietnamskim, tajskim, indonezyjskim, japońskim, koreańskim, hindi i arabskim. Wyboru dokonuje się w Ustawieniach („Langue / Language”), a zmiana obowiązuje po ponownym uruchomieniu interfejsu; zmienna `OMEGA_FOLD_LANG` (na przykład `OMEGA_FOLD_LANG=pl ./omega-fold.sh`) wymusza język na czas jednej sesji. Uruchomiony z omega-suite, omega-fold przejmuje język pakietu. W tekstowej konsoli Linuksa (TTY) języki o piśmie innym niż łacińskie są na czas sesji wyświetlane po angielsku. Wiersz poleceń pozostaje po francusku.

### Tryb skryptowy (CLI)

Każde podpolecenie włącza tryb CLI:

```bash
# Skan lokalny (drzewo + odnośniki wewnętrzne)
./omega-fold.sh scan /var/www/mojastrona --type local

# Skan lokalny w trybie dynamicznym (sprawdza też odnośniki zewnętrzne przez HTTP)
./omega-fold.sh scan /var/www/mojastrona --type local --mode dynamic

# Skan zdalny (crawl BFS od początkowego URL)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Historia (z filtrowaniem według celu)
./omega-fold.sh history --target /var/www/mojastrona --limit 20

# Szczegóły skanu (tekst, JSON lub HTML) — do wyboru 5 motywów eksportu
./omega-fold.sh show <scan_id> --format html --theme omega-base --output raport.html
```

Opcje `scan`:

| Opcja | Domyślnie | Działanie |
|---|---|---|
| `--type` | *(wymagane)* | `local` lub `distant` (zdalny) |
| `--mode` | `static` | `static` (odnośniki zewnętrzne niesprawdzane) lub `dynamic` (sprawdzane przez HTTP) |
| `--max-depth` | `5` | Maksymalna śledzona głębokość (skan zdalny) |
| `--max-pages` | `1000` | Maksymalna liczba przeszukanych stron (skan zdalny) |
| `--delay` | `100` | Opóźnienie (ms) między dwoma żądaniami (skan zdalny) |
| `--user-agent` | `omega-fold/0.1` | Wysyłany nagłówek `User-Agent` (skan zdalny) |
| `--respect-robots` | wyłączone | Przestrzega `robots.txt` (skan zdalny) |

W skanie zdalnym cel bez schematu (`example.org`) jest automatycznie uzupełniany do `https://example.org` — nie trzeba go podawać, chyba że chce się jawnie wymusić `http://`.

Jeśli strona ma więcej stron niż `--max-pages` (domyślnie 1000), skan zatrzymuje się na limicie, ale wyraźnie to zgłasza: `scan.status` ma wartość `completed_truncated` zamiast `completed`, z widocznym ostrzeżeniem w podsumowaniu CLI, na ekranie szczegółów TUI i w eksporcie HTML — podana liczba plików nie jest wtedy rzeczywistym rozmiarem strony; aby uzyskać pełne pokrycie, uruchom ponownie z wyższym `--max-pages`.

Jeśli alias utworzył `install.sh`, `fold scan ...` działa z dowolnego miejsca w terminalu, bez przedrostka `./omega-fold.sh`.

## 4. Rodziny plików

Każdy plik jest przypisywany do rodziny na podstawie rozszerzenia (wygrywa pierwsze dopasowanie) — pełne szczegóły i tabela rozszerzenie po rozszerzeniu: `docs/FAMILIES.md`.

| Rodzina | Przykładowe rozszerzenia |
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
| `other` | wszystko inne |

## 5. Odnośniki i sprawdzanie

### Klasyfikacja

Każdy znaleziony odnośnik (`href`/`src`/`action`) jest klasyfikowany w tej kolejności pierwszeństwa:

| Typ | Rozpoznawany, gdy | Przykład |
|---|---|---|
| `empty` | Pusty ciąg | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Specjalny schemat | `mailto:x@y.z` |
| `anchor` | Zaczyna się bezpośrednio od `#` (czysta kotwica) | `#section` |
| `external` | `http://`, `https://` lub `//` (względny wobec protokołu) | `https://example.org` |
| `absolute` | Zaczyna się od `/` | `/img/logo.png` |
| `relative` | Wszystko inne | `img/logo.png`, `../page.html` |

`absolute` i `relative` to dwie postaci odnośnika **wewnętrznego** — odnośnik `page.html#section` pozostaje `relative` (końcowy fragment nie czyni z niego zwykłej kotwicy; naprawdę prowadzi do innego zasobu).

### Sprawdzanie

- **Odnośnik wewnętrzny**: zawsze sprawdzany względem zbioru ścieżek rzeczywiście znalezionych podczas skanu (bez żądania sieciowego) — `absolute` rozwiązywany względem korzenia skanu, `relative` z separatorem względem katalogu pliku źródłowego, `relative` bez separatora (sama nazwa pliku) wyszukiwany w całym drzewie. W skanie zdalnym sprawdzanie odbywa się w drugim przebiegu po zakończeniu crawla, względem zbioru stron rzeczywiście odwiedzonych z powodzeniem — strona poza zabezpieczeniami lub zablokowana przez `robots.txt` pozostaje `unchecked`, nigdy `broken` na podstawie przypuszczenia.
- **Odnośnik zewnętrzny**: sprawdzany żądaniem HTTP (HEAD, potem GET, jeśli HEAD się nie powiedzie) tylko w trybie `dynamic` — w trybie `static` pozostaje `unchecked`.

## 6. Zabezpieczenia zdalnego crawla

Zawsze aktywne, nigdy niewyłączalne — regulować można tylko ich progi:

- **Głębokość** (`--max-depth`): ogranicza wyłącznie dodawanie nowych stron do kolejki; odnośniki znalezione na już odwiedzonej stronie zawsze trafiają do wyniku, nawet jeśli strona docelowa nie będzie śledzona.
- **Liczba stron** (`--max-pages`): ogranicza łączną liczbę odwiedzonych stron na wszystkich głębokościach.
- **Opóźnienie** (`--delay`): przerwa między dwoma kolejnymi żądaniami HTTP.
- **Ta sama domena**: śledzone są tylko odnośniki wewnętrzne do tego samego `netloc` co początkowy URL — sprawdzane zarówno na ścieżce odnośnika, jak i na URL **rzeczywiście załadowanym po przekierowaniu**: permalink, którego ścieżka wygląda jak wewnętrzny folder (`/go/xyz`, `/public/nazwa/`), ale który w rzeczywistości przekierowuje do zewnętrznej domeny, nigdy nie jest traktowany jako strona skanowanego serwisu (jego treść nie byłaby twoja).
- **`robots.txt`** (`--respect-robots`): wzmacnia zabezpieczenia zamiast je osłabiać — zabroniona strona nigdy nie jest odwiedzana, jej odnośniki wychodzące pozostają `unchecked`.

## 7. Architektura

Omega-fold jest zbudowany zgodnie z **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), wzorowaną na szablonie pakietu `omega-` (zobacz `omega-scan`/`omega-check`/`omega-deep`) i sprawdzaną przez `import-linter` przy każdej zmianie. Wszystkie szczegóły znajdują się w **`docs/ARCHITECTURE.md`**.

Bardzo krótki przegląd:

```text
src/omega_fold/
├── domain/          Czysta logika biznesowa: skany, drzewo (tree), odnośniki, statystyki, raporty
├── application/     Przypadki użycia (commands/queries) — run_scan (lokalny/zdalny), export_scan_report...
├── ports/           Kontrakty oczekiwane przez aplikację (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Konkretne implementacje (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    eksportery Jinja2 — Textual NIE jest tutaj)
├── interfaces/      tui/ (Textual) i cli/ (skryptowalne), ze ścisłą równością funkcji
├── app/             Składanie (DependencyContainer, bootstrap, cykl życia)
├── core/, shared/   Wspólne słownictwo, narzędzia niezwiązane z logiką biznesową
└── plugins/         Struktura przygotowana, pusta (brak potwierdzonej osi rozszerzeń)
```

Zasady projektowe:
- `domain/tree/service.py`: składa w drzewo znaną już płaską listę plików, nigdy nie wykonuje operacji wejścia/wyjścia — rzeczywiste przechodzenie (`os.walk`) znajduje się w `infrastructure/filesystem/`.
- `domain/scans/policies.py`: zabezpieczenia crawla (głębokość/strony/domena), czysta logika testowalna bez sieci.
- `infrastructure/filesystem/` i `infrastructure/network/`: wykonują operacje wejścia/wyjścia (dysk, HTTP), nigdy nie oceniają.
- `infrastructure/exporters/`: czytają już złożony wynik skanu, nigdy nie przeliczają statystyki.
- `infrastructure/storage/sqlite/`: przechowuje tylko dane źródłowe (`scans`/`files`/`links`) — drzewo i statystyki są przeliczane przy odczycie tymi samymi czystymi funkcjami co pierwotny skan (zobacz `DECISIONS_ARCHITECTURE.md`, D-011), nigdy nie są powielane w bazie.

## 8. Eksporty

Raporty tekstowe i HTML są zapisywane w języku wybranym w Ustawieniach („Język eksportów”, domyślnie język interfejsu); JSON pozostaje danymi i nie jest tłumaczony. Raporty są domyślnie tworzone w `var/exports/` (ścieżka robocza zakotwiczona w folderze projektu, `$OMEGA_FOLD_VAR_DIR`, aby ją zmienić) albo pod wskazaną ścieżką (`--output`).

### JSON, źródło prawdy

Pełna struktura wyniku (`Scan` + drzewo + odnośniki + statystyki), ściśle serializowalna do JSON.

### Tekst, zwięzły raport do czytania

Podsumowanie, podział według rodzin, drzewo ASCII (ograniczone do 6 poziomów głębokości — raport tekstowy nie służy do wypisywania drzewa tysięcy plików), lista niedziałających odnośników.

### HTML, samodzielny raport WWW

5 motywów do wyboru (`--theme`). Łączny rozmiar strony jest eksponowany na początku (to główny cel raportu ze skanu) i wszędzie — w CLI, TUI, eksportach — podawany w czytelnej postaci (KB/MB/GB...) zamiast surowych bajtów. Własny układ: kontener, siatka statystyk, histogram SVG podziału według rodzin (rysowany ręcznie, bez ciężkiej biblioteki wykresów — ta sama technika co diagram architektury w `omega-deep`), tabele rozszerzeń/największych plików. Z linkowanych domen zewnętrznych pierwsze 20 jest widocznych od razu, reszta w zwijanym panelu (przydatne przy stronie z setkami zewnętrznych przekierowań); lista niedziałających odnośników jest domyślnie zwinięta.

Drzewo jest renderowane jako natywny **wielopoziomowy** HTML: jeden `<details>` na katalog, domyślnie otwarty tylko korzeń, każdy podfolder rozwija się niezależnie po kliknięciu (inspirowane skryptem użytkownika do generowania indeksów) — przeglądarka układa tylko otwartą treść, więc pozostaje to użyteczne nawet dla strony z dziesiątkami tysięcy plików, bez JavaScriptu.

## 9. Historia

Każdy skan jest zapisywany (SQLite, `var/db/omega-fold.db`). Historię można przeglądać według celu (`omega-fold history --target ...`), oglądać szczegóły dawnego skanu (`omega-fold show <scan_id>`) albo korzystać z menu Historia w TUI (wraz z ponownym uruchomieniem).

## 10. Zgodność z terminalami

TUI (Textual) automatycznie wykrywa możliwości terminala (emulator, rozmiar) i odpowiednio dostosowuje swój strukturalny arkusz stylów (`complete`/`standard`/`reduced`/`mono`), bez ręcznej opcji. Tryb CLI zawsze pozostaje zwykłym tekstem, niezależnie od terminala. Zasada wspólna dla całego pakietu `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil według wykrytego emulatora

| Emulator | Profil początkowy |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, nowoczesne SSH | `reduced` |
| TTY Linuksa, starsze SSH | `mono` |
| Nierozpoznany emulator | `reduced` (domyślna wartość zapasowa) |

### Profil według rozmiaru terminala

| Minimalny rozmiar (kolumny × wiersze) | Górna granica profilu |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| poniżej | `mono` |

Ostateczny profil to **bardziej restrykcyjny z dwóch** (emulator i rozmiar) — można go odświeżyć na bieżąco klawiszem `r`.

## 11. Testy

```bash
source .venv/bin/activate
lint-imports        # sprawdza Dependency Rule (6 kontraktów)
pytest -q           # 186 testów
ruff check src tests
mypy -p omega_fold
```

Struktura: `tests/unit/` (domena i infrastruktura bez prawdziwych operacji wejścia/wyjścia — eksportery, wykres SVG, znaczniki ekranu startowego TUI), `tests/integration/` (prawdziwy system plików przez `tmp_path`, pozorowany serwer HTTP `pytest-httpserver`, prawdziwa baza SQLite, CLI od początku do końca), `tests/tui/` (nawigacja przez `Pilot`, strukturalna — bez samozwańczej weryfikacji wizualnej, zobacz `docs/ARCHITECTURE.md` §Interfejs TUI).

## 12. Poza zakresem

- Analiza treści/SEO
- Renderowanie JavaScriptu po stronie klienta
- Przeszukiwanie bez zabezpieczeń
- Aktywne skanowanie podatności, fuzzing, brute force
- Panel WWW

---

> Omega-fold — Zmapować strukturę, sprawdzić jej odnośniki, nigdy nie zgadywać tego, czego nie odwiedzono.
