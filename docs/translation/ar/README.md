<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - رخصة MIT (انظر ملف LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**محلّل بنية المواقع والمجلدات (محليًا وعن بُعد)**

> طوّره [kraynux](https://github.com/kraynux) من أجل [Omega-Server](https://kraynux.snake-mackarel.ts.net)   

الصفحة الرسمية: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; لقطات الشاشة: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-الاستخدام)

🌐 الواجهة والتقارير المُصدَّرة متاحة بـ **17 لغة** — انظر [لغات الواجهة](#لغات-الواجهة).  
**اللغات:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](README.md)

---

**Omega-fold** أداة TUI + CLI تحلّل بنية مجلد محلي أو موقع بعيد (زحف HTTP تضبطه حدود أمان): شجرة كاملة، وإحصاءات حسب الامتداد وفئة الملف، وخريطة للروابط (داخلية وخارجية، بكل أنواعها)، وكشف الروابط المعطّلة. هي إحدى أدوات مجموعة `omega-`، مبنية وفق Clean Architecture — انظر `docs/ARCHITECTURE.md` لكل التفاصيل التقنية.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ar/omega-fold/D.png" width="24%" />
</p>

## 1. الرؤية والنطاق

### ما يفعله Omega-fold

- يفحص مجلدًا محليًا (`os.walk` حقيقي) أو يزحف على موقع بعيد بالعرض أولًا (BFS)، ضمن حدود أمان صارمة.
- يبني الشجرة الكاملة (ملفات ومجلدات، العمق، الحجم) ويصنّفها حسب الفئة (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — انظر [§4](#4-فئات-الملفات).
- يستخرج كل الروابط (`<a href>` و`<img src>` و`<script src>` و`<link href>` و`<form action>`) من كل صفحة أو ملف HTML، ويصنّفها (داخلي مطلق/نسبي، خارجي، مرساة، `mailto:`/`tel:`/`javascript:`/`data:`) ويتحقق من وجودها — انظر [§5](#5-الروابط-والتحقق).
- يحسب الإحصاءات: التوزيع حسب الامتداد والفئة، وأكبر الملفات، والملفات ذات أكثر الروابط الصادرة، والنطاقات الخارجية الأكثر ربطًا.
- يعرض النتيجة في TUI (Textual) أو في CLI قابل للبرمجة النصية، مع ثلاثة أنواع من التصدير (JSON، ونص، وHTML بخمس سمات).
- يحتفظ بسجل دائم للفحوص (SQLite) يمكن تصفّحه وإعادة تشغيله.

### ما لا يفعله Omega-fold

- تحليل المحتوى أو تحسين محركات البحث (العناوين، والأوصاف الوصفية، وكثافة الكلمات المفتاحية).
- الزحف بلا حدود أمان — العمق وعدد الصفحات والمهلة بين الطلبات مفعّلة دائمًا.
- عرض JavaScript من جهة العميل (تُجلب الصفحة كما يرسلها الخادم، ولا تُنفَّذ في متصفح بلا واجهة).
- فحص الثغرات النشط، والتشويش (fuzzing)، والتخمين بالقوة الغاشمة.
- لوحة تحكم ويب.

## 2. التثبيت

### المتطلبات

- Python 3.10+
- اتصال بالإنترنت، من أجل الاعتماديات
- لواجهة TUI: خط [Nerd Font](https://www.nerdfonts.com/) مثبّت في الطرفية، من أجل أيقونة الترويسة — من دونه يظهر هذا الحرف مربعًا فارغًا (القيد نفسه الذي يواجه الرموز التعبيرية، لكنه أكثر انتشارًا بكثير بين مستخدمي الطرفية). غيابه لا يؤثر في العمل، فهو أمر شكلي بحت.

### التثبيت

```bash
[ -d omega-fold ] && echo "ℹ️ مُستخرَج هنا مسبقًا، تم تخطي الخطوة." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. ينشئ البيئة الافتراضية `.venv` إن لم تكن موجودة.
2. يثبّت الاعتماديات (`vendor/omega-lib/` ثم `pip install -e .`؛ ويبقى `pyproject.toml` المرجع الوحيد).
3. يجعل `omega-fold.sh` و`install.sh` قابلين للتنفيذ.
4. يضيف الاسم المستعار `fold` إلى `~/.bashrc` و`~/.zshrc` (من دون تكرار إن كان موجودًا).

### الاعتماديات

مُعرَّفة في `pyproject.toml` (لا يوجد `requirements.txt`):
- `omega-lib`: المكتبة المشتركة للمجموعة (سمات التصدير، `ConfidenceLevel`) — مضمّنة في `vendor/omega-lib/`
- `httpx`: التحقق المتزامن من الروابط الخارجية (`LinkChecker`)
- `aiohttp`: زحف HTTP غير متزامن (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: استخراج روابط HTML
- `jinja2`: قوالب تصدير HTML
- اعتماديات التطوير (`pip install -e ".[dev]"`): `pytest` و`pytest-asyncio` و`pytest-cov` و`pytest-httpserver` و`ruff` و`mypy` و`import-linter`

## 3. الاستخدام

### الوضع التفاعلي (TUI)

يُنصح به للاستخدام اليومي — يُشغَّل من دون وسائط:

```bash
./omega-fold.sh
```
إن أنشأت الاسم المستعار، فاكتب `fold` فقط في الطرفية:
```bash
fold
```

المسار: شاشة البداية (تُغلق بضغطة مفتاح أو نقرة) ← القائمة الرئيسية (فحص / السجل / الإعدادات / مساعدة) ← إدخال الهدف، والنوع (محلي/بعيد)، والوضع (ثابت/ديناميكي)، وحدود أمان الزحف البعيد، ولكل حقل تسميته الواضحة ← الفحص (مؤشر تقدّم غير محدد، وسجل مباشر للعمليات، وزر إلغاء متاح في أي وقت) ← تفاصيل الفحص (التوزيع حسب الفئة والامتداد، والشجرة، والروابط المعطّلة، والتصدير) ← السجل (عرض التفاصيل، و**التصدير مباشرة** دون المرور بالتفاصيل، وإعادة التشغيل) والإعدادات من القائمة الرئيسية. التكيّف مع الطرفية (الألوان، والحجم، وتبسيط البنية) تلقائي.

#### اختصارات لوحة المفاتيح

| المفتاح | الإجراء |
|---|---|
| `↑` / `↓` | التنقل بين عناصر الشاشة |
| `Tab` / `Shift+Tab` | التنقل بين حقول النموذج |
| `Esc` | العودة إلى الشاشة السابقة (تأكيد الخروج في الشاشة الرئيسية) |
| `t` | السمة التالية (تُطبَّق فورًا دون تأكيد) |
| `r` | تحديث اكتشاف الطرفية |
| `a` | عرض المساعدة |
| `q` | الخروج (مع تأكيد) |

### لغات الواجهة

الواجهة متاحة بـ 17 لغة: الفرنسية، والإنجليزية، والإسبانية، والبرتغالية (البرازيل)، والإيطالية، والألمانية، والهولندية، والبولندية، والروسية، والصينية المبسّطة، والفيتنامية، والتايلاندية، والإندونيسية، واليابانية، والكورية، والهندية، والعربية. يتم الاختيار من الإعدادات («Langue / Language») ويسري بعد إعادة تشغيل الواجهة؛ ويفرض المتغير `OMEGA_FOLD_LANG` (مثلًا `OMEGA_FOLD_LANG=ar ./omega-fold.sh`) لغة طوال جلسة واحدة. عند التشغيل من omega-suite، يأخذ omega-fold لغة المجموعة. على وحدة التحكم النصية في Linux ‏(TTY)، تُعرض اللغات ذات الكتابة غير اللاتينية بالإنجليزية طوال الجلسة. يبقى سطر الأوامر بالفرنسية.

### التواصل والدعم

تتيح المساعدة (المفتاح `a`) شاشة **التواصل والدعم**: *ادفع ثمن قهوة* (صفحة PayPal الخاصة بالمطوّر)، و*التواصل مع الدعم* (عنوان البريد الإلكتروني ونموذج التواصل في الموقع، معروضان بوضوح)، و*تسجيلي كمستخدم (مجهول الهوية)* و*التحقق من التحديثات*. التسجيل اختياري، ومعطّل افتراضيًا، ويُرسل مرة واحدة فقط: يُستخدم فقط لإحصاء المستخدمين، وإن رغبت، قارتهم أو بلدهم (قوائم مغلقة، دون أي نص حر). يُرسل مفتاحًا مولَّدًا عشوائيًا واسم البرنامج (`omega-fold`) وإصداره؛ ولا يُرسل أبدًا اسمًا أو اسم جهاز أو إعدادًا أو هدفًا أو نتيجة. لا يُحفظ عنوان IP في التسجيلات، لكنه، كأي زيارة، يمر عبر فحوص الأمان وسجل الخادم المستقبِل. يمكن السحب في أي وقت من الشاشة نفسها (*إلغاء تسجيلي*). يقرأ التحقق من التحديثات قائمة الإصدارات المنشورة على الموقع فقط، ولا يحدث أبدًا دون نقرة.

### وضع البرمجة النصية (CLI)

أي أمر فرعي يفعّل وضع CLI:

```bash
# فحص محلي (الشجرة + الروابط الداخلية)
./omega-fold.sh scan /var/www/mysite --type local

# فحص محلي في الوضع الديناميكي (يتحقق أيضًا من الروابط الخارجية عبر HTTP)
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# فحص بعيد (زحف BFS من عنوان URL البداية)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# السجل (قابل للتصفية حسب الهدف)
./omega-fold.sh history --target /var/www/mysite --limit 20

# تفاصيل فحص (نص أو JSON أو HTML) — اختيار من 5 سمات للتصدير
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

خيارات `scan`:

| الخيار | الافتراضي | الأثر |
|---|---|---|
| `--type` | *(إلزامي)* | `local` أو `distant` (بعيد) |
| `--mode` | `static` | `static` (لا يُتحقق من الروابط الخارجية) أو `dynamic` (يُتحقق منها عبر HTTP) |
| `--max-depth` | `5` | أقصى عمق يُتتبَّع (فحص بعيد) |
| `--max-pages` | `1000` | أقصى عدد من الصفحات يُزحف عليها (فحص بعيد) |
| `--delay` | `100` | المهلة (مللي ثانية) بين طلبين (فحص بعيد) |
| `--user-agent` | `omega-fold/0.1` | ترويسة `User-Agent` المُرسلة (فحص بعيد) |
| `--respect-robots` | معطّل | يحترم `robots.txt` (فحص بعيد) |

في الفحص البعيد، يُكمَّل الهدف الذي لا يحمل مخططًا (`example.org`) تلقائيًا إلى `https://example.org` — لا داعي لكتابته إلا لفرض `http://` صراحةً.

إذا كان في الموقع صفحات أكثر من `--max-pages` (1000 افتراضيًا)، يتوقف الفحص عند الحد لكنه يصرّح بذلك: تكون قيمة `scan.status` هي `completed_truncated` بدلًا من `completed`، مع تحذير ظاهر في ملخص CLI وشاشة التفاصيل في TUI وتصدير HTML — ولا يكون عدد الملفات المُبلَّغ عنه حينها هو الحجم الحقيقي للموقع؛ أعد التشغيل بقيمة `--max-pages` أعلى لتغطية كاملة.

إذا أنشأ `install.sh` الاسم المستعار، فإن `fold scan ...` يعمل من أي مكان في الطرفية، دون البادئة `./omega-fold.sh`.

## 4. فئات الملفات

يُصنَّف كل ملف في فئة حسب امتداده (أول تطابق هو الفائز) — التفاصيل الكاملة وجدول لكل امتداد: `docs/FAMILIES.md`.

| الفئة | أمثلة على الامتدادات |
|---|---|
| `images` | `.jpg`، `.png`، `.svg`، `.webp`، `.ico`... |
| `documents` | `.pdf`، `.doc`، `.xlsx`، `.odt`... |
| `code` | `.html`، `.php`، `.js`، `.ts`، `.py`، `.css`... |
| `data` | `.json`، `.xml`، `.yaml`، `.csv`، `.sql`... |
| `archives` | `.zip`، `.tar`، `.gz`، `.7z`... |
| `fonts` | `.ttf`، `.otf`، `.woff`، `.woff2`... |
| `video` | `.mp4`، `.webm`، `.mkv`... |
| `audio` | `.mp3`، `.wav`، `.flac`... |
| `text` | `.txt`، `.md`، `.rst`، `.log` |
| `other` | كل ما تبقّى |

## 5. الروابط والتحقق

### التصنيف

يُصنَّف كل رابط يُعثر عليه (`href`/`src`/`action`) وفق ترتيب الأولوية التالي:

| النوع | يُعرَف عندما | مثال |
|---|---|---|
| `empty` | سلسلة فارغة | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | مخطط خاص | `mailto:x@y.z` |
| `anchor` | يبدأ مباشرة بـ `#` (مرساة خالصة) | `#section` |
| `external` | `http://` أو `https://` أو `//` (نسبي إلى البروتوكول) | `https://example.org` |
| `absolute` | يبدأ بـ `/` | `/img/logo.png` |
| `relative` | كل ما تبقّى | `img/logo.png`، `../page.html` |

`absolute` و`relative` هما شكلا الرابط **الداخلي** — يبقى الرابط `page.html#section` من نوع `relative` (الجزء الأخير لا يجعله مجرد مرساة، فهو ينقل فعلًا إلى مورد آخر).

### التحقق

- **الرابط الداخلي**: يُطابَق دائمًا مع مجموعة المسارات التي عُثر عليها فعلًا أثناء الفحص (دون أي طلب شبكي) — يُحلّ `absolute` انطلاقًا من جذر الفحص، و`relative` الذي يحتوي فاصلًا انطلاقًا من مجلد الملف المصدر، ويُبحث عن `relative` الخالي من الفاصل (اسم ملف فقط) في الشجرة كلها. في الفحص البعيد، يجري التحقق في مرور ثانٍ بعد انتهاء الزحف، مقابل مجموعة الصفحات التي زيرت بنجاح فعلًا — تبقى الصفحة الواقعة خارج حدود الأمان أو المحجوبة بـ `robots.txt` بحالة `unchecked`، ولا تُعدّ `broken` بالتخمين أبدًا.
- **الرابط الخارجي**: يُتحقق منه بطلب HTTP (‏HEAD ثم GET إن فشل HEAD) في الوضع `dynamic` فقط — وفي الوضع `static` يبقى `unchecked`.

## 6. حدود أمان الزحف البعيد

مفعّلة دائمًا ولا يمكن تعطيلها — لا يُعدَّل إلا عتباتها:

- **العمق** (`--max-depth`): يحدّ فقط من إضافة صفحات جديدة إلى طابور الزحف؛ أما الروابط الموجودة في صفحة سبقت زيارتها فتظهر دائمًا في النتيجة، حتى لو لم تُتتبَّع الصفحة التي تشير إليها.
- **عدد الصفحات** (`--max-pages`): يحدّ من العدد الإجمالي للصفحات المزورة في كل الأعماق.
- **المهلة** (`--delay`): استراحة بين طلبي HTTP متتاليين.
- **النطاق نفسه**: لا تُتتبَّع إلا الروابط الداخلية المتجهة إلى `netloc` نفسه الخاص بعنوان URL البداية — ويُتحقق من ذلك في مسار الرابط وفي عنوان URL **المحمَّل فعلًا بعد إعادة التوجيه**: الرابط الدائم الذي يبدو مساره مجلدًا داخليًا (`/go/xyz`، `/public/name/`) لكنه يعيد التوجيه فعليًا إلى نطاق خارجي لا يُعامَل أبدًا كصفحة من الموقع المفحوص (فمحتواه ليس محتواك).
- **`robots.txt`** (`--respect-robots`): يعزّز حدود الأمان بدلًا من إضعافها — لا تُزار الصفحة المحظورة أبدًا، وتبقى روابطها الصادرة `unchecked`.

## 7. البنية المعمارية

بُني Omega-fold وفق **Clean Architecture** ‏(domain / application / infrastructure / interfaces / ports / core / app / plugins / shared)، بما يتّسق مع قالب مجموعة `omega-` (انظر `omega-scan`/`omega-check`/`omega-deep`)، ويتحقق منها `import-linter` عند كل تعديل. التفاصيل الكاملة في **`docs/ARCHITECTURE.md`**.

نظرة عامة قصيرة جدًا:

```text
src/omega_fold/
├── domain/          منطق أعمال خالص: الفحوص، والشجرة (tree)، والروابط، والإحصاءات، والتقارير
├── application/     حالات الاستخدام (commands/queries) — run_scan (محلي/بعيد)، export_scan_report...
├── ports/           العقود التي يتوقعها التطبيق (local_fs_reader، distant_crawler،
│                    html_link_extractor، link_checker، scan_repository، report_exporter...)
├── infrastructure/  تنفيذات فعلية (os.walk، aiohttp، httpx، BeautifulSoup، SQLite،
│                    مُصدِّرات Jinja2 — Textual ليس هنا)
├── interfaces/      tui/ ‏(Textual) وcli/ (قابل للبرمجة النصية)، بتكافؤ وظيفي صارم
├── app/             التجميع (DependencyContainer، bootstrap، دورة الحياة)
├── core/, shared/   مفردات مشتركة، وأدوات مساعدة خارج منطق الأعمال
└── plugins/         البنية جاهزة، فارغة (لا يوجد محور توسعة مؤكد)
```

قواعد التصميم:
- `domain/tree/service.py`: يجمع قائمة مسطّحة معروفة من الملفات في شجرة، ولا يقوم أبدًا بعمليات إدخال/إخراج — الاستعراض الفعلي (`os.walk`) يوجد في `infrastructure/filesystem/`.
- `domain/scans/policies.py`: حدود أمان الزحف (العمق/الصفحات/النطاق)، منطق خالص قابل للاختبار دون شبكة.
- `infrastructure/filesystem/` و`infrastructure/network/`: ينفّذان الإدخال/الإخراج (القرص، HTTP)، ولا يُصدران أحكامًا أبدًا.
- `infrastructure/exporters/`: تقرأ نتيجة الفحص المجمّعة مسبقًا، ولا تعيد حساب أي إحصاء أبدًا.
- `infrastructure/storage/sqlite/`: لا يخزّن إلا البيانات المصدرية (`scans`/`files`/`links`) — تُعاد حساب الشجرة والإحصاءات عند القراءة بالدوال الخالصة نفسها المستخدمة في الفحص الأول (انظر `DECISIONS_ARCHITECTURE.md`، D-011)، ولا تُكرَّر في قاعدة البيانات أبدًا.

## 8. التصدير

تُكتب التقارير النصية وتقارير HTML باللغة المختارة في الإعدادات («لغة التصدير»، وهي افتراضيًا لغة الواجهة)؛ ويبقى JSON بيانات لا تُترجم. تُنشأ التقارير افتراضيًا في `var/exports/` (مسار تشغيل مرتبط بمجلد المشروع، و`$OMEGA_FOLD_VAR_DIR` لتغييره)، أو في المسار المحدد (`--output`).

### JSON، المرجع

البنية الكاملة للنتيجة (`Scan` + الشجرة + الروابط + الإحصاءات)، قابلة للتسلسل إلى JSON بصرامة.

### النص، تقرير مقروء موجز

ملخص، وتوزيع حسب الفئة، وشجرة ASCII (محدودة بستة مستويات عمق — فالتقرير النصي ليس مخصصًا لسرد شجرة من آلاف الملفات)، وقائمة الروابط المعطّلة.

### HTML، تقرير ويب مستقل

خمس سمات للاختيار (`--theme`). يُبرَز الحجم الإجمالي للموقع أولًا (فهو الهدف الأول لتقرير الفحص) ويُعرض بصيغة مقروءة (KB/MB/GB...) في كل مكان — CLI وTUI والتصدير — بدلًا من البايتات الخام. تخطيط خاص: حاوية، وشبكة إحصاءات، ومخطط SVG بياني للتوزيع حسب الفئة (مرسوم يدويًا، دون اعتماد ثقيل على مكتبات الرسوم — التقنية نفسها المستخدمة في مخطط البنية المعمارية لـ `omega-deep`)، وجداول الامتدادات وأكبر الملفات. تُعرض أول 20 من النطاقات الخارجية المرتبطة مباشرة، والباقي في لوحة قابلة للطي (مفيد لموقع فيه مئات من عمليات إعادة التوجيه الخارجية)؛ وقائمة الروابط المعطّلة مطويّة افتراضيًا.

تُعرض الشجرة بـ HTML أصلي **متعدد المستويات**: عنصر `<details>` لكل مجلد، والجذر وحده مفتوح افتراضيًا، وكل مجلد فرعي يُفتح مستقلًا بالنقر (مستوحى من نص برمجي لدى المستخدم لتوليد الفهارس) — لا يرتّب المتصفح إلا المحتوى المفتوح، لذا يبقى قابلًا للاستخدام حتى لموقع فيه عشرات الآلاف من الملفات، دون JavaScript.

## 9. السجل

يُحفظ كل فحص (SQLite، `var/db/omega-fold.db`). يمكن تصفّح السجل حسب الهدف (`omega-fold history --target ...`)، أو عرض تفاصيل فحص سابق (`omega-fold show <scan_id>`)، أو من قائمة السجل في TUI (بما في ذلك إعادة التشغيل).

## 10. التوافق مع الطرفيات

تكتشف واجهة TUI ‏(Textual) قدرات الطرفية تلقائيًا (المحاكي، والحجم) وتكيّف ورقة أنماطها البنيوية وفقًا لذلك (`complete`/`standard`/`reduced`/`mono`)، دون أي خيار يدوي. يبقى وضع CLI نصًا بسيطًا دائمًا، مستقلًا عن الطرفية. وهي سياسة تتشاركها مجموعة `omega-` كلها (`omega-lib`، `terminal/policies.py`).

### الملف الشخصي حسب المحاكي المكتشَف

| المحاكي | الملف الشخصي الأولي |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm، urxvt، SSH حديث | `reduced` |
| TTY في Linux، SSH قديم | `mono` |
| محاكٍ غير معروف | `reduced` (البديل الافتراضي) |

### الملف الشخصي حسب حجم الطرفية

| الحجم الأدنى (أعمدة × أسطر) | سقف الملف الشخصي |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| أقل من ذلك | `mono` |

الملف الشخصي النهائي هو **الأكثر تقييدًا بين الاثنين** (المحاكي والحجم) — ويمكن تحديثه مباشرة بالمفتاح `r`.

## 11. الاختبارات

```bash
source .venv/bin/activate
lint-imports        # يتحقق من Dependency Rule (6 عقود)
pytest -q           # 186 اختبارًا
ruff check src tests
mypy -p omega_fold
```

البنية: `tests/unit/` (النطاق والبنية التحتية دون إدخال/إخراج حقيقي — المُصدِّرات، والرسم البياني SVG، وترميز شاشة بداية TUI)، و`tests/integration/` (نظام ملفات حقيقي عبر `tmp_path`، وخادم HTTP وهمي `pytest-httpserver`، وقاعدة بيانات SQLite حقيقية، وCLI من البداية إلى النهاية)، و`tests/tui/` (التنقل عبر `Pilot`، اختبارات بنيوية — دون ادعاء تحقق بصري ذاتي، انظر `docs/ARCHITECTURE.md` §واجهة TUI).

## 12. خارج النطاق

- تحليل المحتوى/تحسين محركات البحث
- عرض JavaScript من جهة العميل
- الزحف بلا حدود أمان
- فحص الثغرات النشط، والتشويش، والقوة الغاشمة
- لوحة تحكم ويب

---

> Omega-fold — ارسم خريطة البنية، وتحقق من روابطها، ولا تخمّن أبدًا ما لم تتم زيارته.
