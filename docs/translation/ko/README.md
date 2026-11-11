<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 라이선스 (LICENSE 파일 참조) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-fold.png" alt="Omega-Fold" width="512">
</div>

#  OMEGA-FOLD

**사이트/디렉터리 구조 분석기 (로컬 및 원격)**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net)를 위해 [kraynux](https://github.com/kraynux)가 개발   

공식 페이지: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; 스크린샷: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-사용법)

🌐 인터페이스와 내보낸 보고서는 **17개 언어**로 제공됩니다 — [인터페이스 언어](#인터페이스-언어) 참조.  
**언어:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold**는 로컬 디렉터리나 원격 사이트(안전 제한이 걸린 HTTP 크롤링)의 구조를 분석하는 TUI + CLI 도구입니다: 전체 트리, 확장자/파일 계열별 통계, 링크 지도(내부/외부, 모든 유형), 깨진 링크 탐지. `omega-` 제품군의 도구이며 Clean Architecture로 구성되어 있습니다 — 기술적인 세부 사항은 모두 `docs/ARCHITECTURE.md`를 참조하세요.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-fold/D.png" width="24%" />
</p>

## 1. 비전과 범위

### Omega-fold가 하는 일

- 로컬 디렉터리를 스캔(실제 `os.walk`)하거나 원격 사이트를 너비 우선(BFS)으로 크롤링하며, 엄격한 안전 제한 안에서 동작합니다.
- 전체 트리(파일/디렉터리, 깊이, 크기)를 만들고 계열별로 분류합니다(`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — [§4](#4-파일-계열) 참조.
- 각 HTML 페이지/파일에서 모든 링크(`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`)를 추출해 분류(내부 절대/상대, 외부, 앵커, `mailto:`/`tel:`/`javascript:`/`data:`)하고 존재 여부를 확인합니다 — [§5](#5-링크와-검사) 참조.
- 통계를 계산합니다: 확장자/계열별 분포, 가장 큰 파일, 나가는 링크가 가장 많은 파일, 가장 많이 링크된 외부 도메인.
- 결과를 TUI(Textual) 또는 스크립트용 CLI로 보여 주며, 세 가지 내보내기(JSON, 텍스트, 5가지 테마의 HTML)를 제공합니다.
- 스캔 기록을 영구 보관(SQLite)하며, 조회하고 다시 실행할 수 있습니다.

### Omega-fold가 하지 않는 일

- 콘텐츠나 SEO 분석(제목, 메타 설명, 키워드 밀도).
- 안전 제한 없는 크롤링 — 깊이, 페이지 수, 요청 간 지연은 항상 적용됩니다.
- 클라이언트 측 JavaScript 렌더링(페이지는 서버가 보낸 그대로 가져오며, 헤드리스 브라우저에서 실행하지 않습니다).
- 능동적 취약점 스캔, 퍼징, 무차별 대입.
- 웹 대시보드.

## 2. 설치

### 요구 사항

- Python 3.10+
- 의존성을 위한 인터넷 연결
- TUI의 경우: 헤더 아이콘을 위해 터미널에 [Nerd Font](https://www.nerdfonts.com/) 글꼴 설치 — 없으면 이 문자가 빈 사각형으로 표시됩니다(이모지와 같은 제약이지만 터미널 사용자 사이에서는 훨씬 널리 쓰입니다). 없어도 동작에는 영향이 없으며 순전히 외관 문제입니다.

### 설치

```bash
[ -d omega-fold ] && echo "ℹ️ 이미 여기에 압축이 풀려 있어 이 단계를 건너뜁니다." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. 가상 환경 `.venv`가 아직 없으면 만듭니다.
2. 의존성을 설치합니다(`vendor/omega-lib/` 다음 `pip install -e .`; `pyproject.toml`이 유일한 기준 정보로 남습니다).
3. `omega-fold.sh`와 `install.sh`를 실행 가능하게 만듭니다.
4. 별칭 `fold`를 `~/.bashrc`와 `~/.zshrc`에 추가합니다(이미 있으면 중복하지 않습니다).

### 의존성

`pyproject.toml`에 선언(`requirements.txt` 없음):
- `omega-lib`: 제품군 공용 라이브러리(내보내기 테마, `ConfidenceLevel`) — `vendor/omega-lib/`에 포함
- `httpx`: 외부 링크의 동기 검사(`LinkChecker`)
- `aiohttp`: 비동기 HTTP 크롤링(`DistantCrawler`)
- `beautifulsoup4` + `lxml`: HTML 링크 추출
- `jinja2`: HTML 내보내기용 템플릿
- 개발 의존성(`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. 사용법

### 대화형 모드 (TUI)

일상적인 사용에 권장 — 인수 없이 실행합니다:

```bash
./omega-fold.sh
```
별칭을 만들었다면 터미널에 `fold`만 입력하면 됩니다:
```bash
fold
```

흐름: 시작 화면(키를 누르거나 클릭하면 닫힘) → 메인 메뉴(스캔 / 기록 / 설정 / 도움말) → 대상, 유형(로컬/원격), 모드(정적/동적), 원격 크롤링 안전 제한 입력(각 필드에 명확한 레이블) → 스캔(불확정 진행 표시, 실시간 작업 로그, 언제든 누를 수 있는 취소 버튼) → 스캔 상세(계열별·확장자별 분포, 트리, 깨진 링크, 내보내기) → 메인 메뉴에서 기록(상세 보기, 상세를 거치지 않고 **바로 내보내기**, 다시 실행)과 설정. 터미널에 대한 적응(색상, 크기, 구조 단순화)은 자동입니다.

#### 단축키

| 키 | 동작 |
|---|---|
| `↑` / `↓` | 화면의 항목 사이 이동 |
| `Tab` / `Shift+Tab` | 양식의 필드 사이 이동 |
| `Esc` | 이전 화면으로 돌아가기(홈 화면에서는 종료 확인) |
| `t` | 다음 테마(확인 없이 즉시 적용) |
| `r` | 터미널 감지 새로 고침 |
| `a` | 도움말 표시 |
| `q` | 종료(확인 후) |

### 인터페이스 언어

인터페이스는 17개 언어로 제공됩니다: 프랑스어, 영어, 스페인어, 포르투갈어(브라질), 이탈리아어, 독일어, 네덜란드어, 폴란드어, 러시아어, 중국어 간체, 베트남어, 태국어, 인도네시아어, 일본어, 한국어, 힌디어, 아랍어. 설정(“Langue / Language”)에서 선택하며 인터페이스를 다시 시작한 뒤 적용됩니다. 변수 `OMEGA_FOLD_LANG`(예: `OMEGA_FOLD_LANG=ko ./omega-fold.sh`)으로 한 세션 동안 언어를 강제할 수 있습니다. omega-suite에서 실행하면 omega-fold는 제품군의 언어를 사용합니다. Linux 텍스트 콘솔(TTY)에서는 라틴 문자가 아닌 언어가 해당 세션 동안 영어로 표시됩니다. 명령줄은 프랑스어로 유지됩니다.

### 문의 및 지원

도움말(`a` 키)에는 **문의 및 지원** 화면이 있습니다: *커피 한 잔 사기*(개발자의 PayPal 페이지), *지원팀에 문의*(이메일 주소와 사이트의 문의 양식을 그대로 표시), *사용자로 등록(익명)*, *업데이트 확인*. 등록은 자발적이며 기본적으로 꺼져 있고 한 번만 전송됩니다. 사용자 수와, 원하면 사용자의 대륙 또는 국가(닫힌 목록, 자유 입력 없음)를 세는 데에만 쓰입니다. 무작위로 생성한 키, 소프트웨어 이름(`omega-fold`)과 버전만 보내며, 이름, 컴퓨터 이름, 설정, 대상, 결과는 절대 보내지 않습니다. IP 주소는 등록 정보에 저장되지 않지만, 모든 방문과 마찬가지로 수신 서버의 보안 검사와 로그를 거칩니다. 같은 화면에서 언제든지 철회할 수 있습니다(*등록 취소*). 업데이트 확인은 사이트에 게시된 버전 목록만 읽으며, 클릭하지 않으면 절대 실행되지 않습니다.

### 스크립트 모드 (CLI)

하위 명령을 지정하면 CLI 모드가 됩니다:

```bash
# 로컬 스캔(트리 + 내부 링크)
./omega-fold.sh scan /var/www/mysite --type local

# 동적 모드 로컬 스캔(외부 링크도 HTTP로 검사)
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# 원격 스캔(시작 URL부터 BFS 크롤링)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# 기록(대상별 필터 가능)
./omega-fold.sh history --target /var/www/mysite --limit 20

# 스캔 상세(텍스트, JSON 또는 HTML) — 내보내기 테마 5가지 중 선택
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

`scan` 옵션:

| 옵션 | 기본값 | 효과 |
|---|---|---|
| `--type` | *(필수)* | `local` 또는 `distant`(원격) |
| `--mode` | `static` | `static`(외부 링크 검사 안 함) 또는 `dynamic`(HTTP로 검사) |
| `--max-depth` | `5` | 따라가는 최대 깊이(원격 스캔) |
| `--max-pages` | `1000` | 크롤링할 최대 페이지 수(원격 스캔) |
| `--delay` | `100` | 두 요청 사이의 지연(ms)(원격 스캔) |
| `--user-agent` | `omega-fold/0.1` | 보내는 `User-Agent` 헤더(원격 스캔) |
| `--respect-robots` | 꺼짐 | `robots.txt` 준수(원격 스캔) |

원격 스캔에서 스킴이 없는 대상(`example.org`)은 자동으로 `https://example.org`로 보완됩니다 — `http://`를 명시적으로 강제하려는 경우가 아니면 지정할 필요가 없습니다.

사이트의 페이지가 `--max-pages`(기본 1000)보다 많으면 스캔은 한도에서 멈추지만 그 사실을 명시적으로 알립니다: `scan.status`가 `completed` 대신 `completed_truncated`가 되고, CLI 요약, TUI 상세 화면, HTML 내보내기에 눈에 띄는 경고가 표시됩니다 — 이때 보고된 파일 수는 사이트의 실제 규모가 아닙니다. 전체를 다루려면 더 큰 `--max-pages`로 다시 실행하세요.

별칭을 `install.sh`가 만들었다면 `fold scan ...`은 `./omega-fold.sh` 접두사 없이 터미널 어디에서나 동작합니다.

## 4. 파일 계열

각 파일은 확장자에 따라 계열로 분류됩니다(처음 일치하는 항목 우선) — 전체 세부 사항과 확장자별 표: `docs/FAMILIES.md`.

| 계열 | 확장자 예시 |
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
| `other` | 그 밖의 모든 것 |

## 5. 링크와 검사

### 분류

찾은 각 링크(`href`/`src`/`action`)는 다음 우선순위로 분류됩니다:

| 유형 | 인식 조건 | 예 |
|---|---|---|
| `empty` | 빈 문자열 | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | 특수 스킴 | `mailto:x@y.z` |
| `anchor` | `#`로 바로 시작(순수 앵커) | `#section` |
| `external` | `http://`, `https://` 또는 `//`(프로토콜 상대) | `https://example.org` |
| `absolute` | `/`로 시작 | `/img/logo.png` |
| `relative` | 그 밖의 모든 것 | `img/logo.png`, `../page.html` |

`absolute`와 `relative`는 **내부** 링크의 두 형태입니다 — `page.html#section` 링크는 `relative`로 남습니다(끝의 프래그먼트가 있다고 단순한 앵커가 되지 않으며, 실제로 다른 리소스로 이동합니다).

### 검사

- **내부 링크**: 항상 스캔 중 실제로 찾은 경로 집합과 대조합니다(네트워크 요청 없음) — `absolute`는 스캔 루트 기준으로, 구분자가 있는 `relative`는 원본 파일의 디렉터리 기준으로 해석하고, 구분자가 없는 `relative`(파일 이름만)는 트리 전체에서 찾습니다. 원격 스캔에서는 크롤링이 끝난 뒤 두 번째 단계에서 실제로 방문에 성공한 페이지 집합과 대조합니다 — 안전 제한 밖이거나 `robots.txt`로 막힌 페이지는 `unchecked`로 남으며, 추측으로 `broken`이 되지 않습니다.
- **외부 링크**: `dynamic` 모드에서만 HTTP 요청(HEAD, 실패하면 GET)으로 검사합니다 — `static` 모드에서는 `unchecked`로 남습니다.

## 6. 원격 크롤링 안전 제한

항상 켜져 있고 끌 수 없습니다 — 임곗값만 조정할 수 있습니다:

- **깊이**(`--max-depth`): 새로 크롤링할 페이지를 대기열에 넣는 것만 제한합니다. 이미 방문한 페이지에서 찾은 링크는 그 대상 페이지를 따라가지 않더라도 항상 결과에 포함됩니다.
- **페이지 수**(`--max-pages`): 모든 깊이에 걸쳐 방문하는 페이지의 총수를 제한합니다.
- **지연**(`--delay`): 연속된 두 HTTP 요청 사이의 휴지.
- **같은 도메인**: 시작 URL과 같은 `netloc`을 가리키는 내부 링크만 따라갑니다 — 링크의 경로와 **리디렉션 후 실제로 불러온** URL 모두에서 확인합니다: 경로가 내부 폴더처럼 보이지만(`/go/xyz`, `/public/name/`) 실제로는 외부 도메인으로 리디렉션되는 고유 링크는 스캔 대상 사이트의 페이지로 취급되지 않습니다(그 내용은 당신의 것이 아니므로).
- **`robots.txt`**(`--respect-robots`): 안전 제한을 약하게 하는 것이 아니라 강화합니다 — 금지된 페이지는 방문하지 않으며, 그 페이지의 나가는 링크는 `unchecked`로 남습니다.

## 7. 아키텍처

Omega-fold는 **Clean Architecture**(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)로 구성되어 있으며, `omega-` 제품군의 템플릿(`omega-scan`/`omega-check`/`omega-deep` 참조)에 맞추고 변경할 때마다 `import-linter`로 검증합니다. 전체 세부 사항은 **`docs/ARCHITECTURE.md`**에 있습니다.

아주 짧은 개요:

```text
src/omega_fold/
├── domain/          순수 업무 로직: 스캔, 트리(tree), 링크, 통계, 보고서
├── application/     사용 사례(commands/queries) — run_scan(로컬/원격), export_scan_report...
├── ports/           애플리케이션이 기대하는 계약(local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  구체 구현(os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2 내보내기 도구 — Textual은 여기에 없음)
├── interfaces/      tui/(Textual)와 cli/(스크립트용), 기능이 엄격히 동일
├── app/             조립(DependencyContainer, bootstrap, 수명 주기)
├── core/, shared/   공통 어휘, 업무 외 유틸리티
└── plugins/         구조만 마련됨, 비어 있음(확정된 확장 방향 없음)
```

설계 규칙:
- `domain/tree/service.py`: 이미 알고 있는 평면 파일 목록을 트리로 묶으며 I/O는 전혀 하지 않습니다 — 실제 순회(`os.walk`)는 `infrastructure/filesystem/`에 있습니다.
- `domain/scans/policies.py`: 크롤링 안전 제한(깊이/페이지/도메인), 네트워크 없이 테스트할 수 있는 순수 로직.
- `infrastructure/filesystem/`와 `infrastructure/network/`: I/O(디스크, HTTP)를 수행하며 판단하지 않습니다.
- `infrastructure/exporters/`: 이미 조립된 스캔 결과를 읽기만 하며 통계를 다시 계산하지 않습니다.
- `infrastructure/storage/sqlite/`: 원본 데이터(`scans`/`files`/`links`)만 저장합니다 — 트리와 통계는 읽을 때 첫 스캔과 같은 순수 함수로 다시 계산되며(`DECISIONS_ARCHITECTURE.md`, D-011 참조), 데이터베이스에 중복 저장되지 않습니다.

## 8. 내보내기

텍스트와 HTML 보고서는 설정에서 고른 언어로 작성됩니다(“내보내기 언어”, 기본값은 인터페이스와 같음). JSON은 데이터로 남으며 번역되지 않습니다. 보고서는 기본적으로 `var/exports/`에 생성되며(실행 경로는 프로젝트 폴더에 고정, `$OMEGA_FOLD_VAR_DIR`로 변경 가능), 지정한 경로(`--output`)에 생성할 수도 있습니다.

### JSON, 기준 정보

결과의 전체 구조(`Scan` + 트리 + 링크 + 통계), 엄격하게 JSON 직렬화 가능.

### 텍스트, 간결하고 읽기 쉬운 보고서

요약, 계열별 분포, ASCII 트리(깊이 6단계로 제한 — 텍스트 보고서는 수천 개 파일의 트리를 나열하기 위한 것이 아님), 깨진 링크 목록.

### HTML, 독립형 웹 보고서

테마 5가지 중 선택(`--theme`). 사이트의 전체 크기를 가장 먼저 강조하며(스캔 보고서의 첫째 목적), CLI, TUI, 내보내기 어디서나 원시 바이트가 아닌 읽기 쉬운 형식(KB/MB/GB...)으로 표시합니다. 전용 레이아웃: 컨테이너, 통계 격자, 계열별 분포의 SVG 히스토그램(직접 그림, 무거운 차트 의존성 없음 — `omega-deep`의 아키텍처 다이어그램과 같은 기법), 확장자/가장 큰 파일 표. 링크된 외부 도메인은 상위 20개를 바로 보여 주고 나머지는 접을 수 있는 패널에 넣습니다(외부 리디렉션이 수백 개인 사이트에서 유용). 깨진 링크 목록은 기본적으로 접혀 있습니다.

트리는 네이티브 **다단계** HTML로 표시됩니다: 디렉터리마다 `<details>` 하나, 기본적으로 루트만 열려 있고 각 하위 폴더는 클릭하면 개별적으로 펼쳐집니다(사용자의 인덱스 생성 스크립트에서 착안) — 브라우저는 열린 내용만 배치하므로 파일이 수만 개인 사이트에서도 JavaScript 없이 쓸 만합니다.

## 9. 기록

각 스캔은 저장됩니다(SQLite, `var/db/omega-fold.db`). 대상별 기록(`omega-fold history --target ...`), 지난 스캔의 상세(`omega-fold show <scan_id>`), 또는 TUI의 기록 메뉴(다시 실행 포함)에서 확인할 수 있습니다.

## 10. 터미널 호환성

TUI(Textual)는 터미널의 능력(에뮬레이터, 크기)을 자동으로 감지하고 그에 맞게 구조 스타일시트(`complete`/`standard`/`reduced`/`mono`)를 조정합니다. 수동 옵션은 필요 없습니다. CLI 모드는 항상 일반 텍스트이며 터미널과 무관합니다. 이 정책은 `omega-` 제품군 전체가 공유합니다(`omega-lib`, `terminal/policies.py`).

### 감지된 에뮬레이터에 따른 프로필

| 에뮬레이터 | 초기 프로필 |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, 최신 SSH | `reduced` |
| Linux TTY, 구형 SSH | `mono` |
| 인식할 수 없는 에뮬레이터 | `reduced`(기본 대체값) |

### 터미널 크기에 따른 프로필

| 최소 크기(열 × 행) | 프로필 상한 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 그보다 작음 | `mono` |

최종 프로필은 **둘 중 더 엄격한 쪽**(에뮬레이터와 크기)입니다 — `r` 키로 바로 새로 고칠 수 있습니다.

## 11. 테스트

```bash
source .venv/bin/activate
lint-imports        # Dependency Rule 검사(계약 6개)
pytest -q           # 테스트 186개
ruff check src tests
mypy -p omega_fold
```

구조: `tests/unit/`(실제 I/O 없는 도메인과 인프라 — 내보내기 도구, SVG 그래프, TUI 시작 화면 마크업), `tests/integration/`(`tmp_path`를 통한 실제 파일 시스템, 가짜 HTTP 서버 `pytest-httpserver`, 실제 SQLite 데이터베이스, 처음부터 끝까지의 CLI), `tests/tui/`(`Pilot`을 통한 탐색, 구조적 — 시각 검증을 했다고 주장하지 않음, `docs/ARCHITECTURE.md` §TUI 인터페이스 참조).

## 12. 범위 밖

- 콘텐츠/SEO 분석
- 클라이언트 측 JavaScript 렌더링
- 안전 제한 없는 크롤링
- 능동적 취약점 스캔, 퍼징, 무차별 대입
- 웹 대시보드

---

> Omega-fold — 구조를 지도로 그리고, 링크를 확인하고, 방문하지 않은 것은 결코 추측하지 않는다.
