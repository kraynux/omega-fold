<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Giấy phép MIT (xem tệp LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Công cụ phân tích cấu trúc trang web/thư mục (cục bộ và từ xa)**

> Được [kraynux](https://github.com/kraynux) xây dựng cho [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Trang chính thức: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Ảnh chụp màn hình: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-sử-dụng)

🌐 Giao diện và báo cáo xuất có sẵn bằng **17 ngôn ngữ** — xem [Ngôn ngữ giao diện](#ngôn-ngữ-giao-diện).  
**Ngôn ngữ:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** là công cụ TUI + CLI phân tích cấu trúc của một thư mục cục bộ hoặc một trang web từ xa (thu thập HTTP có giới hạn an toàn): cây thư mục đầy đủ, thống kê theo phần mở rộng/nhóm tệp, bản đồ liên kết (nội bộ/bên ngoài, mọi loại), phát hiện liên kết hỏng. Đây là một công cụ của bộ `omega-`, được tổ chức theo Clean Architecture — xem `docs/ARCHITECTURE.md` để biết đầy đủ chi tiết kỹ thuật.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-fold/D.png" width="24%" />
</p>

## 1. Tầm nhìn và phạm vi

### Omega-fold làm gì

- Quét một thư mục cục bộ (`os.walk` thật) hoặc thu thập một trang web từ xa theo chiều rộng (BFS), trong các giới hạn an toàn nghiêm ngặt.
- Dựng cây thư mục đầy đủ (tệp/thư mục, độ sâu, kích thước) và phân loại theo nhóm (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — xem [§4](#4-nhóm-tệp).
- Trích xuất mọi liên kết (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) từ mỗi trang/tệp HTML, phân loại chúng (nội bộ tuyệt đối/tương đối, bên ngoài, neo, `mailto:`/`tel:`/`javascript:`/`data:`) và kiểm tra chúng có tồn tại không — xem [§5](#5-liên-kết-và-kiểm-tra).
- Tính thống kê: phân bố theo phần mở rộng/nhóm, các tệp lớn nhất, các tệp có nhiều liên kết ra nhất, các tên miền bên ngoài được liên kết nhiều nhất.
- Hiển thị kết quả trong TUI (Textual) hoặc CLI có thể viết script, với ba kiểu xuất (JSON, văn bản, HTML với 5 giao diện màu).
- Lưu lịch sử quét lâu dài (SQLite), có thể xem lại và chạy lại.

### Omega-fold không làm gì

- Phân tích nội dung hoặc SEO (tiêu đề, mô tả meta, mật độ từ khóa).
- Thu thập không có giới hạn an toàn — độ sâu, số trang và khoảng nghỉ giữa các yêu cầu luôn được áp dụng.
- Kết xuất JavaScript phía máy khách (trang được lấy đúng như máy chủ trả về, không chạy trong trình duyệt không giao diện).
- Quét lỗ hổng chủ động, fuzzing, tấn công dò mật khẩu.
- Bảng điều khiển web.

## 2. Cài đặt

### Yêu cầu

- Python 3.10+
- Kết nối Internet, để cài các phụ thuộc
- Với TUI: một phông [Nerd Font](https://www.nerdfonts.com/) được cài trong terminal, cho biểu tượng ở phần đầu — nếu không có, ký tự này hiện thành ô vuông trống (cùng giới hạn như biểu tượng cảm xúc, nhưng phổ biến hơn nhiều ở người dùng terminal). Thiếu phông không ảnh hưởng đến hoạt động, chỉ thuần về hình thức.

### Cài đặt

```bash
[ -d omega-fold ] && echo "ℹ️ Đã giải nén ở đây, bỏ qua bước này." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Tạo môi trường ảo `.venv` nếu chưa có.
2. Cài các phụ thuộc (`vendor/omega-lib/` rồi `pip install -e .`; `pyproject.toml` vẫn là nguồn chuẩn duy nhất).
3. Cấp quyền thực thi cho `omega-fold.sh` và `install.sh`.
4. Thêm bí danh `fold` vào `~/.bashrc` và `~/.zshrc` (không trùng lặp nếu đã có).

### Phụ thuộc

Khai báo trong `pyproject.toml` (không có `requirements.txt`):
- `omega-lib`: thư viện dùng chung của bộ công cụ (giao diện xuất, `ConfidenceLevel`) — đi kèm trong `vendor/omega-lib/`
- `httpx`: kiểm tra đồng bộ các liên kết bên ngoài (`LinkChecker`)
- `aiohttp`: thu thập HTTP bất đồng bộ (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: trích xuất liên kết HTML
- `jinja2`: mẫu cho bản xuất HTML
- Phụ thuộc phát triển (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Sử dụng

### Chế độ tương tác (TUI)

Khuyên dùng hằng ngày — chạy không có đối số:

```bash
./omega-fold.sh
```
nếu đã tạo bí danh, chỉ cần gõ `fold` trong terminal:
```bash
fold
```

Trình tự: màn hình khởi động (đóng bằng một phím hoặc một cú nhấp) → menu chính (Quét / Lịch sử / Thiết lập / Trợ giúp) → nhập mục tiêu, loại (cục bộ/từ xa), chế độ (tĩnh/động) và các giới hạn an toàn khi thu thập từ xa, mỗi trường có nhãn rõ ràng riêng → quét (thanh tiến trình không xác định, nhật ký thao tác trực tiếp, nút Hủy bất cứ lúc nào) → chi tiết lần quét (phân bố theo nhóm và theo phần mở rộng, cây thư mục, liên kết hỏng, xuất) → lịch sử (xem chi tiết, **xuất trực tiếp** không cần qua màn hình chi tiết, chạy lại) và thiết lập từ menu chính. Việc thích ứng với terminal (màu, kích thước, giản lược cấu trúc) là tự động.

#### Phím tắt

| Phím | Thao tác |
|---|---|
| `↑` / `↓` | Di chuyển giữa các mục trên màn hình |
| `Tab` / `Shift+Tab` | Di chuyển giữa các trường của biểu mẫu |
| `Esc` | Quay lại màn hình trước (xác nhận thoát ở màn hình chính) |
| `t` | Giao diện màu tiếp theo (áp dụng ngay, không cần xác nhận) |
| `r` | Làm mới việc nhận diện terminal |
| `a` | Hiện trợ giúp |
| `q` | Thoát (có xác nhận) |

### Ngôn ngữ giao diện

Giao diện có sẵn bằng 17 ngôn ngữ: tiếng Pháp, tiếng Anh, tiếng Tây Ban Nha, tiếng Bồ Đào Nha (Brasil), tiếng Ý, tiếng Đức, tiếng Hà Lan, tiếng Ba Lan, tiếng Nga, tiếng Trung giản thể, tiếng Việt, tiếng Thái, tiếng Indonesia, tiếng Nhật, tiếng Hàn, tiếng Hindi và tiếng Ả Rập. Ngôn ngữ được chọn trong Thiết lập (“Langue / Language”) và có hiệu lực sau khi khởi động lại giao diện; biến `OMEGA_FOLD_LANG` (ví dụ `OMEGA_FOLD_LANG=vi ./omega-fold.sh`) buộc dùng một ngôn ngữ trong một phiên. Khi được chạy từ omega-suite, omega-fold dùng ngôn ngữ của bộ công cụ. Trên console văn bản Linux (TTY), giao diện hiển thị bằng tiếng Anh trong phiên đó đối với tiếng Việt và các ngôn ngữ không dùng chữ Latinh. Dòng lệnh vẫn bằng tiếng Pháp.

### Liên hệ và hỗ trợ

Phần trợ giúp (phím `a`) có màn hình **Liên hệ và hỗ trợ**: *Mời một ly cà phê* (trang PayPal của nhà phát triển), *Liên hệ hỗ trợ* (địa chỉ email và biểu mẫu liên hệ của trang web, hiển thị rõ ràng), *Khai báo là người dùng (ẩn danh)* và *Kiểm tra cập nhật*. Việc khai báo là tự nguyện, tắt theo mặc định và chỉ gửi một lần: nó chỉ dùng để đếm số người dùng và, nếu bạn muốn, châu lục hoặc quốc gia của họ (danh sách đóng, không bao giờ là văn bản tự do). Nó gửi một khóa được tạo ngẫu nhiên, tên phần mềm (`omega-fold`) và phiên bản của nó; không bao giờ gửi tên, tên máy, thiết lập, mục tiêu hay kết quả. Địa chỉ IP không được lưu trong các khai báo, nhưng, như mọi lượt truy cập, nó đi qua các kiểm tra bảo mật và nhật ký của máy chủ nhận. Có thể rút lại bất cứ lúc nào từ cùng màn hình (*Không khai báo tôi nữa*). Việc kiểm tra cập nhật chỉ đọc danh sách các phiên bản đã phát hành trên trang web, và không bao giờ khi chưa nhấp.

### Chế độ script (CLI)

Bất kỳ lệnh con nào cũng kích hoạt chế độ CLI:

```bash
# Quét cục bộ (cây thư mục + liên kết nội bộ)
./omega-fold.sh scan /var/www/trangcuatoi --type local

# Quét cục bộ ở chế độ động (kiểm tra cả liên kết bên ngoài qua HTTP)
./omega-fold.sh scan /var/www/trangcuatoi --type local --mode dynamic

# Quét từ xa (thu thập BFS từ URL bắt đầu)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Lịch sử (lọc được theo mục tiêu)
./omega-fold.sh history --target /var/www/trangcuatoi --limit 20

# Chi tiết một lần quét (văn bản, JSON hoặc HTML) — chọn 1 trong 5 giao diện xuất
./omega-fold.sh show <scan_id> --format html --theme omega-base --output baocao.html
```

Tùy chọn của `scan`:

| Tùy chọn | Mặc định | Tác dụng |
|---|---|---|
| `--type` | *(bắt buộc)* | `local` hoặc `distant` (từ xa) |
| `--mode` | `static` | `static` (không kiểm tra liên kết bên ngoài) hoặc `dynamic` (kiểm tra qua HTTP) |
| `--max-depth` | `5` | Độ sâu tối đa được theo (quét từ xa) |
| `--max-pages` | `1000` | Số trang tối đa được thu thập (quét từ xa) |
| `--delay` | `100` | Khoảng nghỉ (ms) giữa hai yêu cầu (quét từ xa) |
| `--user-agent` | `omega-fold/0.1` | Tiêu đề `User-Agent` được gửi (quét từ xa) |
| `--respect-robots` | tắt | Tuân theo `robots.txt` (quét từ xa) |

Khi quét từ xa, mục tiêu không có giao thức (`example.org`) được tự động bổ sung thành `https://example.org` — không cần ghi rõ, trừ khi muốn buộc dùng `http://`.

Nếu trang web có nhiều trang hơn `--max-pages` (mặc định 1000), lần quét dừng ở giới hạn nhưng báo rõ điều đó: `scan.status` là `completed_truncated` thay vì `completed`, kèm cảnh báo hiển thị trong phần tóm tắt CLI, màn hình chi tiết của TUI và bản xuất HTML — khi đó số tệp được báo không phải kích thước thật của trang web; hãy chạy lại với `--max-pages` cao hơn để bao quát đầy đủ.

Nếu bí danh được `install.sh` tạo, `fold scan ...` hoạt động ở bất kỳ đâu trong terminal, không cần tiền tố `./omega-fold.sh`.

## 4. Nhóm tệp

Mỗi tệp được xếp vào một nhóm theo phần mở rộng (kết quả khớp đầu tiên được chọn) — chi tiết đầy đủ và bảng theo từng phần mở rộng: `docs/FAMILIES.md`.

| Nhóm | Ví dụ phần mở rộng |
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
| `other` | mọi thứ còn lại |

## 5. Liên kết và kiểm tra

### Phân loại

Mỗi liên kết tìm thấy (`href`/`src`/`action`) được phân loại theo thứ tự ưu tiên sau:

| Loại | Nhận diện khi | Ví dụ |
|---|---|---|
| `empty` | Chuỗi rỗng | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Giao thức đặc biệt | `mailto:x@y.z` |
| `anchor` | Bắt đầu trực tiếp bằng `#` (neo thuần) | `#section` |
| `external` | `http://`, `https://` hoặc `//` (tương đối theo giao thức) | `https://example.org` |
| `absolute` | Bắt đầu bằng `/` | `/img/logo.png` |
| `relative` | Mọi thứ còn lại | `img/logo.png`, `../page.html` |

`absolute` và `relative` là hai dạng của một liên kết **nội bộ** — liên kết `page.html#section` vẫn là `relative` (đoạn ở cuối không biến nó thành một neo đơn thuần; nó thực sự dẫn tới một tài nguyên khác).

### Kiểm tra

- **Liên kết nội bộ**: luôn được kiểm tra với tập các đường dẫn thực sự tìm thấy trong lần quét (không có yêu cầu mạng) — `absolute` được phân giải từ gốc của lần quét, `relative` có dấu phân cách được phân giải từ thư mục của tệp nguồn, `relative` không có dấu phân cách (chỉ tên tệp) được tìm trong toàn bộ cây. Khi quét từ xa, việc kiểm tra diễn ra ở lượt thứ hai sau khi thu thập xong, đối chiếu với tập các trang thực sự truy cập thành công — một trang nằm ngoài giới hạn an toàn hoặc bị `robots.txt` chặn sẽ giữ `unchecked`, không bao giờ bị phỏng đoán là `broken`.
- **Liên kết bên ngoài**: được kiểm tra bằng một yêu cầu HTTP (HEAD, rồi GET nếu HEAD thất bại) chỉ ở chế độ `dynamic` — ở chế độ `static`, nó giữ `unchecked`.

## 6. Giới hạn an toàn khi thu thập từ xa

Luôn bật, không bao giờ tắt được — chỉ điều chỉnh được ngưỡng:

- **Độ sâu** (`--max-depth`): chỉ giới hạn việc đưa trang mới vào hàng đợi thu thập; các liên kết tìm thấy trên một trang đã truy cập luôn có trong kết quả, kể cả khi trang mà chúng trỏ tới sẽ không được theo.
- **Số trang** (`--max-pages`): giới hạn tổng số trang được truy cập, ở mọi độ sâu.
- **Khoảng nghỉ** (`--delay`): thời gian dừng giữa hai yêu cầu HTTP liên tiếp.
- **Cùng tên miền**: chỉ theo các liên kết nội bộ tới cùng `netloc` với URL bắt đầu — được kiểm tra cả trên đường dẫn của liên kết lẫn trên URL **thực sự được tải sau chuyển hướng**: một liên kết cố định có đường dẫn trông như thư mục nội bộ (`/go/xyz`, `/public/ten/`) nhưng thực ra chuyển hướng tới tên miền bên ngoài sẽ không bao giờ được coi là trang của trang web đang quét (nội dung của nó không phải của bạn).
- **`robots.txt`** (`--respect-robots`): củng cố giới hạn an toàn thay vì làm yếu đi — một trang bị cấm không bao giờ được truy cập, các liên kết ra của nó giữ `unchecked`.

## 7. Kiến trúc

Omega-fold được tổ chức theo **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), thống nhất với mẫu của bộ `omega-` (xem `omega-scan`/`omega-check`/`omega-deep`) và được `import-linter` kiểm tra ở mỗi thay đổi. Chi tiết đầy đủ nằm trong **`docs/ARCHITECTURE.md`**.

Tổng quan rất ngắn:

```text
src/omega_fold/
├── domain/          Logic nghiệp vụ thuần: quét, cây thư mục (tree), liên kết, thống kê, báo cáo
├── application/     Ca sử dụng (commands/queries) — run_scan (cục bộ/từ xa), export_scan_report...
├── ports/           Hợp đồng mà ứng dụng cần (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Triển khai cụ thể (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    bộ xuất Jinja2 — Textual KHÔNG nằm ở đây)
├── interfaces/      tui/ (Textual) và cli/ (viết script được), tương đương chức năng nghiêm ngặt
├── app/             Lắp ráp (DependencyContainer, bootstrap, vòng đời)
├── core/, shared/   Từ vựng dùng chung, tiện ích không thuộc nghiệp vụ
└── plugins/         Đã có cấu trúc, đang trống (chưa có hướng mở rộng nào được xác nhận)
```

Quy tắc thiết kế:
- `domain/tree/service.py`: gộp một danh sách tệp phẳng đã biết thành cây, không bao giờ thực hiện I/O — việc duyệt thật (`os.walk`) nằm trong `infrastructure/filesystem/`.
- `domain/scans/policies.py`: giới hạn an toàn khi thu thập (độ sâu/số trang/tên miền), logic thuần, kiểm thử được mà không cần mạng.
- `infrastructure/filesystem/` và `infrastructure/network/`: thực hiện I/O (đĩa, HTTP), không bao giờ đánh giá.
- `infrastructure/exporters/`: đọc kết quả quét đã lắp ráp sẵn, không bao giờ tính lại một thống kê.
- `infrastructure/storage/sqlite/`: chỉ lưu dữ liệu nguồn (`scans`/`files`/`links`) — cây thư mục và thống kê được tính lại khi đọc bằng chính các hàm thuần đã dùng ở lần quét đầu (xem `DECISIONS_ARCHITECTURE.md`, D-011), không bao giờ lưu trùng trong cơ sở dữ liệu.

## 8. Xuất

Báo cáo văn bản và HTML được viết bằng ngôn ngữ chọn trong Thiết lập (“Ngôn ngữ bản xuất”, mặc định là ngôn ngữ giao diện); JSON vẫn là dữ liệu, không được dịch. Báo cáo được tạo mặc định trong `var/exports/` (đường dẫn khi chạy gắn với thư mục dự án, dùng `$OMEGA_FOLD_VAR_DIR` để thay đổi), hoặc tại đường dẫn được chỉ định (`--output`).

### JSON, nguồn chuẩn

Toàn bộ cấu trúc của kết quả (`Scan` + cây thư mục + liên kết + thống kê), tuần tự hóa JSON nghiêm ngặt.

### Văn bản, báo cáo dễ đọc gọn nhẹ

Tóm tắt, phân bố theo nhóm, cây ASCII (giới hạn 6 cấp độ sâu — báo cáo văn bản không nhằm liệt kê một cây hàng nghìn tệp), danh sách liên kết hỏng.

### HTML, báo cáo web độc lập

5 giao diện màu để chọn (`--theme`). Tổng kích thước trang web được làm nổi bật đầu tiên (đó là mục tiêu chính của một báo cáo quét) và hiển thị ở dạng dễ đọc (KB/MB/GB...) ở mọi nơi — CLI, TUI, bản xuất — thay vì số byte thô. Bố cục riêng: khung chứa, lưới thống kê, biểu đồ SVG phân bố theo nhóm (vẽ thủ công, không dùng thư viện biểu đồ nặng — cùng kỹ thuật với sơ đồ kiến trúc của `omega-deep`), bảng phần mở rộng/tệp lớn nhất. Với các tên miền bên ngoài được liên kết, 20 tên miền đầu hiện ngay, phần còn lại nằm trong một khung thu gọn (hữu ích với trang web có hàng trăm chuyển hướng ra ngoài); danh sách liên kết hỏng được thu gọn theo mặc định.

Cây thư mục được hiển thị bằng HTML gốc **nhiều cấp**: mỗi thư mục một `<details>`, mặc định chỉ mở thư mục gốc, mỗi thư mục con mở ra độc lập khi nhấp (lấy cảm hứng từ một script tạo chỉ mục của người dùng) — trình duyệt chỉ dàn trang phần nội dung đang mở, nên vẫn dùng tốt ngay cả với trang web có hàng chục nghìn tệp, không cần JavaScript.

## 9. Lịch sử

Mỗi lần quét đều được lưu (SQLite, `var/db/omega-fold.db`). Có thể xem lịch sử theo mục tiêu (`omega-fold history --target ...`), chi tiết một lần quét trước (`omega-fold show <scan_id>`), hoặc từ menu Lịch sử của TUI (bao gồm chạy lại).

## 10. Tương thích terminal

TUI (Textual) tự động nhận diện khả năng của terminal (trình giả lập, kích thước) và điều chỉnh bảng kiểu cấu trúc tương ứng (`complete`/`standard`/`reduced`/`mono`), không cần tùy chọn thủ công. Chế độ CLI luôn là văn bản thuần, không phụ thuộc terminal. Đây là chính sách chung của toàn bộ `omega-` (`omega-lib`, `terminal/policies.py`).

### Cấu hình theo trình giả lập được nhận diện

| Trình giả lập | Cấu hình ban đầu |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH hiện đại | `reduced` |
| TTY Linux, SSH cũ | `mono` |
| Trình giả lập không nhận diện được | `reduced` (dự phòng mặc định) |

### Cấu hình theo kích thước terminal

| Kích thước tối thiểu (cột × dòng) | Mức trần cấu hình |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| nhỏ hơn | `mono` |

Cấu hình cuối cùng là **cấu hình hạn chế hơn trong hai** (trình giả lập và kích thước) — có thể làm mới trực tiếp bằng phím `r`.

## 11. Kiểm thử

```bash
source .venv/bin/activate
lint-imports        # kiểm tra Dependency Rule (6 hợp đồng)
pytest -q           # 186 bài kiểm thử
ruff check src tests
mypy -p omega_fold
```

Cấu trúc: `tests/unit/` (domain và hạ tầng không có I/O thật — bộ xuất, biểu đồ SVG, đánh dấu màn hình khởi động TUI), `tests/integration/` (hệ thống tệp thật qua `tmp_path`, máy chủ HTTP giả `pytest-httpserver`, cơ sở dữ liệu SQLite thật, CLI từ đầu đến cuối), `tests/tui/` (điều hướng qua `Pilot`, mang tính cấu trúc — không tự nhận đã kiểm tra hình ảnh, xem `docs/ARCHITECTURE.md` §Giao diện TUI).

## 12. Ngoài phạm vi

- Phân tích nội dung/SEO
- Kết xuất JavaScript phía máy khách
- Thu thập không có giới hạn an toàn
- Quét lỗ hổng chủ động, fuzzing, dò mật khẩu
- Bảng điều khiển web

---

> Omega-fold — Lập bản đồ một cấu trúc, kiểm tra liên kết của nó, không bao giờ đoán những gì chưa được truy cập.
