<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - MIT लाइसेंस (LICENSE फ़ाइल देखें) -->
<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-fold.png" alt="Omega-Fold" width="512">
</div>

#  OMEGA-FOLD

**साइट/डायरेक्टरी संरचना विश्लेषक (लोकल और रिमोट)**

> [Omega-Server](https://kraynux.snake-mackarel.ts.net) के लिए [kraynux](https://github.com/kraynux) द्वारा निर्मित   

आधिकारिक पेज: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; स्क्रीनशॉट: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-उपयोग)

🌐 इंटरफ़ेस और एक्सपोर्ट की गई रिपोर्टें **17 भाषाओं** में उपलब्ध हैं — देखें [इंटरफ़ेस की भाषाएँ](#इंटरफ़ेस-की-भाषाएँ)।  
**भाषाएँ:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** एक TUI + CLI टूल है जो किसी लोकल डायरेक्टरी या रिमोट साइट (सुरक्षा सीमाओं से बँधी HTTP क्रॉलिंग) की संरचना का विश्लेषण करता है: पूरा ट्री, एक्सटेंशन/फ़ाइल श्रेणी के अनुसार आँकड़े, लिंक का नक्शा (आंतरिक/बाहरी, हर प्रकार के), टूटे लिंक की पहचान। यह `omega-` सुइट का एक टूल है, Clean Architecture में बना — पूरी तकनीकी जानकारी के लिए `docs/ARCHITECTURE.md` देखें।

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/hi/omega-fold/A.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/hi/omega-fold/B.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/hi/omega-fold/C.png" width="24%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/hi/omega-fold/D.png" width="24%" />
</p>

## 1. दृष्टि और दायरा

### Omega-fold क्या करता है

- लोकल डायरेक्टरी स्कैन करता है (असली `os.walk`) या रिमोट साइट को चौड़ाई-पहले (BFS) क्रॉल करता है, सख़्त सुरक्षा सीमाओं के भीतर।
- पूरा ट्री बनाता है (फ़ाइलें/डायरेक्टरी, गहराई, आकार) और उसे श्रेणियों में बाँटता है (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — देखें [§4](#4-फ़ाइल-श्रेणियाँ)।
- हर HTML पेज/फ़ाइल से सभी लिंक (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) निकालता है, उनका वर्गीकरण करता है (आंतरिक निरपेक्ष/सापेक्ष, बाहरी, एंकर, `mailto:`/`tel:`/`javascript:`/`data:`) और जाँचता है कि वे मौजूद हैं — देखें [§5](#5-लिंक-और-जाँच)।
- आँकड़े निकालता है: एक्सटेंशन/श्रेणी के अनुसार बँटवारा, सबसे बड़ी फ़ाइलें, सबसे ज़्यादा बाहरी लिंक वाली फ़ाइलें, सबसे ज़्यादा लिंक किए गए बाहरी डोमेन।
- नतीजे TUI (Textual) या स्क्रिप्ट योग्य CLI में दिखाता है, तीन एक्सपोर्ट के साथ (JSON, टेक्स्ट, 5 थीम वाला HTML)।
- स्कैन का स्थायी इतिहास (SQLite) रखता है, जिसे देखा और दोबारा चलाया जा सकता है।

### Omega-fold क्या नहीं करता

- सामग्री या SEO विश्लेषण (शीर्षक, मेटा विवरण, कीवर्ड घनत्व)।
- बिना सुरक्षा सीमाओं के क्रॉलिंग — गहराई, पेज संख्या और अनुरोधों के बीच का अंतराल हमेशा लागू रहते हैं।
- क्लाइंट-साइड JavaScript रेंडरिंग (पेज वैसा ही लिया जाता है जैसा सर्वर भेजता है, हेडलेस ब्राउज़र में चलाया नहीं जाता)।
- सक्रिय कमज़ोरी स्कैन, फ़ज़िंग, ब्रूट फ़ोर्स।
- वेब डैशबोर्ड।

## 2. इंस्टॉलेशन

### आवश्यकताएँ

- Python 3.10+
- निर्भरताओं के लिए इंटरनेट कनेक्शन
- TUI के लिए: हेडर के आइकन के लिए टर्मिनल में [Nerd Font](https://www.nerdfonts.com/) फ़ॉन्ट इंस्टॉल हो — इसके बिना यह अक्षर खाली डिब्बे की तरह दिखता है (इमोजी जैसी ही सीमा, लेकिन टर्मिनल उपयोगकर्ताओं में यह फ़ॉन्ट कहीं ज़्यादा प्रचलित है)। इसके न होने से काम पर कोई असर नहीं पड़ता, यह केवल दिखावट की बात है।

### इंस्टॉलेशन

```bash
[ -d omega-fold ] && echo "ℹ️ यहाँ पहले से निकाला जा चुका है, यह चरण छोड़ा गया।" || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. वर्चुअल एनवायरनमेंट `.venv` बनाता है, अगर वह पहले से न हो।
2. निर्भरताएँ इंस्टॉल करता है (`vendor/omega-lib/`, फिर `pip install -e .`; `pyproject.toml` ही सत्य का एकमात्र स्रोत रहता है)।
3. `omega-fold.sh` और `install.sh` को चलाने योग्य बनाता है।
4. `~/.bashrc` और `~/.zshrc` में उपनाम `fold` जोड़ता है (पहले से हो तो दोहराता नहीं)।

### निर्भरताएँ

`pyproject.toml` में घोषित (कोई `requirements.txt` नहीं):
- `omega-lib`: सुइट की साझा लाइब्रेरी (एक्सपोर्ट थीम, `ConfidenceLevel`) — `vendor/omega-lib/` में शामिल
- `httpx`: बाहरी लिंक की सिंक्रोनस जाँच (`LinkChecker`)
- `aiohttp`: एसिंक्रोनस HTTP क्रॉलिंग (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: HTML लिंक निकालना
- `jinja2`: HTML एक्सपोर्ट के टेम्पलेट
- विकास निर्भरताएँ (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. उपयोग

### इंटरैक्टिव मोड (TUI)

रोज़मर्रा के उपयोग के लिए अनुशंसित — बिना आर्ग्युमेंट के चलाएँ:

```bash
./omega-fold.sh
```
अगर आपने उपनाम बनाया है, तो टर्मिनल में बस `fold` लिखें:
```bash
fold
```

क्रम: स्वागत स्क्रीन (कोई कुंजी दबाने या क्लिक करने पर बंद) → मुख्य मेनू (स्कैन करें / इतिहास / सेटिंग्स / सहायता) → लक्ष्य, प्रकार (लोकल/रिमोट), मोड (स्थिर/गतिशील) और रिमोट क्रॉलिंग की सुरक्षा सीमाएँ भरना, हर फ़ील्ड पर उसका स्पष्ट लेबल → स्कैन (अनिश्चित प्रगति सूचक, कार्यों का लाइव लॉग, किसी भी समय रद्द करें बटन) → स्कैन का विवरण (श्रेणी और एक्सटेंशन के अनुसार बँटवारा, ट्री, टूटे लिंक, एक्सपोर्ट) → मुख्य मेनू से इतिहास (विवरण देखें, विवरण से गुज़रे बिना **सीधे एक्सपोर्ट**, दोबारा चलाएँ) और सेटिंग्स। टर्मिनल के अनुसार ढलना (रंग, आकार, संरचना का सरलीकरण) अपने आप होता है।

#### कीबोर्ड शॉर्टकट

| कुंजी | क्रिया |
|---|---|
| `↑` / `↓` | स्क्रीन के तत्वों के बीच जाना |
| `Tab` / `Shift+Tab` | फ़ॉर्म के फ़ील्ड के बीच जाना |
| `Esc` | पिछली स्क्रीन पर लौटना (होम स्क्रीन पर बाहर निकलने की पुष्टि) |
| `t` | अगली थीम (तुरंत लागू, बिना पुष्टि) |
| `r` | टर्मिनल पहचान ताज़ा करना |
| `a` | सहायता दिखाना |
| `q` | बाहर निकलना (पुष्टि के साथ) |

### इंटरफ़ेस की भाषाएँ

इंटरफ़ेस 17 भाषाओं में उपलब्ध है: फ़्रेंच, अंग्रेज़ी, स्पेनिश, पुर्तगाली (ब्राज़ील), इतालवी, जर्मन, डच, पोलिश, रूसी, सरलीकृत चीनी, वियतनामी, थाई, इंडोनेशियाई, जापानी, कोरियाई, हिंदी और अरबी। चुनाव सेटिंग्स में होता है (“Langue / Language”) और इंटरफ़ेस दोबारा शुरू होने के बाद लागू होता है; चर `OMEGA_FOLD_LANG` (उदाहरण `OMEGA_FOLD_LANG=hi ./omega-fold.sh`) एक सत्र के लिए भाषा तय कर देता है। omega-suite से चलाने पर omega-fold सुइट की भाषा अपनाता है। Linux टेक्स्ट कंसोल (TTY) पर गैर-लैटिन लिपि वाली भाषाएँ उस सत्र में अंग्रेज़ी में दिखती हैं। कमांड लाइन फ़्रेंच में ही रहती है।

### संपर्क और सहायता

सहायता (`a` कुंजी) में **संपर्क और सहायता** स्क्रीन है: *एक कॉफ़ी पिलाएँ* (डेवलपर का PayPal पेज), *सहायता से संपर्क करें* (ईमेल पता और साइट का संपर्क फ़ॉर्म, साफ़ दिखाए गए), *उपयोगकर्ता के रूप में पंजीकरण करें (अनाम)* और *अपडेट जाँचें*। पंजीकरण स्वैच्छिक है, डिफ़ॉल्ट रूप से बंद है और केवल एक बार भेजा जाता है: इसका उपयोग केवल उपयोगकर्ताओं की गिनती के लिए होता है और, यदि आप चाहें, उनके महाद्वीप या देश के लिए (बंद सूचियाँ, कभी मुक्त पाठ नहीं)। यह एक यादृच्छिक रूप से बनी कुंजी, सॉफ़्टवेयर का नाम (`omega-fold`) और उसका संस्करण भेजता है; कभी कोई नाम, मशीन का नाम, सेटिंग, लक्ष्य या परिणाम नहीं। IP पता पंजीकरणों में सहेजा नहीं जाता, लेकिन हर विज़िट की तरह यह प्राप्त करने वाले सर्वर की सुरक्षा जाँचों और लॉग से होकर गुज़रता है। उसी स्क्रीन से कभी भी वापस लिया जा सकता है (*अब मेरा पंजीकरण न करें*)। अपडेट जाँच केवल साइट पर प्रकाशित संस्करणों की सूची पढ़ती है, और कभी बिना क्लिक के नहीं।

### स्क्रिप्ट मोड (CLI)

कोई भी उप-कमांड CLI मोड चालू कर देता है:

```bash
# लोकल स्कैन (ट्री + आंतरिक लिंक)
./omega-fold.sh scan /var/www/mysite --type local

# गतिशील मोड में लोकल स्कैन (बाहरी लिंक भी HTTP से जाँचता है)
./omega-fold.sh scan /var/www/mysite --type local --mode dynamic

# रिमोट स्कैन (शुरुआती URL से BFS क्रॉलिंग)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# इतिहास (लक्ष्य के अनुसार फ़िल्टर किया जा सकता है)
./omega-fold.sh history --target /var/www/mysite --limit 20

# स्कैन का विवरण (टेक्स्ट, JSON या HTML) — 5 एक्सपोर्ट थीम में से चुनें
./omega-fold.sh show <scan_id> --format html --theme omega-base --output report.html
```

`scan` के विकल्प:

| विकल्प | डिफ़ॉल्ट | प्रभाव |
|---|---|---|
| `--type` | *(अनिवार्य)* | `local` या `distant` (रिमोट) |
| `--mode` | `static` | `static` (बाहरी लिंक नहीं जाँचे जाते) या `dynamic` (HTTP से जाँचे जाते हैं) |
| `--max-depth` | `5` | अधिकतम गहराई जहाँ तक जाया जाता है (रिमोट स्कैन) |
| `--max-pages` | `1000` | क्रॉल किए जाने वाले पेजों की अधिकतम संख्या (रिमोट स्कैन) |
| `--delay` | `100` | दो अनुरोधों के बीच अंतराल (ms) (रिमोट स्कैन) |
| `--user-agent` | `omega-fold/0.1` | भेजा जाने वाला `User-Agent` हेडर (रिमोट स्कैन) |
| `--respect-robots` | बंद | `robots.txt` का पालन करता है (रिमोट स्कैन) |

रिमोट स्कैन में बिना स्कीम वाला लक्ष्य (`example.org`) अपने आप `https://example.org` बन जाता है — इसे लिखने की ज़रूरत नहीं, जब तक आप स्पष्ट रूप से `http://` लागू न करना चाहें।

अगर साइट में `--max-pages` (डिफ़ॉल्ट 1000) से ज़्यादा पेज हैं, तो स्कैन सीमा पर रुक जाता है लेकिन यह साफ़ बताता है: `scan.status` का मान `completed` की जगह `completed_truncated` होता है, और CLI सारांश, TUI की विवरण स्क्रीन और HTML एक्सपोर्ट में एक दिखने वाली चेतावनी होती है — तब बताई गई फ़ाइलों की संख्या साइट का असली आकार नहीं होती; पूरा कवरेज पाने के लिए ज़्यादा `--max-pages` के साथ दोबारा चलाएँ।

अगर उपनाम `install.sh` ने बनाया है, तो `fold scan ...` टर्मिनल में कहीं से भी, `./omega-fold.sh` उपसर्ग के बिना काम करता है।

## 4. फ़ाइल श्रेणियाँ

हर फ़ाइल अपने एक्सटेंशन के अनुसार एक श्रेणी में रखी जाती है (पहला मेल मान्य) — पूरा विवरण और हर एक्सटेंशन की तालिका: `docs/FAMILIES.md`।

| श्रेणी | एक्सटेंशन के उदाहरण |
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
| `other` | बाकी सब |

## 5. लिंक और जाँच

### वर्गीकरण

मिले हर लिंक (`href`/`src`/`action`) का वर्गीकरण इस प्राथमिकता क्रम में होता है:

| प्रकार | कब पहचाना जाता है | उदाहरण |
|---|---|---|
| `empty` | खाली स्ट्रिंग | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | विशेष स्कीम | `mailto:x@y.z` |
| `anchor` | सीधे `#` से शुरू (शुद्ध एंकर) | `#section` |
| `external` | `http://`, `https://` या `//` (प्रोटोकॉल-सापेक्ष) | `https://example.org` |
| `absolute` | `/` से शुरू | `/img/logo.png` |
| `relative` | बाकी सब | `img/logo.png`, `../page.html` |

`absolute` और `relative` **आंतरिक** लिंक के दो रूप हैं — `page.html#section` लिंक `relative` ही रहता है (अंत का फ़्रैगमेंट उसे सिर्फ़ एंकर नहीं बनाता; वह सचमुच किसी दूसरे संसाधन पर ले जाता है)।

### जाँच

- **आंतरिक लिंक**: हमेशा स्कैन के दौरान सचमुच मिले पथों के समूह से मिलाया जाता है (कोई नेटवर्क अनुरोध नहीं) — `absolute` स्कैन की जड़ से हल होता है, विभाजक वाला `relative` स्रोत फ़ाइल की डायरेक्टरी से, और बिना विभाजक वाला `relative` (सिर्फ़ फ़ाइल नाम) पूरे ट्री में खोजा जाता है। रिमोट स्कैन में जाँच क्रॉलिंग पूरी होने के बाद दूसरे चरण में होती है, उन पेजों के समूह से जिन पर सचमुच सफलतापूर्वक जाया गया — सुरक्षा सीमाओं से बाहर या `robots.txt` से रोका गया पेज `unchecked` रहता है, अनुमान से कभी `broken` नहीं।
- **बाहरी लिंक**: केवल `dynamic` मोड में HTTP अनुरोध से जाँचा जाता है (HEAD, और HEAD विफल हो तो GET) — `static` मोड में यह `unchecked` रहता है।

## 6. रिमोट क्रॉलिंग की सुरक्षा सीमाएँ

हमेशा सक्रिय, कभी बंद नहीं की जा सकतीं — केवल उनकी सीमाएँ बदली जा सकती हैं:

- **गहराई** (`--max-depth`): केवल क्रॉल किए जाने वाले नए पेजों को कतार में जोड़ने को सीमित करती है; पहले से देखे गए पेज पर मिले लिंक हमेशा नतीजे में आते हैं, भले ही वे जिस पेज की ओर इशारा करते हैं उस पर आगे न जाया जाए।
- **पेज संख्या** (`--max-pages`): सभी गहराइयों में देखे गए पेजों की कुल संख्या सीमित करती है।
- **अंतराल** (`--delay`): लगातार दो HTTP अनुरोधों के बीच का ठहराव।
- **वही डोमेन**: केवल वे आंतरिक लिंक अपनाए जाते हैं जो शुरुआती URL वाले ही `netloc` पर जाते हैं — यह लिंक के पथ और **रीडायरेक्ट के बाद सचमुच लोड हुए** URL, दोनों पर जाँचा जाता है: ऐसा परमालिंक जिसका पथ आंतरिक फ़ोल्डर जैसा दिखता है (`/go/xyz`, `/public/name/`) पर जो असल में किसी बाहरी डोमेन पर रीडायरेक्ट करता है, कभी स्कैन की जा रही साइट का पेज नहीं माना जाता (उसकी सामग्री आपकी नहीं होगी)।
- **`robots.txt`** (`--respect-robots`): सुरक्षा सीमाओं को कमज़ोर नहीं, बल्कि मज़बूत करता है — वर्जित पेज पर कभी नहीं जाया जाता, उसके बाहरी लिंक `unchecked` रहते हैं।

## 7. आर्किटेक्चर

Omega-fold **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared) में बना है, `omega-` सुइट के ढाँचे के अनुरूप (देखें `omega-scan`/`omega-check`/`omega-deep`), और हर बदलाव पर `import-linter` से जाँचा जाता है। पूरा विवरण **`docs/ARCHITECTURE.md`** में है।

बहुत छोटा सार:

```text
src/omega_fold/
├── domain/          शुद्ध व्यावसायिक तर्क: स्कैन, ट्री (tree), लिंक, आँकड़े, रिपोर्ट
├── application/     उपयोग के मामले (commands/queries) — run_scan (लोकल/रिमोट), export_scan_report...
├── ports/           एप्लिकेशन द्वारा अपेक्षित अनुबंध (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  ठोस कार्यान्वयन (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    Jinja2 एक्सपोर्टर — Textual यहाँ नहीं है)
├── interfaces/      tui/ (Textual) और cli/ (स्क्रिप्ट योग्य), सख़्त कार्यात्मक समानता के साथ
├── app/             जोड़ना (DependencyContainer, bootstrap, जीवन-चक्र)
├── core/, shared/   साझा शब्दावली, गैर-व्यावसायिक उपयोगिताएँ
└── plugins/         ढाँचा तैयार, खाली (कोई पुष्ट विस्तार दिशा नहीं)
```

डिज़ाइन नियम:
- `domain/tree/service.py`: पहले से ज्ञात फ़ाइलों की सपाट सूची को ट्री में जोड़ता है, कभी I/O नहीं करता — असली भ्रमण (`os.walk`) `infrastructure/filesystem/` में है।
- `domain/scans/policies.py`: क्रॉलिंग की सुरक्षा सीमाएँ (गहराई/पेज/डोमेन), बिना नेटवर्क के जाँचने योग्य शुद्ध तर्क।
- `infrastructure/filesystem/` और `infrastructure/network/`: I/O करते हैं (डिस्क, HTTP), कभी निर्णय नहीं देते।
- `infrastructure/exporters/`: पहले से जुड़ा स्कैन नतीजा पढ़ते हैं, कभी कोई आँकड़ा दोबारा नहीं निकालते।
- `infrastructure/storage/sqlite/`: केवल स्रोत डेटा (`scans`/`files`/`links`) रखता है — ट्री और आँकड़े पढ़ते समय उन्हीं शुद्ध फ़ंक्शनों से दोबारा निकाले जाते हैं जो पहले स्कैन में थे (देखें `DECISIONS_ARCHITECTURE.md`, D-011), डेटाबेस में कभी दोहराए नहीं जाते।

## 8. एक्सपोर्ट

टेक्स्ट और HTML रिपोर्टें सेटिंग्स में चुनी गई भाषा में लिखी जाती हैं (“एक्सपोर्ट की भाषा”, डिफ़ॉल्ट रूप से इंटरफ़ेस वाली); JSON डेटा ही रहता है, उसका अनुवाद नहीं होता। रिपोर्टें डिफ़ॉल्ट रूप से `var/exports/` में बनती हैं (रनटाइम पथ प्रोजेक्ट फ़ोल्डर से जुड़ा, बदलने के लिए `$OMEGA_FOLD_VAR_DIR`), या बताए गए पथ (`--output`) पर।

### JSON, सत्य का स्रोत

नतीजे की पूरी संरचना (`Scan` + ट्री + लिंक + आँकड़े), सख़्ती से JSON में बदलने योग्य।

### टेक्स्ट, संक्षिप्त पठनीय रिपोर्ट

सारांश, श्रेणी के अनुसार बँटवारा, ASCII ट्री (6 स्तर की गहराई तक सीमित — टेक्स्ट रिपोर्ट हज़ारों फ़ाइलों का ट्री सूचीबद्ध करने के लिए नहीं है), टूटे लिंक की सूची।

### HTML, स्वतंत्र वेब रिपोर्ट

चुनने के लिए 5 थीम (`--theme`)। साइट का कुल आकार सबसे पहले उभारा जाता है (स्कैन रिपोर्ट का पहला उद्देश्य यही है) और हर जगह — CLI, TUI, एक्सपोर्ट — कच्चे बाइट की जगह पठनीय रूप (KB/MB/GB...) में दिखाया जाता है। अपना लेआउट: कंटेनर, आँकड़ों का ग्रिड, श्रेणी के अनुसार बँटवारे का SVG हिस्टोग्राम (हाथ से बनाया, कोई भारी चार्ट निर्भरता नहीं — `omega-deep` के आर्किटेक्चर आरेख वाली ही तकनीक), एक्सटेंशन/सबसे बड़ी फ़ाइलों की तालिकाएँ। लिंक किए गए बाहरी डोमेन में पहले 20 सीधे दिखते हैं, बाकी एक मोड़ने योग्य पैनल में (सैकड़ों बाहरी रीडायरेक्ट वाली साइट पर उपयोगी); टूटे लिंक की सूची डिफ़ॉल्ट रूप से मुड़ी रहती है।

ट्री मूल **बहु-स्तरीय** HTML में दिखता है: हर डायरेक्टरी के लिए एक `<details>`, डिफ़ॉल्ट रूप से केवल जड़ खुली, हर उप-फ़ोल्डर क्लिक पर अलग से खुलता है (उपयोगकर्ता की एक इंडेक्स बनाने वाली स्क्रिप्ट से प्रेरित) — ब्राउज़र केवल खुली सामग्री को सजाता है, इसलिए दसियों हज़ार फ़ाइलों वाली साइट पर भी यह बिना JavaScript के उपयोगी रहता है।

## 9. इतिहास

हर स्कैन सहेजा जाता है (SQLite, `var/db/omega-fold.db`)। इतिहास लक्ष्य के अनुसार देखा जा सकता है (`omega-fold history --target ...`), पिछले स्कैन का विवरण (`omega-fold show <scan_id>`), या TUI के इतिहास मेनू से (दोबारा चलाना शामिल)।

## 10. टर्मिनल संगतता

TUI (Textual) अपने आप टर्मिनल की क्षमताएँ (एमुलेटर, आकार) पहचानता है और उसके अनुसार अपनी संरचनात्मक स्टाइलशीट बदलता है (`complete`/`standard`/`reduced`/`mono`), बिना किसी मैनुअल विकल्प के। CLI मोड हमेशा सादा टेक्स्ट रहता है, टर्मिनल से स्वतंत्र। यह नीति पूरे `omega-` सुइट में साझा है (`omega-lib`, `terminal/policies.py`)।

### पहचाने गए एमुलेटर के अनुसार प्रोफ़ाइल

| एमुलेटर | प्रारंभिक प्रोफ़ाइल |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, आधुनिक SSH | `reduced` |
| Linux TTY, पुराना SSH | `mono` |
| अपरिचित एमुलेटर | `reduced` (डिफ़ॉल्ट विकल्प) |

### टर्मिनल के आकार के अनुसार प्रोफ़ाइल

| न्यूनतम आकार (कॉलम × पंक्तियाँ) | प्रोफ़ाइल की ऊपरी सीमा |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| इससे कम | `mono` |

अंतिम प्रोफ़ाइल **दोनों में से अधिक प्रतिबंधात्मक** होती है (एमुलेटर और आकार) — `r` कुंजी से तुरंत ताज़ा की जा सकती है।

## 11. परीक्षण

```bash
source .venv/bin/activate
lint-imports        # Dependency Rule जाँचता है (6 अनुबंध)
pytest -q           # 186 परीक्षण
ruff check src tests
mypy -p omega_fold
```

संरचना: `tests/unit/` (बिना असली I/O के डोमेन और इंफ्रास्ट्रक्चर — एक्सपोर्टर, SVG ग्राफ़, TUI स्वागत स्क्रीन का मार्कअप), `tests/integration/` (`tmp_path` से असली फ़ाइल सिस्टम, नकली HTTP सर्वर `pytest-httpserver`, असली SQLite डेटाबेस, शुरू से अंत तक CLI), `tests/tui/` (`Pilot` से नेविगेशन, संरचनात्मक — दृश्य जाँच का कोई स्व-दावा नहीं, देखें `docs/ARCHITECTURE.md` §TUI इंटरफ़ेस)।

## 12. दायरे से बाहर

- सामग्री/SEO विश्लेषण
- क्लाइंट-साइड JavaScript रेंडरिंग
- बिना सुरक्षा सीमाओं के क्रॉलिंग
- सक्रिय कमज़ोरी स्कैन, फ़ज़िंग, ब्रूट फ़ोर्स
- वेब डैशबोर्ड

---

> Omega-fold — संरचना का नक्शा बनाओ, उसके लिंक जाँचो, जो देखा नहीं गया उसका कभी अनुमान मत लगाओ।
