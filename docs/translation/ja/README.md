<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT ライセンス（LICENSE ファイルを参照） -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**サイト／ディレクトリ構造アナライザー（ローカルとリモート）**

> **Omega-server** のために **kraynux** が開発 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

公式ページ：[OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; スクリーンショット：[SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-使い方)

🌐 インターフェースとエクスポートされるレポートは **17 言語** に対応 — [インターフェースの言語](#インターフェースの言語)を参照。  
**言語：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** は、ローカルディレクトリまたはリモートサイト（安全上の制限付き HTTP クロール）の構造を解析する TUI + CLI ツールです：完全なツリー、拡張子／ファイル分類ごとの統計、リンクマップ（内部／外部、全種類）、リンク切れの検出。`omega-` スイートのツールで、Clean Architecture で構成されています — 技術的な詳細はすべて `docs/ARCHITECTURE.md` を参照してください。

## 1. ビジョンと範囲

### Omega-fold ができること

- ローカルディレクトリをスキャン（実際の `os.walk`）するか、リモートサイトを幅優先（BFS）でクロールします。いずれも厳格な安全上の制限内で行います。
- 完全なツリー（ファイル／ディレクトリ、深さ、サイズ）を構築し、分類ごとに整理します（`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`）— [§4](#4-ファイルの分類) を参照。
- 各 HTML ページ／ファイルからすべてのリンク（`<a href>`、`<img src>`、`<script src>`、`<link href>`、`<form action>`）を抽出し、分類（内部の絶対／相対、外部、アンカー、`mailto:`/`tel:`/`javascript:`/`data:`）して存在を確認します — [§5](#5-リンクとチェック) を参照。
- 統計を算出します：拡張子／分類ごとの内訳、最大のファイル、外部へのリンクが最も多いファイル、最も多くリンクされている外部ドメイン。
- 結果を TUI（Textual）またはスクリプト可能な CLI で表示し、3 種類のエクスポート（JSON、テキスト、5 テーマの HTML）を備えます。
- スキャン履歴を永続的に保存（SQLite）し、閲覧や再実行ができます。

### Omega-fold がしないこと

- コンテンツや SEO の分析（タイトル、メタディスクリプション、キーワード密度）。
- 安全上の制限なしのクロール — 深さ、ページ数、リクエスト間の待機時間は常に有効です。
- クライアント側の JavaScript レンダリング（ページはサーバーが返したとおりに取得し、ヘッドレスブラウザーでは実行しません）。
- 能動的な脆弱性スキャン、ファジング、総当たり攻撃。
- Web ダッシュボード。

## 2. インストール

### 前提条件

- Python 3.10+
- 依存関係のためのインターネット接続
- TUI の場合：ヘッダーのアイコン用に、端末に [Nerd Font](https://www.nerdfonts.com/) がインストールされていること — ない場合、その文字は空の四角で表示されます（絵文字と同じ制約ですが、端末ユーザーの間でははるかに普及しています）。なくても動作には影響せず、見た目だけの問題です。

### インストール

```bash
[ -d omega-fold ] && echo "ℹ️ ここに展開済みのため、この手順をスキップします。" || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`：

1. 仮想環境 `.venv` がまだなければ作成します。
2. 依存関係をインストールします（`vendor/omega-lib/`、続いて `pip install -e .`。`pyproject.toml` が唯一の正となる情報源です）。
3. `omega-fold.sh` と `install.sh` を実行可能にします。
4. エイリアス `fold` を `~/.bashrc` と `~/.zshrc` に追加します（既にあれば重複させません）。

### 依存関係

`pyproject.toml` で宣言（`requirements.txt` はありません）：
- `omega-lib`：スイート共通ライブラリ（エクスポートのテーマ、`ConfidenceLevel`）— `vendor/omega-lib/` に同梱
- `httpx`：外部リンクの同期チェック（`LinkChecker`）
- `aiohttp`：非同期 HTTP クロール（`DistantCrawler`）
- `beautifulsoup4` + `lxml`：HTML リンクの抽出
- `jinja2`：HTML エクスポートのテンプレート
- 開発用の依存関係（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`ruff`、`mypy`、`import-linter`

## 3. 使い方

### 対話モード（TUI）

日常の利用におすすめ — 引数なしで起動します：

```bash
./omega-fold.sh
```
エイリアスを作成した場合は、端末で `fold` と入力するだけです：
```bash
fold
```

流れ：スプラッシュ画面（キーまたはクリックで閉じる）→ メインメニュー（スキャン / 履歴 / 設定 / ヘルプ）→ 対象、種類（ローカル／リモート）、モード（静的／動的）、リモートクロールの安全上の制限を入力（各欄に明確なラベル付き）→ スキャン（不確定の進捗表示、操作のリアルタイムログ、いつでも使えるキャンセルボタン）→ スキャンの詳細（分類別・拡張子別の内訳、ツリー、リンク切れ、エクスポート）→ メインメニューから履歴（詳細の表示、詳細を経由せず**直接エクスポート**、再実行）と設定。端末への適応（色、サイズ、構造の簡略化）は自動です。

#### キーボードショートカット

| キー | 操作 |
|---|---|
| `↑` / `↓` | 画面の項目間を移動 |
| `Tab` / `Shift+Tab` | フォームの入力欄間を移動 |
| `Esc` | 前の画面に戻る（ホーム画面では終了を確認） |
| `t` | 次のテーマ（確認なしですぐに適用） |
| `r` | 端末の検出を更新 |
| `a` | ヘルプを表示 |
| `q` | 終了（確認あり） |

### インターフェースの言語

インターフェースは 17 言語に対応しています：フランス語、英語、スペイン語、ポルトガル語（ブラジル）、イタリア語、ドイツ語、オランダ語、ポーランド語、ロシア語、簡体字中国語、ベトナム語、タイ語、インドネシア語、日本語、韓国語、ヒンディー語、アラビア語。設定（「Langue / Language」）で選択し、インターフェースの再起動後に反映されます。変数 `OMEGA_FOLD_LANG`（例：`OMEGA_FOLD_LANG=ja ./omega-fold.sh`）で、1 セッションの間だけ言語を固定できます。omega-suite から起動した場合、omega-fold はスイートの言語を使います。Linux のテキストコンソール（TTY）では、ラテン文字以外の言語はそのセッション中は英語で表示されます。コマンドラインはフランス語のままです。

### スクリプトモード（CLI）

サブコマンドを指定すると CLI モードになります：

```bash
# ローカルスキャン（ツリー + 内部リンク）
./omega-fold.sh scan /var/www/mysite --type local

# 動的モードのローカルスキャン（外部リンクも HTTP でチェック）
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# リモートスキャン（開始 URL からの BFS クロール）
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# 履歴（対象で絞り込み可能）
./omega-fold.sh history --target /var/www/mysite --limit 20

# スキャンの詳細（テキスト、JSON、HTML）— エクスポートのテーマは 5 種類から選択
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

`scan` のオプション：

| オプション | 既定値 | 効果 |
|---|---|---|
| `--type` | *（必須）* | `local` または `distant`（リモート） |
| `--mode` | `static` | `static`（外部リンクはチェックしない）または `dynamic`（HTTP でチェック） |
| `--max-depth` | `5` | たどる最大の深さ（リモートスキャン） |
| `--max-pages` | `1000` | クロールする最大ページ数（リモートスキャン） |
| `--delay` | `100` | 2 つのリクエスト間の待機時間（ミリ秒）（リモートスキャン） |
| `--user-agent` | `omega-fold/0.1` | 送信する `User-Agent` ヘッダー（リモートスキャン） |
| `--respect-robots` | 無効 | `robots.txt` に従う（リモートスキャン） |

リモートスキャンでは、スキームのない対象（`example.org`）は自動的に `https://example.org` に補完されます — `http://` を明示的に強制したい場合を除き、指定は不要です。

サイトのページ数が `--max-pages`（既定 1000）を超える場合、スキャンは上限で止まりますが、そのことを明示的に報告します：`scan.status` は `completed` ではなく `completed_truncated` になり、CLI の要約、TUI の詳細画面、HTML エクスポートに目立つ警告が表示されます — このとき報告されるファイル数はサイトの実際の規模ではありません。完全に網羅するには、より大きな `--max-pages` で再実行してください。

エイリアスが `install.sh` によって作成されていれば、`fold scan ...` は `./omega-fold.sh` の接頭辞なしで端末のどこからでも使えます。

## 4. ファイルの分類

各ファイルは拡張子に応じて分類されます（最初に一致したものが優先）— 完全な詳細と拡張子ごとの表：`docs/FAMILIES.md`。

| 分類 | 拡張子の例 |
|---|---|
| `images` | `.jpg`、`.png`、`.svg`、`.webp`、`.ico`... |
| `documents` | `.pdf`、`.doc`、`.xlsx`、`.odt`... |
| `code` | `.html`、`.php`、`.js`、`.ts`、`.py`、`.css`... |
| `data` | `.json`、`.xml`、`.yaml`、`.csv`、`.sql`... |
| `archives` | `.zip`、`.tar`、`.gz`、`.7z`... |
| `fonts` | `.ttf`、`.otf`、`.woff`、`.woff2`... |
| `video` | `.mp4`、`.webm`、`.mkv`... |
| `audio` | `.mp3`、`.wav`、`.flac`... |
| `text` | `.txt`、`.md`、`.rst`、`.log` |
| `other` | それ以外すべて |

## 5. リンクとチェック

### 分類

見つかった各リンク（`href`/`src`/`action`）は、次の優先順位で分類されます：

| 種類 | 判定条件 | 例 |
|---|---|---|
| `empty` | 空文字列 | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | 特殊なスキーム | `mailto:x@y.z` |
| `anchor` | `#` で直接始まる（純粋なアンカー） | `#section` |
| `external` | `http://`、`https://`、または `//`（プロトコル相対） | `https://example.org` |
| `absolute` | `/` で始まる | `/img/logo.png` |
| `relative` | それ以外すべて | `img/logo.png`、`../page.html` |

`absolute` と `relative` は**内部**リンクの 2 つの形です — `page.html#section` というリンクは `relative` のままです（末尾のフラグメントがあっても単なるアンカーにはならず、実際に別のリソースへ移動します）。

### チェック

- **内部リンク**：常に、スキャン中に実際に見つかったパスの集合と照合します（ネットワークリクエストなし）— `absolute` はスキャンのルートから、区切り文字を含む `relative` は元ファイルのディレクトリから解決し、区切り文字のない `relative`（ファイル名のみ）はツリー全体から探します。リモートスキャンでは、クロール終了後の 2 回目のパスで、実際に正常に訪問できたページの集合と照合します — 安全上の制限の外にあるページや `robots.txt` でブロックされたページは `unchecked` のままで、推測で `broken` にされることはありません。
- **外部リンク**：`dynamic` モードでのみ HTTP リクエスト（HEAD、失敗した場合は GET）でチェックします — `static` モードでは `unchecked` のままです。

## 6. リモートクロールの安全上の制限

常に有効で、無効にはできません — 調整できるのはしきい値だけです：

- **深さ**（`--max-depth`）：新しくクロールするページのキュー投入だけを制限します。既に訪問したページで見つかったリンクは、リンク先のページをたどらない場合でも必ず結果に含まれます。
- **ページ数**（`--max-pages`）：すべての深さを通じて訪問するページの総数を制限します。
- **待機時間**（`--delay`）：連続する 2 つの HTTP リクエスト間の休止。
- **同一ドメイン**：開始 URL と同じ `netloc` への内部リンクだけをたどります — リンクのパスと、**リダイレクト後に実際に読み込まれた** URL の両方で確認します：パスが内部フォルダーのように見える（`/go/xyz`、`/public/name/`）が実際には外部ドメインへリダイレクトするパーマリンクは、スキャン対象サイトのページとして扱われることはありません（その内容はあなたのものではないため）。
- **`robots.txt`**（`--respect-robots`）：安全上の制限を弱めるのではなく強化します — 禁止されたページは訪問せず、その外部へのリンクは `unchecked` のままです。

## 7. アーキテクチャ

Omega-fold は **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared）で構成され、`omega-` スイートのテンプレート（`omega-scan`/`omega-check`/`omega-deep` を参照）に揃えてあり、変更のたびに `import-linter` で検証されます。完全な詳細は **`docs/ARCHITECTURE.md`** にあります。

ごく短い概要：

```text
src/omega_fold/
├── domain/          純粋な業務ロジック：スキャン、ツリー（tree）、リンク、統計、レポート
├── application/     ユースケース（commands/queries）— run_scan（ローカル／リモート）、export_scan_report...
├── ports/           アプリケーションが期待する契約（local_fs_reader、distant_crawler、
│                    html_link_extractor、link_checker、scan_repository、report_exporter...）
├── infrastructure/  具体的な実装（os.walk、aiohttp、httpx、BeautifulSoup、SQLite、
│                    Jinja2 エクスポーター — Textual はここにはありません）
├── interfaces/      tui/（Textual）と cli/（スクリプト可能）、機能は厳密に同等
├── app/             組み立て（DependencyContainer、bootstrap、ライフサイクル）
├── core/, shared/   横断的な語彙、業務外のユーティリティ
└── plugins/         構造のみ用意、空（確定した拡張の方向性なし）
```

設計ルール：
- `domain/tree/service.py`：既知のファイルのフラットな一覧をツリーにまとめ、I/O は一切行いません — 実際の走査（`os.walk`）は `infrastructure/filesystem/` にあります。
- `domain/scans/policies.py`：クロールの安全上の制限（深さ／ページ／ドメイン）、ネットワークなしでテストできる純粋なロジック。
- `infrastructure/filesystem/` と `infrastructure/network/`：I/O（ディスク、HTTP）を行い、判断はしません。
- `infrastructure/exporters/`：組み立て済みのスキャン結果を読むだけで、統計を再計算することはありません。
- `infrastructure/storage/sqlite/`：元データ（`scans`/`files`/`links`）だけを保存します — ツリーと統計は、読み込み時に最初のスキャンと同じ純粋関数で再計算され（`DECISIONS_ARCHITECTURE.md`、D-011 を参照）、データベースに重複して保存されることはありません。

## 8. エクスポート

テキストと HTML のレポートは、設定で選んだ言語で書かれます（「エクスポートの言語」、既定はインターフェースと同じ）。JSON はデータのままで翻訳されません。レポートは既定で `var/exports/` に生成されます（実行時のパスはプロジェクトフォルダーに固定、`$OMEGA_FOLD_VAR_DIR` で変更可能）。または指定したパス（`--output`）に生成されます。

### JSON、正となる情報源

結果の完全な構造（`Scan` + ツリー + リンク + 統計）、厳密に JSON シリアライズ可能。

### テキスト、コンパクトで読みやすいレポート

要約、分類別の内訳、ASCII ツリー（深さ 6 階層まで — テキストレポートは数千ファイルのツリーを一覧にするためのものではありません）、リンク切れの一覧。

### HTML、単体で完結する Web レポート

5 種類のテーマから選択（`--theme`）。サイトの合計サイズを最初に強調し（スキャンレポートの第一の目的）、CLI、TUI、エクスポートのどこでも生のバイト数ではなく読みやすい形式（KB/MB/GB...）で表示します。専用のレイアウト：コンテナー、統計グリッド、分類別内訳の SVG ヒストグラム（手描きで、重いグラフライブラリに依存しない — `omega-deep` のアーキテクチャ図と同じ技法）、拡張子／最大ファイルの表。リンクされている外部ドメインは上位 20 件をそのまま表示し、残りは折りたたみパネルに入ります（外部リダイレクトが数百あるサイトで便利）。リンク切れの一覧は既定で折りたたまれています。

ツリーはネイティブの**多階層** HTML で描画されます：ディレクトリごとに 1 つの `<details>`、既定ではルートだけが開いており、各サブフォルダーはクリックで個別に展開します（ユーザーの索引生成スクリプトに着想）— ブラウザーは開いている内容しかレイアウトしないため、数万ファイルのサイトでも JavaScript なしで快適に使えます。

## 9. 履歴

各スキャンは保存されます（SQLite、`var/db/omega-fold.db`）。対象ごとの履歴（`omega-fold history --target ...`）、過去のスキャンの詳細（`omega-fold show <scan_id>`）、または TUI の履歴メニュー（再実行を含む）から確認できます。

## 10. 端末との互換性

TUI（Textual）は端末の能力（エミュレーター、サイズ）を自動的に検出し、それに合わせて構造スタイルシート（`complete`/`standard`/`reduced`/`mono`）を調整します。手動の指定は不要です。CLI モードは常にプレーンテキストで、端末に依存しません。この方針は `omega-` スイート全体で共通です（`omega-lib`、`terminal/policies.py`）。

### 検出したエミュレーターによるプロファイル

| エミュレーター | 初期プロファイル |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm、urxvt、最近の SSH | `reduced` |
| Linux TTY、古い SSH | `mono` |
| 認識できないエミュレーター | `reduced`（既定の代替） |

### 端末サイズによるプロファイル

| 最小サイズ（列 × 行） | プロファイルの上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| それ未満 | `mono` |

最終的なプロファイルは**両者のうち制限の厳しい方**（エミュレーターとサイズ）です — `r` キーでその場で更新できます。

## 11. テスト

```bash
source .venv/bin/activate
lint-imports        # Dependency Rule をチェック（6 つの契約）
pytest -q           # 186 件のテスト
ruff check src tests
mypy -p omega_fold
```

構成：`tests/unit/`（実際の I/O を伴わないドメインとインフラ — エクスポーター、SVG グラフ、TUI スプラッシュのマークアップ）、`tests/integration/`（`tmp_path` による実際のファイルシステム、模擬 HTTP サーバー `pytest-httpserver`、実際の SQLite データベース、エンドツーエンドの CLI）、`tests/tui/`（`Pilot` によるナビゲーション、構造的 — 視覚的な検証をしたとは主張しない、`docs/ARCHITECTURE.md` §TUI インターフェースを参照）。

## 12. 範囲外

- コンテンツ／SEO の分析
- クライアント側の JavaScript レンダリング
- 安全上の制限なしのクロール
- 能動的な脆弱性スキャン、ファジング、総当たり攻撃
- Web ダッシュボード

---

> Omega-fold — 構造を地図にし、そのリンクを確かめ、訪れていないものを決して推測しない。
