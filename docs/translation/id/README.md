<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Lisensi MIT (lihat berkas LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Penganalisis struktur situs/direktori (lokal dan jarak jauh)**

> Dibuat oleh [kraynux](https://github.com/kraynux) untuk [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

Halaman resmi: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Tangkapan layar: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-penggunaan)

🌐 Antarmuka dan laporan ekspor tersedia dalam **17 bahasa** — lihat [Bahasa antarmuka](#bahasa-antarmuka).  
**Bahasa:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** adalah alat TUI + CLI yang menganalisis struktur direktori lokal atau situs jarak jauh (crawl HTTP yang dibatasi pengaman): pohon lengkap, statistik per ekstensi/kelompok berkas, peta tautan (internal/eksternal, semua jenis), deteksi tautan rusak. Alat dari rangkaian `omega-`, disusun dengan Clean Architecture — lihat `docs/ARCHITECTURE.md` untuk detail teknis lengkap.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-fold/D.png" width="24%" />
</p>

## 1. Visi dan cakupan

### Yang dilakukan Omega-fold

- Memindai direktori lokal (`os.walk` sungguhan) atau meng-crawl situs jarak jauh secara melebar (BFS), dibatasi pengaman yang ketat.
- Membangun pohon lengkap (berkas/direktori, kedalaman, ukuran) dan mengelompokkannya (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — lihat [§4](#4-kelompok-berkas).
- Mengambil semua tautan (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) dari setiap halaman/berkas HTML, menggolongkannya (internal absolut/relatif, eksternal, jangkar, `mailto:`/`tel:`/`javascript:`/`data:`) dan memeriksa keberadaannya — lihat [§5](#5-tautan-dan-pemeriksaan).
- Menghitung statistik: sebaran per ekstensi/kelompok, berkas terbesar, berkas dengan tautan keluar terbanyak, domain eksternal yang paling sering ditautkan.
- Menampilkan hasil di TUI (Textual) atau CLI yang bisa dipakai dalam skrip, dengan tiga ekspor (JSON, teks, HTML dengan 5 tema).
- Menyimpan riwayat pemindaian permanen (SQLite) yang dapat dilihat dan diulang.

### Yang tidak dilakukan Omega-fold

- Analisis konten atau SEO (judul, deskripsi meta, kepadatan kata kunci).
- Crawl tanpa pengaman — kedalaman, jumlah halaman, dan jeda antarpermintaan selalu aktif.
- Rendering JavaScript di sisi klien (halaman diambil apa adanya dari server, tidak dijalankan di peramban headless).
- Pemindaian kerentanan aktif, fuzzing, brute force.
- Dasbor web.

## 2. Instalasi

### Prasyarat

- Python 3.10+
- Koneksi Internet, untuk dependensi
- Untuk TUI: fon [Nerd Font](https://www.nerdfonts.com/) terpasang di terminal, untuk ikon di header — tanpanya, karakter ini tampil sebagai kotak kosong (keterbatasan yang sama dengan emoji, tetapi jauh lebih umum tersedia di kalangan pengguna terminal). Ketiadaannya tidak memengaruhi fungsi, murni soal tampilan.

### Instalasi

```bash
[ -d omega-fold ] && echo "ℹ️ Sudah diekstrak di sini, langkah dilewati." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Membuat lingkungan virtual `.venv` jika belum ada.
2. Memasang dependensi (`vendor/omega-lib/` lalu `pip install -e .`; `pyproject.toml` tetap menjadi satu-satunya sumber kebenaran).
3. Menjadikan `omega-fold.sh` dan `install.sh` dapat dieksekusi.
4. Menambahkan alias `fold` ke `~/.bashrc` dan `~/.zshrc` (tanpa duplikat jika sudah ada).

### Dependensi

Dideklarasikan di `pyproject.toml` (tanpa `requirements.txt`):
- `omega-lib`: pustaka bersama rangkaian (tema ekspor, `ConfidenceLevel`) — disertakan di `vendor/omega-lib/`
- `httpx`: pemeriksaan sinkron tautan eksternal (`LinkChecker`)
- `aiohttp`: crawl HTTP asinkron (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: pengambilan tautan HTML
- `jinja2`: templat untuk ekspor HTML
- Dependensi pengembangan (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Penggunaan

### Mode interaktif (TUI)

Disarankan untuk pemakaian sehari-hari — dijalankan tanpa argumen:

```bash
./omega-fold.sh
```
jika Anda sudah membuat alias, cukup ketik `fold` di terminal:
```bash
fold
```

Alur: layar pembuka (tertutup dengan satu tombol atau klik) → menu utama (Pindai / Riwayat / Pengaturan / Bantuan) → isian target, jenis (lokal/jarak jauh), mode (statis/dinamis), dan pengaman crawl jarak jauh, masing-masing dengan labelnya sendiri yang jelas → pemindaian (indikator tak tentu, log operasi langsung, tombol Batal kapan saja) → detail pemindaian (sebaran per kelompok dan per ekstensi, pohon, tautan rusak, ekspor) → riwayat (lihat detail, **ekspor langsung** tanpa melalui detail, ulangi) dan pengaturan dari menu utama. Penyesuaian dengan terminal (warna, ukuran, penyederhanaan struktur) berlangsung otomatis.

#### Pintasan keyboard

| Tombol | Aksi |
|---|---|
| `↑` / `↓` | Berpindah antarelemen layar |
| `Tab` / `Shift+Tab` | Berpindah antarkolom formulir |
| `Esc` | Kembali ke layar sebelumnya (konfirmasi keluar di layar awal) |
| `t` | Tema berikutnya (langsung diterapkan, tanpa konfirmasi) |
| `r` | Menyegarkan deteksi terminal |
| `a` | Menampilkan bantuan |
| `q` | Keluar (dengan konfirmasi) |

### Bahasa antarmuka

Antarmuka tersedia dalam 17 bahasa: Prancis, Inggris, Spanyol, Portugis (Brasil), Italia, Jerman, Belanda, Polandia, Rusia, Tionghoa Sederhana, Vietnam, Thai, Indonesia, Jepang, Korea, Hindi, dan Arab. Pilihan dibuat di Pengaturan (“Langue / Language”) dan berlaku setelah antarmuka dimulai ulang; variabel `OMEGA_FOLD_LANG` (misalnya `OMEGA_FOLD_LANG=id ./omega-fold.sh`) memaksakan bahasa untuk satu sesi. Jika dijalankan dari omega-suite, omega-fold memakai bahasa rangkaian. Di konsol teks Linux (TTY), bahasa beraksara non-Latin ditampilkan dalam bahasa Inggris selama sesi itu. Baris perintah tetap berbahasa Prancis.

### Kontak dan dukungan

Bantuan (tombol `a`) menyediakan layar **Kontak dan dukungan**: *Traktir kopi* (halaman PayPal pengembang), *Hubungi dukungan* (alamat email dan formulir kontak situs, ditampilkan apa adanya), *Daftarkan saya sebagai pengguna (anonim)*, dan *Periksa pembaruan*. Pendaftaran bersifat sukarela, nonaktif secara bawaan, dan dikirim hanya sekali: hanya digunakan untuk menghitung pengguna dan, jika Anda mau, benua atau negara mereka (daftar tertutup, tidak pernah teks bebas). Yang dikirim adalah kunci yang diambil secara acak, nama perangkat lunak (`omega-fold`), dan versinya; tidak pernah nama, nama mesin, pengaturan, target, maupun hasil. Alamat IP tidak disimpan dalam pendaftaran, tetapi, seperti setiap kunjungan, melewati pemeriksaan keamanan dan log server penerima. Penarikan kapan saja dari layar yang sama (*Jangan daftarkan saya lagi*). Pemeriksaan pembaruan hanya membaca daftar versi yang dipublikasikan di situs, dan tidak pernah tanpa klik.

### Mode skrip (CLI)

Setiap subperintah mengaktifkan mode CLI:

```bash
# Pemindaian lokal (pohon + tautan internal)
./omega-fold.sh scan /var/www/situsku --type local

# Pemindaian lokal mode dinamis (juga memeriksa tautan eksternal melalui HTTP)
./omega-fold.sh scan /var/www/situsku --type local --mode dynamic

# Pemindaian jarak jauh (crawl BFS dari URL awal)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Riwayat (dapat difilter per target)
./omega-fold.sh history --target /var/www/situsku --limit 20

# Detail pemindaian (teks, JSON, atau HTML) — 5 tema ekspor untuk dipilih
./omega-fold.sh show <scan_id> --format html --theme omega-base --output laporan.html
```

Opsi `scan`:

| Opsi | Bawaan | Efek |
|---|---|---|
| `--type` | *(wajib)* | `local` atau `distant` (jarak jauh) |
| `--mode` | `static` | `static` (tautan eksternal tidak diperiksa) atau `dynamic` (diperiksa melalui HTTP) |
| `--max-depth` | `5` | Kedalaman maksimum yang diikuti (pemindaian jarak jauh) |
| `--max-pages` | `1000` | Jumlah maksimum halaman yang di-crawl (pemindaian jarak jauh) |
| `--delay` | `100` | Jeda (ms) antara dua permintaan (pemindaian jarak jauh) |
| `--user-agent` | `omega-fold/0.1` | Header `User-Agent` yang dikirim (pemindaian jarak jauh) |
| `--respect-robots` | nonaktif | Mematuhi `robots.txt` (pemindaian jarak jauh) |

Untuk pemindaian jarak jauh, target tanpa skema (`example.org`) otomatis dilengkapi menjadi `https://example.org` — tidak perlu ditulis kecuali untuk memaksa `http://` secara eksplisit.

Jika situs memiliki lebih banyak halaman daripada `--max-pages` (bawaan 1000), pemindaian berhenti di batas tetapi melaporkannya secara eksplisit: `scan.status` bernilai `completed_truncated` alih-alih `completed`, dengan peringatan yang terlihat di ringkasan CLI, layar detail TUI, dan ekspor HTML — jumlah berkas yang dilaporkan saat itu bukan ukuran situs sebenarnya; jalankan ulang dengan `--max-pages` yang lebih tinggi untuk cakupan penuh.

Jika alias dibuat oleh `install.sh`, `fold scan ...` berfungsi dari mana saja di terminal, tanpa awalan `./omega-fold.sh`.

## 4. Kelompok berkas

Setiap berkas digolongkan ke dalam kelompok berdasarkan ekstensinya (kecocokan pertama yang menang) — detail lengkap dan tabel per ekstensi: `docs/FAMILIES.md`.

| Kelompok | Contoh ekstensi |
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
| `other` | selebihnya |

## 5. Tautan dan pemeriksaan

### Penggolongan

Setiap tautan yang ditemukan (`href`/`src`/`action`) digolongkan dengan urutan prioritas berikut:

| Jenis | Dikenali bila | Contoh |
|---|---|---|
| `empty` | String kosong | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Skema khusus | `mailto:x@y.z` |
| `anchor` | Langsung diawali `#` (jangkar murni) | `#section` |
| `external` | `http://`, `https://`, atau `//` (relatif terhadap protokol) | `https://example.org` |
| `absolute` | Diawali `/` | `/img/logo.png` |
| `relative` | Selebihnya | `img/logo.png`, `../page.html` |

`absolute` dan `relative` adalah dua bentuk tautan **internal** — tautan `page.html#section` tetap `relative` (fragmen di akhir tidak menjadikannya jangkar biasa; tautan itu benar-benar menuju sumber daya lain).

### Pemeriksaan

- **Tautan internal**: selalu diperiksa terhadap kumpulan jalur yang benar-benar ditemukan selama pemindaian (tanpa permintaan jaringan) — `absolute` diselesaikan dari akar pemindaian, `relative` dengan pemisah diselesaikan dari direktori berkas sumber, `relative` tanpa pemisah (hanya nama berkas) dicari di seluruh pohon. Untuk pemindaian jarak jauh, pemeriksaan dilakukan pada putaran kedua setelah crawl selesai, terhadap kumpulan halaman yang benar-benar berhasil dikunjungi — halaman di luar pengaman atau diblokir `robots.txt` tetap `unchecked`, tidak pernah `broken` berdasarkan dugaan.
- **Tautan eksternal**: diperiksa dengan permintaan HTTP (HEAD, lalu GET jika HEAD gagal) hanya dalam mode `dynamic` — dalam mode `static`, tautan tetap `unchecked`.

## 6. Pengaman crawl jarak jauh

Selalu aktif, tidak pernah bisa dimatikan — hanya ambangnya yang dapat diatur:

- **Kedalaman** (`--max-depth`): hanya membatasi masuknya halaman baru ke antrean crawl; tautan yang ditemukan di halaman yang sudah dikunjungi selalu tercantum dalam hasil, meskipun halaman tujuannya tidak akan diikuti.
- **Jumlah halaman** (`--max-pages`): membatasi total halaman yang dikunjungi di semua kedalaman.
- **Jeda** (`--delay`): jeda antara dua permintaan HTTP berturut-turut.
- **Domain yang sama**: hanya tautan internal ke `netloc` yang sama dengan URL awal yang diikuti — diperiksa pada jalur tautan maupun pada URL yang **benar-benar dimuat setelah pengalihan**: permalink yang jalurnya mirip folder internal (`/go/xyz`, `/public/nama/`) tetapi sebenarnya mengalihkan ke domain eksternal tidak pernah diperlakukan sebagai halaman situs yang dipindai (isinya bukan milik Anda).
- **`robots.txt`** (`--respect-robots`): memperkuat pengaman alih-alih melemahkannya — halaman terlarang tidak pernah dikunjungi, tautan keluarnya tetap `unchecked`.

## 7. Arsitektur

Omega-fold disusun dengan **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), selaras dengan templat rangkaian `omega-` (lihat `omega-scan`/`omega-check`/`omega-deep`) dan diverifikasi oleh `import-linter` pada setiap perubahan. Detail lengkap ada di **`docs/ARCHITECTURE.md`**.

Gambaran singkat:

```text
src/omega_fold/
├── domain/          Logika bisnis murni: pemindaian, pohon (tree), tautan, statistik, laporan
├── application/     Kasus penggunaan (commands/queries) — run_scan (lokal/jarak jauh), export_scan_report...
├── ports/           Kontrak yang diharapkan aplikasi (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implementasi konkret (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    pengekspor Jinja2 — Textual TIDAK ada di sini)
├── interfaces/      tui/ (Textual) dan cli/ (untuk skrip), dengan kesetaraan fungsi yang ketat
├── app/             Perakitan (DependencyContainer, bootstrap, siklus hidup)
├── core/, shared/   Kosakata lintas bagian, utilitas nonbisnis
└── plugins/         Struktur sudah disiapkan, kosong (belum ada arah perluasan yang dipastikan)
```

Aturan desain:
- `domain/tree/service.py`: menggabungkan daftar datar berkas yang sudah diketahui menjadi pohon, tidak pernah melakukan I/O — penelusuran sebenarnya (`os.walk`) ada di `infrastructure/filesystem/`.
- `domain/scans/policies.py`: pengaman crawl (kedalaman/halaman/domain), logika murni yang dapat diuji tanpa jaringan.
- `infrastructure/filesystem/` dan `infrastructure/network/`: melakukan I/O (disk, HTTP), tidak pernah menilai.
- `infrastructure/exporters/`: membaca hasil pemindaian yang sudah dirakit, tidak pernah menghitung ulang statistik.
- `infrastructure/storage/sqlite/`: hanya menyimpan data sumber (`scans`/`files`/`links`) — pohon dan statistik dihitung ulang saat dibaca oleh fungsi murni yang sama dengan pemindaian awal (lihat `DECISIONS_ARCHITECTURE.md`, D-011), tidak pernah diduplikasi di basis data.

## 8. Ekspor

Laporan teks dan HTML ditulis dalam bahasa yang dipilih di Pengaturan (“Bahasa ekspor”, bawaannya sama dengan antarmuka); JSON tetap berupa data dan tidak diterjemahkan. Laporan dibuat di `var/exports/` secara bawaan (jalur runtime yang berjangkar pada folder proyek, `$OMEGA_FOLD_VAR_DIR` untuk menggantinya), atau di jalur yang ditentukan (`--output`).

### JSON, sumber kebenaran

Struktur lengkap hasil (`Scan` + pohon + tautan + statistik), sepenuhnya dapat diserialisasi ke JSON.

### Teks, laporan ringkas yang mudah dibaca

Ringkasan, sebaran per kelompok, pohon ASCII (dibatasi 6 tingkat kedalaman — laporan teks tidak dimaksudkan untuk mendaftar pohon ribuan berkas), daftar tautan rusak.

### HTML, laporan web mandiri

5 tema pilihan (`--theme`). Ukuran total situs ditonjolkan paling awal (itulah tujuan utama laporan pemindaian) dan ditampilkan dalam format yang mudah dibaca (KB/MB/GB...) di mana-mana — CLI, TUI, ekspor — bukan dalam byte mentah. Tata letak khusus: wadah, kisi statistik, histogram SVG sebaran per kelompok (digambar manual, tanpa dependensi grafik yang berat — teknik yang sama dengan diagram arsitektur `omega-deep`), tabel ekstensi/berkas terbesar. Domain eksternal yang ditautkan menampilkan 20 teratas secara langsung dan sisanya di panel lipat (berguna untuk situs dengan ratusan pengalihan eksternal); daftar tautan rusak dilipat secara bawaan.

Pohon ditampilkan dalam HTML asli **bertingkat**: satu `<details>` per direktori, hanya akar yang terbuka secara bawaan, setiap subfolder terbuka sendiri-sendiri saat diklik (terinspirasi dari skrip pembuat indeks milik pengguna) — peramban hanya menata konten yang terbuka, sehingga tetap dapat digunakan bahkan untuk situs dengan puluhan ribu berkas, tanpa JavaScript.

## 9. Riwayat

Setiap pemindaian disimpan (SQLite, `var/db/omega-fold.db`). Riwayat dapat dilihat per target (`omega-fold history --target ...`), detail pemindaian lama (`omega-fold show <scan_id>`), atau dari menu Riwayat di TUI (termasuk pengulangan).

## 10. Kompatibilitas terminal

TUI (Textual) otomatis mendeteksi kemampuan terminal (emulator, ukuran) dan menyesuaikan lembar gaya strukturalnya (`complete`/`standard`/`reduced`/`mono`), tanpa opsi manual. Mode CLI selalu berupa teks biasa, tidak bergantung pada terminal. Kebijakan ini dipakai bersama oleh seluruh rangkaian `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil menurut emulator yang terdeteksi

| Emulator | Profil awal |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH modern | `reduced` |
| TTY Linux, SSH lama | `mono` |
| Emulator tidak dikenal | `reduced` (cadangan bawaan) |

### Profil menurut ukuran terminal

| Ukuran minimum (kolom × baris) | Batas atas profil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| di bawahnya | `mono` |

Profil akhir adalah **yang lebih ketat dari keduanya** (emulator dan ukuran) — dapat disegarkan langsung dengan tombol `r`.

## 11. Pengujian

```bash
source .venv/bin/activate
lint-imports        # memeriksa Dependency Rule (6 kontrak)
pytest -q           # 186 pengujian
ruff check src tests
mypy -p omega_fold
```

Struktur: `tests/unit/` (domain dan infrastruktur tanpa I/O sungguhan — pengekspor, grafik SVG, markah layar pembuka TUI), `tests/integration/` (sistem berkas sungguhan melalui `tmp_path`, server HTTP tiruan `pytest-httpserver`, basis data SQLite sungguhan, CLI dari awal sampai akhir), `tests/tui/` (navigasi melalui `Pilot`, struktural — tanpa klaim verifikasi visual, lihat `docs/ARCHITECTURE.md` §Antarmuka TUI).

## 12. Di luar cakupan

- Analisis konten/SEO
- Rendering JavaScript di sisi klien
- Crawl tanpa pengaman
- Pemindaian kerentanan aktif, fuzzing, brute force
- Dasbor web

---

> Omega-fold — Memetakan struktur, memeriksa tautannya, tidak pernah menebak apa yang belum dikunjungi.
