<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（见 LICENSE 文件） -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**站点/目录结构分析器（本地与远程）**

> 由 [kraynux](https://github.com/kraynux) 为 [Omega-Server](https://kraynux.snake-mackarel.ts.net) 打造   

官方页面：[OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; 截图：[SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-使用)

🌐 界面和导出的报告提供 **17 种语言** — 见[界面语言](#界面语言)。  
**语言：**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** 是一个 TUI + CLI 工具，用于分析本地目录或远程站点（受安全限制约束的 HTTP 爬取）的结构：完整目录树、按扩展名/文件类别的统计、链接图谱（内部/外部，各种类型）、失效链接检测。它是 `omega-` 套件中的一个工具，采用 Clean Architecture 构建 — 完整技术细节见 `docs/ARCHITECTURE.md`。

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-fold/D.png" width="24%" />
</p>

## 1. 愿景与范围

### Omega-fold 能做什么

- 扫描本地目录（真实的 `os.walk`），或以广度优先（BFS）方式爬取远程站点，并受严格的安全限制约束。
- 构建完整目录树（文件/目录、深度、大小），并按类别归类（`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`）— 见 [§4](#4-文件类别)。
- 从每个 HTML 页面/文件中提取所有链接（`<a href>`、`<img src>`、`<script src>`、`<link href>`、`<form action>`），进行分类（内部绝对/相对、外部、锚点、`mailto:`/`tel:`/`javascript:`/`data:`）并检查其是否存在 — 见 [§5](#5-链接与检查)。
- 计算统计数据：按扩展名/类别的分布、最大的文件、外链最多的文件、被链接最多的外部域名。
- 在 TUI（Textual）或可脚本化的 CLI 中呈现结果，提供三种导出（JSON、文本、带 5 种主题的 HTML）。
- 保留持久的扫描历史（SQLite），可查看、可重放。

### Omega-fold 不做什么

- 内容或 SEO 分析（标题、元描述、关键词密度）。
- 无安全限制的爬取 — 深度、页面数和请求间隔始终生效。
- 客户端 JavaScript 渲染（页面按服务器返回的原样获取，不在无头浏览器中执行）。
- 主动漏洞扫描、模糊测试、暴力破解。
- Web 仪表盘。

## 2. 安装

### 前提条件

- Python 3.10+
- 互联网连接，用于安装依赖
- 对于 TUI：终端中需安装 [Nerd Font](https://www.nerdfonts.com/) 字体，用于标题栏图标 — 没有它，该字符会显示为空方块（与表情符号的限制相同，但在终端用户中普及得多）。缺少它不会影响运行，纯属外观问题。

### 安装

```bash
[ -d omega-fold ] && echo "ℹ️ 此处已解压，跳过此步骤。" || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`：

1. 如果虚拟环境 `.venv` 尚不存在，则创建它。
2. 安装依赖（先 `vendor/omega-lib/`，再 `pip install -e .`；`pyproject.toml` 仍是唯一的权威来源）。
3. 使 `omega-fold.sh` 和 `install.sh` 可执行。
4. 将别名 `fold` 添加到 `~/.bashrc` 和 `~/.zshrc`（已存在时不会重复添加）。

### 依赖

在 `pyproject.toml` 中声明（没有 `requirements.txt`）：
- `omega-lib`：套件的共享库（导出主题、`ConfidenceLevel`）— 内置于 `vendor/omega-lib/`
- `httpx`：同步检查外部链接（`LinkChecker`）
- `aiohttp`：异步 HTTP 爬取（`DistantCrawler`）
- `beautifulsoup4` + `lxml`：提取 HTML 链接
- `jinja2`：HTML 导出的模板
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`ruff`、`mypy`、`import-linter`

## 3. 使用

### 交互模式（TUI）

推荐日常使用 — 不带参数启动：

```bash
./omega-fold.sh
```
如果已创建别名，只需在终端输入 `fold`：
```bash
fold
```

流程：启动画面（按任意键或点击关闭）→ 主菜单（扫描 / 历史 / 设置 / 帮助）→ 输入目标、类型（本地/远程）、模式（静态/动态）以及远程爬取的安全限制，每个字段都有明确的标签 → 扫描（不确定进度条、实时操作日志、随时可用的取消按钮）→ 扫描详情（按类别和扩展名的分布、目录树、失效链接、导出）→ 从主菜单进入历史（查看详情、无需经过详情即可**直接导出**、重放）和设置。对终端的适配（颜色、尺寸、结构降级）是自动的。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏（在主屏上会确认是否退出） |
| `t` | 下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需确认） |

### 界面语言

界面提供 17 种语言：法语、英语、西班牙语、葡萄牙语（巴西）、意大利语、德语、荷兰语、波兰语、俄语、简体中文、越南语、泰语、印尼语、日语、韩语、印地语和阿拉伯语。在设置中选择（“Langue / Language”），重启界面后生效；变量 `OMEGA_FOLD_LANG`（例如 `OMEGA_FOLD_LANG=zh-CN ./omega-fold.sh`）可在一次会话中强制使用某种语言。从 omega-suite 启动时，omega-fold 使用套件的语言。在 Linux 文本控制台（TTY）上，非拉丁文字的语言在本次会话中以英语显示。命令行保持法语。

### 联系与支持

帮助（`a` 键）提供 **联系与支持** 界面：*请我喝杯咖啡*（开发者的 PayPal 页面）、*联系支持*（明文显示的电子邮件地址和网站联系表单）、*登记为用户（匿名）* 和 *检查更新*。 登记是自愿的，默认关闭，且只发送一次：仅用于统计用户数量，以及（如您愿意）其所在的大洲或国家（封闭列表，绝无自由文本）。它发送一个随机生成的密钥、软件名称（`omega-fold`）及其版本；绝不发送姓名、机器名称、设置、目标或结果。IP 地址不会记录在登记中，但与任何访问一样，会经过接收服务器的安全检查和日志。 可随时在同一界面撤回（*不再登记我*）。 检查更新仅读取网站上已发布版本的列表，且从不在未点击的情况下进行。

### 脚本模式（CLI）

任何子命令都会进入 CLI 模式：

```bash
# 本地扫描（目录树 + 内部链接）
./omega-fold.sh scan /var/www/mysite --type local

# 动态模式的本地扫描（同时通过 HTTP 检查外部链接）
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# 远程扫描（从起始 URL 进行 BFS 爬取）
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# 历史（可按目标筛选）
./omega-fold.sh history --target /var/www/mysite --limit 20

# 扫描详情（文本、JSON 或 HTML）— 5 种导出主题可选
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

`scan` 的选项：

| 选项 | 默认值 | 作用 |
|---|---|---|
| `--type` | *（必填）* | `local` 或 `distant`（远程） |
| `--mode` | `static` | `static`（不检查外部链接）或 `dynamic`（通过 HTTP 检查） |
| `--max-depth` | `5` | 跟随的最大深度（远程扫描） |
| `--max-pages` | `1000` | 爬取的最大页面数（远程扫描） |
| `--delay` | `100` | 两次请求之间的间隔（毫秒）（远程扫描） |
| `--user-agent` | `omega-fold/0.1` | 发送的 `User-Agent` 请求头（远程扫描） |
| `--respect-robots` | 关闭 | 遵守 `robots.txt`（远程扫描） |

远程扫描时，不带协议的目标（`example.org`）会自动补全为 `https://example.org` — 除非要显式强制使用 `http://`，否则无需指定。

如果站点页面数超过 `--max-pages`（默认 1000），扫描会在上限处停止，但会明确报告：`scan.status` 为 `completed_truncated` 而不是 `completed`，并在 CLI 摘要、TUI 详情屏和 HTML 导出中显示醒目的警告 — 此时报告的文件数并非站点的真实规模；如需完整覆盖，请用更高的 `--max-pages` 重新运行。

如果别名由 `install.sh` 创建，`fold scan ...` 可在终端任何位置使用，无需 `./omega-fold.sh` 前缀。

## 4. 文件类别

每个文件根据其扩展名归入一个类别（首个匹配者胜出）— 完整细节和逐个扩展名的表格见 `docs/FAMILIES.md`。

| 类别 | 扩展名示例 |
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
| `other` | 其余所有 |

## 5. 链接与检查

### 分类

找到的每个链接（`href`/`src`/`action`）按以下优先顺序分类：

| 类型 | 识别条件 | 示例 |
|---|---|---|
| `empty` | 空字符串 | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | 特殊协议 | `mailto:x@y.z` |
| `anchor` | 直接以 `#` 开头（纯锚点） | `#section` |
| `external` | `http://`、`https://` 或 `//`（协议相对） | `https://example.org` |
| `absolute` | 以 `/` 开头 | `/img/logo.png` |
| `relative` | 其余所有 | `img/logo.png`、`../page.html` |

`absolute` 和 `relative` 是**内部**链接的两种形式 — 链接 `page.html#section` 仍是 `relative`（末尾的片段并不使其成为单纯的锚点，它确实会跳转到另一个资源）。

### 检查

- **内部链接**：始终对照扫描期间实际找到的路径集合进行检查（不发网络请求）— `absolute` 相对扫描根目录解析，带分隔符的 `relative` 相对源文件所在目录解析，不带分隔符的 `relative`（仅文件名）在整棵树中查找。远程扫描时，检查在爬取结束后的第二轮进行，对照实际成功访问的页面集合 — 超出安全限制或被 `robots.txt` 阻止的页面保持 `unchecked`，绝不凭猜测标为 `broken`。
- **外部链接**：仅在 `dynamic` 模式下通过 HTTP 请求检查（先 HEAD，HEAD 失败再 GET）— 在 `static` 模式下保持 `unchecked`。

## 6. 远程爬取的安全限制

始终生效，不可关闭 — 只能调整其阈值：

- **深度**（`--max-depth`）：只限制新待爬页面的入队；在已访问页面上找到的链接总会出现在结果中，即使它们指向的页面不会被跟随。
- **页面数**（`--max-pages`）：限制所有深度下访问的页面总数。
- **间隔**（`--delay`）：两次连续 HTTP 请求之间的停顿。
- **同一域名**：只跟随指向与起始 URL 相同 `netloc` 的内部链接 — 既检查链接的路径，也检查**重定向后实际加载的** URL：一个路径看似内部目录（`/go/xyz`、`/public/name/`）但实际重定向到外部域名的永久链接，绝不会被当作被扫描站点的页面（其内容并不属于你）。
- **`robots.txt`**（`--respect-robots`）：加强而不是削弱安全限制 — 被禁止的页面绝不会被访问，其外链保持 `unchecked`。

## 7. 架构

Omega-fold 采用 **Clean Architecture** 构建（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared），与 `omega-` 套件的模板保持一致（见 `omega-scan`/`omega-check`/`omega-deep`），每次修改都由 `import-linter` 验证。完整细节见 **`docs/ARCHITECTURE.md`**。

非常简短的概览：

```text
src/omega_fold/
├── domain/          纯业务逻辑：扫描、目录树（tree）、链接、统计、报告
├── application/     用例（commands/queries）— run_scan（本地/远程）、export_scan_report...
├── ports/           应用所需的契约（local_fs_reader、distant_crawler、
│                    html_link_extractor、link_checker、scan_repository、report_exporter...）
├── infrastructure/  具体实现（os.walk、aiohttp、httpx、BeautifulSoup、SQLite、
│                    Jinja2 导出器 — Textual 不在这里）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），功能严格对等
├── app/             装配（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   通用词汇、非业务工具
└── plugins/         结构已就位，为空（尚无确定的扩展方向）
```

设计规则：
- `domain/tree/service.py`：将已知的扁平文件列表聚合为目录树，从不执行 I/O — 真正的遍历（`os.walk`）位于 `infrastructure/filesystem/`。
- `domain/scans/policies.py`：爬取的安全限制（深度/页面/域名），纯逻辑，无需网络即可测试。
- `infrastructure/filesystem/` 和 `infrastructure/network/`：执行 I/O（磁盘、HTTP），从不做判断。
- `infrastructure/exporters/`：读取已组装好的扫描结果，从不重新计算统计。
- `infrastructure/storage/sqlite/`：只存储源数据（`scans`/`files`/`links`）— 目录树和统计在读取时由与首次扫描相同的纯函数重新计算（见 `DECISIONS_ARCHITECTURE.md`，D-011），从不在数据库中重复存储。

## 8. 导出

文本和 HTML 报告使用设置中选择的语言编写（“导出语言”，默认与界面相同）；JSON 作为数据保持不翻译。报告默认生成在 `var/exports/`（运行时路径锚定在项目目录，可用 `$OMEGA_FOLD_VAR_DIR` 覆盖），或生成在指定路径（`--output`）。

### JSON，权威来源

结果的完整结构（`Scan` + 目录树 + 链接 + 统计），严格可序列化为 JSON。

### 文本，紧凑的可读报告

摘要、按类别的分布、ASCII 目录树（限制为 6 层深度 — 文本报告并不用于列出包含数千个文件的树）、失效链接列表。

### HTML，独立的网页报告

5 种主题可选（`--theme`）。站点总大小最先突出显示（这是扫描报告的首要目标），并在所有地方 — CLI、TUI、导出 — 以易读格式（KB/MB/GB...）显示，而不是原始字节数。专门的布局：容器、统计网格、按类别分布的 SVG 直方图（手工绘制，无沉重的图表依赖 — 与 `omega-deep` 架构图相同的技术）、扩展名/最大文件表格。被链接的外部域名直接显示前 20 个，其余放在可折叠面板中（对于有数百个外部重定向的站点很有用）；失效链接列表默认折叠。

目录树以原生**多层级** HTML 呈现：每个目录一个 `<details>`，默认只展开根目录，每个子文件夹点击后可独立展开（灵感来自用户的一个索引生成脚本）— 浏览器只对展开的内容进行排版，因此即使站点有数万个文件也依然可用，且无需 JavaScript。

## 9. 历史

每次扫描都会保存（SQLite，`var/db/omega-fold.db`）。可按目标查看历史（`omega-fold history --target ...`）、查看过往扫描的详情（`omega-fold show <scan_id>`），或使用 TUI 的历史菜单（含重放）。

## 10. 终端兼容性

TUI（Textual）会自动检测终端的能力（模拟器、尺寸），并据此调整其结构样式表（`complete`/`standard`/`reduced`/`mono`），无需手动选项。CLI 模式始终是纯文本，与终端无关。该策略由整个 `omega-` 套件共享（`omega-lib`、`terminal/policies.py`）。

### 按检测到的模拟器确定的配置

| 模拟器 | 初始配置 |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm、urxvt、现代 SSH | `reduced` |
| Linux TTY、旧版 SSH | `mono` |
| 无法识别的模拟器 | `reduced`（默认回退） |

### 按终端尺寸确定的配置

| 最小尺寸（列 × 行） | 配置上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 更小 | `mono` |

最终配置为**两者中更严格的一个**（模拟器和尺寸）— 可用 `r` 键实时刷新。

## 11. 测试

```bash
source .venv/bin/activate
lint-imports        # 检查 Dependency Rule（6 个契约）
pytest -q           # 186 个测试
ruff check src tests
mypy -p omega_fold
```

结构：`tests/unit/`（无真实 I/O 的领域和基础设施 — 导出器、SVG 图表、TUI 启动画面的标记），`tests/integration/`（通过 `tmp_path` 使用真实文件系统、模拟 HTTP 服务器 `pytest-httpserver`、真实 SQLite 数据库、端到端 CLI），`tests/tui/`（通过 `Pilot` 导航，结构性测试 — 不自称做了视觉验证，见 `docs/ARCHITECTURE.md` §TUI 界面）。

## 12. 范围之外

- 内容/SEO 分析
- 客户端 JavaScript 渲染
- 无安全限制的爬取
- 主动漏洞扫描、模糊测试、暴力破解
- Web 仪表盘

---

> Omega-fold — 绘制结构图，检查其链接，绝不猜测未访问过的内容。
