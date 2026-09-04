<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT 许可证（参见 LICENSE 文件） -->
<div align="center">
  <img src="docs/assets/omega-fold.png" alt="Omega-Fold" width="256">
</div>

#  OMEGA-FOLD

**网站/目录结构分析器（本地和远程）**

> 由 **kraynux** 为 **Omega-server** 开发  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

官方页面：[OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; 预览：[SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-使用方法)

**语言：**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-fold** 是一款 TUI + CLI 工具，用于分析本地目录或远程网站的结构（具备安全限制的 HTTP 爬取）：完整树形结构、按扩展名/文件类别统计、链接映射（内部/外部，包含所有类型）以及失效链接检测。它是 `omega-` 套件中的第五个工具（继 `omega-scan`、`omega-stress`、`omega-check` 和 `omega-deep` 之后），采用 Clean Architecture 架构。完整技术细节请参阅 `docs/ARCHITECTURE.md`。

## 1. 愿景与范围

### Omega-fold 的功能

- 扫描本地目录（真实的 `os.walk`），或使用 BFS 爬取远程网站，并受到严格安全限制的约束。
- 构建完整树形结构（文件/目录、深度、大小），并按类别分类（`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`）。请参阅 [§4](#4-文件类别)。
- 从每个 HTML 页面/文件中提取所有链接（`<a href>`、`<img src>`、`<script src>`、`<link href>`、`<form action>`），对其进行分类（内部绝对/相对链接、外部链接、锚点、`mailto:`/`tel:`/`javascript:`/`data:`），并验证其是否存在。请参阅 [§5](#5-链接与验证)。
- 计算统计信息：按扩展名/类别分布、最大文件、具有最多出站链接的文件、被链接最多的外部域名。
- 通过 TUI（Textual）或可脚本化 CLI 呈现结果，支持三种导出格式（JSON、文本、带 5 种主题的 HTML）。
- 使用 SQLite 持久保存扫描历史记录，并支持查看和重新执行。

### Omega-fold 不执行的功能

- 内容或 SEO 分析（标题、元描述、关键词密度）。
- 不带安全限制的爬取：深度、页面数和请求间隔始终处于启用状态。
- 客户端 JavaScript 渲染（页面按服务器提供的原样获取，不会在无头浏览器中执行）。
- 主动漏洞扫描、模糊测试或暴力破解。
- Web 控制面板。

## 2. 安装

### 前置要求

- Python 3.10+
- 用于安装依赖的 Internet 连接
- 对于 TUI：终端中需要安装 [Nerd Font](https://www.nerdfonts.com/)，用于显示标题图标。如果没有该字体，字符会显示为空方框（与 emoji 类似的限制，但 Nerd Font 在终端用户中更为普及）。缺少字体不会影响功能，仅影响外观。

### 安装

```bash
[ -d omega-fold ] && echo "ℹ️ 已在此处解压，跳过此步骤。" || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`：

1. 如果 `.venv` 尚不存在，则创建虚拟环境。
2. 安装依赖（先处理 `vendor/omega-lib/`，然后执行 `pip install -e .`；`pyproject.toml` 始终是唯一的事实来源）。
3. 将 `omega-fold.sh` 和 `install.sh` 设置为可执行。
4. 将 `fold` 别名添加到 `~/.bashrc` 和 `~/.zshrc`（如果已存在则不会重复添加）。

### 依赖

在 `pyproject.toml` 中声明（不存在 `requirements.txt`）：
- `omega-lib`：套件共享库（导出主题、`ConfidenceLevel`），已包含在 `vendor/omega-lib/` 中
- `httpx`：同步验证外部链接（`LinkChecker`）
- `aiohttp`：异步 HTTP 爬取（`DistantCrawler`）
- `beautifulsoup4` + `lxml`：提取 HTML 链接
- `jinja2`：HTML 导出的模板引擎
- 开发依赖（`pip install -e ".[dev]"`）：`pytest`、`pytest-asyncio`、`pytest-cov`、`pytest-httpserver`、`ruff`、`mypy`、`import-linter`

## 3. 使用方法

### 交互模式（TUI）

建议日常使用时采用此模式 — 不带参数启动：

```bash
./omega-fold.sh
```
如果已经创建别名，只需在终端中输入：
```bash
fold
```

流程：启动界面（按键或点击后关闭）→ 主菜单（Scanner / History / Settings / Help）→ 输入目标、类型（本地/远程）、模式（静态/动态）和远程爬取安全限制，每个字段均带有明确标签 → 扫描（不确定进度指示器、实时操作日志，可随时点击取消）→ 扫描详情（按类别和扩展名的分布、树形结构、失效链接、导出）→ 历史记录（查看详情、**直接导出**而无需返回详情页、重新执行）以及主菜单中的设置。终端适配（颜色、尺寸和结构降级）会自动完成。

#### 键盘快捷键

| 按键 | 操作 |
|---|---|
| `↑` / `↓` | 在屏幕元素之间移动 |
| `Tab` / `Shift+Tab` | 在表单字段之间移动 |
| `Esc` | 返回上一屏（主页会显示退出确认） |
| `t` | 下一个主题（立即应用，无需确认） |
| `r` | 刷新终端检测 |
| `a` | 显示帮助 |
| `q` | 退出（需要确认） |

### 可脚本化模式（CLI）

任意子命令都会触发 CLI 模式：

```bash
# 本地扫描（树形结构 + 内部链接）
./omega-fold.sh scan /var/www/monsite --type local

# 动态模式下的本地扫描（还会通过 HTTP 验证外部链接）
./omega-fold.sh scan /var/www/monsite --type local --mode dynamic

# 远程扫描（从起始 URL 开始进行 BFS 爬取）
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# 历史记录（可按目标筛选）
./omega-fold.sh history --target /var/www/monsite --limit 20

# 扫描详情（文本、JSON 或 HTML）— 可选择 5 种导出主题
./omega-fold.sh show <scan_id> --format html --theme omega-base --output rapport.html
```

`scan` 选项：

| 选项 | 默认值 | 作用 |
|---|---|---|
| `--type` | *(必需)* | `local` 或 `distant` |
| `--mode` | `static` | `static`（不验证外部链接）或 `dynamic`（通过 HTTP 验证） |
| `--max-depth` | `5` | 最大跟踪深度（远程扫描） |
| `--max-pages` | `1000` | 最大爬取页面数（远程扫描） |
| `--delay` | `100` | 两次请求之间的延迟（毫秒，远程扫描） |
| `--user-agent` | `omega-fold/0.1` | 发送的 `User-Agent` 标头（远程扫描） |
| `--respect-robots` | 已禁用 | 遵守 `robots.txt`（远程扫描） |

对于远程扫描，没有协议的目标（`example.org`）会自动补全为 `https://example.org`；除非需要明确强制使用 `http://`，否则无需指定。

如果网站的页面数超过 `--max-pages`（默认 1000），扫描会在达到限制时停止，但会明确报告：`scan.status` 将为 `completed_truncated` 而非 `completed`，且 CLI 摘要、TUI 详情界面和 HTML 导出中都会显示警告。此时报告的文件数量并非网站实际大小；如需完整覆盖，请使用更高的 `--max-pages` 重新运行。

如果 `install.sh` 创建了别名，则无需 `./omega-fold.sh` 前缀，在终端任意位置都可以执行 `fold scan ...`。

## 4. 文件类别

每个文件都根据其扩展名归类到一个类别中（第一个匹配项优先）。完整说明和逐扩展名表格位于 `docs/FAMILIES.md`。

| 类别 | 扩展示例 |
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
| `other` | 其他所有文件 |

## 5. 链接与验证

### 分类

每个发现的链接（`href`/`src`/`action`）按以下优先顺序分类：

| 类型 | 识别条件 | 示例 |
|---|---|---|
| `empty` | 空字符串 | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | 特殊协议 | `mailto:x@y.z` |
| `anchor` | 直接以 `#` 开头（纯锚点） | `#section` |
| `external` | `http://`、`https://` 或 `//`（protocol-relative） | `https://example.org` |
| `absolute` | 以 `/` 开头 | `/img/logo.png` |
| `relative` | 其他所有情况 | `img/logo.png`, `../page.html` |

`absolute` 和 `relative` 是**内部**链接的两种形式。`page.html#section` 仍然属于 `relative`（末尾片段不会使它成为简单锚点；它仍会导航到另一项资源）。

### 验证

- **内部链接**：始终根据扫描期间实际发现的路径集合进行验证（不发送网络请求）。`absolute` 相对于扫描根目录解析；带分隔符的 `relative` 相对于源文件目录解析；不带分隔符的 `relative`（仅文件名）会在整个树中查找。对于远程扫描，验证会在爬取完成后进行第二次遍历，并基于实际成功访问的页面集合。超出安全限制或被 `robots.txt` 阻止的页面会保持为 `unchecked`，绝不会被假定为 `broken`。
- **外部链接**：仅在 `dynamic` 模式下通过 HTTP 请求验证（先 HEAD，如果 HEAD 失败则 GET）；在 `static` 模式下会保持为 `unchecked`。

## 6. 远程爬取安全限制

始终启用且无法禁用；只能调整其阈值：

- **深度**（`--max-depth`）：仅限制待爬取新页面的入队；已访问页面中发现的链接始终会在结果中报告，即使其目标页面不会被跟踪。
- **页面数**（`--max-pages`）：限制所有深度层级中访问的页面总数。
- **延迟**（`--delay`）：两个连续 HTTP 请求之间的暂停时间。
- **同一域名**：仅跟踪与起始 URL 具有相同 `netloc` 的内部链接。既检查链接路径，也检查**重定向后实际加载的 URL**：路径看似内部目录（`/go/xyz`、`/public/nom/`）但实际上重定向到外部域名的 permalink，永远不会被视为被扫描网站的页面。
- **`robots.txt`**（`--respect-robots`）：会加强而非削弱安全限制；禁止访问的页面永远不会被访问，其出站链接会保持为 `unchecked`。

## 7. 架构

Omega-fold 采用 **Clean Architecture**（domain / application / infrastructure / interfaces / ports / core / app / plugins / shared），与 `omega-` 套件模板保持一致（参见 `omega-scan`/`omega-check`/`omega-deep`），并在每次修改后由 `import-linter` 检查。完整说明位于 **`docs/ARCHITECTURE.md`**。

简要结构：

```text
src/omega_fold/
├── domain/          纯业务逻辑：扫描、树形结构、链接、统计、报告
├── application/     用例（commands/queries）— run_scan（local/distant）、export_scan_report...
├── ports/           应用所需的契约（local_fs_reader、distant_crawler、
│                    html_link_extractor、link_checker、scan_repository、report_exporter...）
├── infrastructure/  具体实现（os.walk、aiohttp、httpx、BeautifulSoup、SQLite、
│                    Jinja2 导出器 — Textual 不在此处）
├── interfaces/      tui/（Textual）和 cli/（可脚本化），保持严格的功能对等
├── app/             组装（DependencyContainer、bootstrap、生命周期）
├── core/, shared/   跨模块术语和非业务工具
└── plugins/         已建立但为空的结构（没有已确认的扩展轴）
```

设计规则：
- `domain/tree/service.py`：将已知的扁平文件列表聚合为树形结构，绝不执行 I/O；实际遍历（`os.walk`）位于 `infrastructure/filesystem/`。
- `domain/scans/policies.py`：爬取安全限制（深度/页面数/域名），无需网络即可测试的纯逻辑。
- `infrastructure/filesystem/` 和 `infrastructure/network/`：负责 I/O（磁盘、HTTP），从不做判断。
- `infrastructure/exporters/`：读取已组装的扫描结果，绝不重新计算统计信息。
- `infrastructure/storage/sqlite/`：仅存储源数据（`scans`/`files`/`links`）；树形结构和统计信息会在读取时由与初始扫描相同的纯函数重新计算（参见 `DECISIONS_ARCHITECTURE.md`，D-011），绝不在数据库中重复保存。

## 8. 导出

默认情况下，报告生成于 `var/exports/`（运行时路径以项目目录为基准，可使用 `$OMEGA_FOLD_VAR_DIR` 覆盖），或者生成到 `--output` 指定的路径。

### JSON，事实来源

完整的结果结构（`Scan` + 树形结构 + 链接 + 统计信息），严格可序列化为 JSON。

### 文本，紧凑的人类可读报告

摘要、按类别分布、ASCII 树形结构（限制为 6 个深度级别；文本报告并非用于列出包含数千个文件的树）以及失效链接列表。

### HTML，独立的 Web 报告

提供 5 种主题（`--theme`）。网站总大小会首先突出显示（这是扫描报告的主要目标），并且在所有位置以易读格式（KB/MB/GB...）显示，包括 CLI、TUI 和导出，而不是原始字节。专用布局包括：容器、统计网格、按类别分布的 SVG 直方图（手工绘制，无需大型图表依赖；与 `omega-deep` 中的架构图采用相同技术）、扩展名/最大文件表格。关联的外部域名直接显示前 20 个，其余部分放在可折叠面板中；失效链接列表默认折叠。

树形结构使用原生**多级** HTML 渲染：每个目录对应一个 `<details>`，默认只展开根目录，每个子目录都可单独点击展开，无需 JavaScript。

## 9. 历史记录

每次扫描都会持久化保存（SQLite，`var/db/omega-fold.db`）。可按目标查看历史记录（`omega-fold history --target ...`）、查看过去扫描的详情（`omega-fold show <scan_id>`），或从 TUI 的 History 菜单访问（包括重新执行）。

## 10. 终端兼容性

TUI（Textual）会自动检测终端能力（模拟器和尺寸），并相应调整结构样式表（`complete`/`standard`/`reduced`/`mono`），无需手动设置标志。CLI 模式始终保持纯文本，与终端无关。整个 `omega-` 套件共享此策略（`omega-lib`、`terminal/policies.py`）。

### 按检测到的模拟器选择配置文件

| 模拟器 | 初始配置文件 |
|---|---|
| Ghostty、Alacritty、WezTerm、Kitty | `complete` |
| Konsole、GNOME Terminal、Terminator、Xfce4 Terminal | `standard` |
| xterm、urxvt、现代 SSH | `reduced` |
| Linux TTY、旧版 SSH | `mono` |
| 未识别的模拟器 | `reduced`（默认回退） |

### 按终端尺寸选择配置文件

| 最小尺寸（列 × 行） | 配置文件上限 |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| 更小 | `mono` |

最终配置文件为**两者中限制更严格的一个**（模拟器和尺寸）；可以使用 `r` 键实时刷新。

## 11. 测试

```bash
source .venv/bin/activate
lint-imports        # 检查 Dependency Rule（6 个契约）
pytest -q           # 165 个测试
ruff check src tests
mypy -p omega_fold
```

结构：`tests/unit/`（domain 和 infrastructure，不进行真实 I/O：导出器、SVG 图表和 TUI 启动画面标记）、`tests/integration/`（通过 `tmp_path` 使用真实文件系统、通过 `pytest-httpserver` 使用虚假 HTTP 服务器、真实 SQLite 数据库、端到端 CLI）、`tests/tui/`（通过 `Pilot` 进行导航，结构测试；不声称执行自动视觉验证，请参阅 `docs/ARCHITECTURE.md` §TUI Interface）。

## 12. 不在范围内

- 内容/SEO 分析
- 客户端 JavaScript 渲染
- 不带安全限制的爬取
- 主动漏洞扫描、模糊测试或暴力破解
- Web 控制面板

---

> Omega-fold — 绘制结构图、验证其链接，绝不猜测尚未访问的内容。