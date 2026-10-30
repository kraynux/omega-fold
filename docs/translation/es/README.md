<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (ver el archivo LICENSE) -->
<div align="center">
  <img src="../../assets/omega-fold.png" alt="Omega-Fold" width="384">
</div>

#  OMEGA-FOLD

**Analizador de estructura de sitios/directorios (local y remoto)**

> Desarrollado por **kraynux** para **Omega-server** 
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Capturas: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-uso)

🌐 Interfaz e informes exportados disponibles en **17 idiomas** — ver [Idiomas de la interfaz](#idiomas-de-la-interfaz).  
**Idiomas:**  
<img src="https://flagcdn.com/w20/fr.png" alt="Français" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**Omega-fold** es una herramienta TUI + CLI que analiza la estructura de un directorio local o de un sitio remoto (rastreo HTTP limitado por salvaguardas): árbol completo, estadísticas por extensión/familia de archivo, mapa de enlaces (internos/externos, de todo tipo), detección de enlaces rotos. Herramienta de la suite `omega-`, estructurada en Clean Architecture — ver `docs/ARCHITECTURE.md` para todos los detalles técnicos.

## 1. Visión y alcance

### Lo que hace Omega-fold

- Escanea un directorio local (`os.walk` real) o rastrea un sitio remoto en anchura (BFS), limitado por salvaguardas estrictas.
- Construye el árbol completo (archivos/directorios, profundidad, tamaño) y lo clasifica por familia (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — ver [§4](#4-familias-de-archivos).
- Extrae todos los enlaces (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) de cada página/archivo HTML, los clasifica (interno absoluto/relativo, externo, ancla, `mailto:`/`tel:`/`javascript:`/`data:`) y comprueba que existen — ver [§5](#5-enlaces-y-comprobación).
- Calcula estadísticas: reparto por extensión/familia, archivos más grandes, archivos con más enlaces salientes, dominios externos más enlazados.
- Presenta el resultado en TUI (Textual) o en CLI scriptable, con tres exportaciones (JSON, texto, HTML con 5 temas).
- Conserva un historial persistente de escaneos (SQLite), consultable y repetible.

### Lo que Omega-fold no hace

- Análisis de contenido o de SEO (títulos, meta descripciones, densidad de palabras clave).
- Rastreo sin salvaguardas — profundidad, número de páginas y retardo entre peticiones siempre activos.
- Renderizado de JavaScript del lado del cliente (la página se obtiene tal como se sirve, no se ejecuta en un navegador headless).
- Escaneo activo de vulnerabilidades, fuzzing, fuerza bruta.
- Panel web.

## 2. Instalación

### Requisitos

- Python 3.10+
- Conexión a Internet, para las dependencias
- Para la TUI: una fuente [Nerd Font](https://www.nerdfonts.com/) instalada en el terminal, para el icono de la cabecera — sin ella, ese carácter se muestra como un cuadro vacío (misma limitación que un emoji, pero mucho más disponible entre los usuarios de terminal). Su ausencia no afecta al funcionamiento; es puramente estética.

### Instalación

```bash
[ -d omega-fold ] && echo "ℹ️ Ya extraído aquí, paso omitido." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si aún no existe.
2. Instala las dependencias (`vendor/omega-lib/` y luego `pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-fold.sh` e `install.sh`.
4. Añade el alias `fold` a `~/.bashrc` y `~/.zshrc` (sin duplicado si ya está presente).

### Dependencias

Declaradas en `pyproject.toml` (sin `requirements.txt`):
- `omega-lib`: biblioteca compartida de la suite (temas de exportación, `ConfidenceLevel`) — incluida en `vendor/omega-lib/`
- `httpx`: comprobación síncrona de los enlaces externos (`LinkChecker`)
- `aiohttp`: rastreo HTTP asíncrono (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: extracción de enlaces HTML
- `jinja2`: plantillas para la exportación HTML
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario — se lanza sin argumentos:

```bash
./omega-fold.sh
```
si ha creado el alias, escriba simplemente `fold` en el terminal:
```bash
fold
```

Recorrido: pantalla de inicio (se cierra con una tecla o un clic) → menú principal (Escanear / Historial / Ajustes / Ayuda) → introducción del objetivo, del tipo (local/remoto), del modo (estático/dinámico) y de las salvaguardas del rastreo remoto, cada campo con su etiqueta explícita → escaneo (indicador indeterminado, registro de operaciones en directo, botón Cancelar en todo momento) → detalle del escaneo (reparto por familia y por extensión, árbol, enlaces rotos, exportación) → historial (ver detalle, **exportar directamente** sin pasar por el detalle, repetir) y ajustes desde el menú principal. La adaptación al terminal (colores, tamaño, degradación estructural) es automática.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Moverse entre los elementos de una pantalla |
| `Tab` / `Mayús+Tab` | Moverse entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Tema siguiente (aplicado de inmediato, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir (con confirmación) |

### Idiomas de la interfaz

La interfaz está disponible en 17 idiomas: francés, inglés, español, portugués (Brasil), italiano, alemán, neerlandés, polaco, ruso, chino simplificado, vietnamita, tailandés, indonesio, japonés, coreano, hindi y árabe. La elección se hace en Ajustes («Langue / Language») y se aplica tras reiniciar la interfaz; la variable `OMEGA_FOLD_LANG` (por ejemplo `OMEGA_FOLD_LANG=es ./omega-fold.sh`) fuerza un idioma durante una sesión. Lanzado desde omega-suite, omega-fold adopta el idioma de la suite. En una consola de texto Linux (TTY), los idiomas de escritura no latina se muestran en inglés durante la sesión. La línea de comandos sigue en francés.

### Modo scriptable (CLI)

Cualquier subcomando activa el modo CLI:

```bash
# Escaneo local (árbol + enlaces internos)
./omega-fold.sh scan /var/www/misitio --type local

# Escaneo local en modo dinámico (comprueba también los enlaces externos por HTTP)
./omega-fold.sh scan /var/www/misitio --type local --mode dynamic

# Escaneo remoto (rastreo BFS desde la URL de partida)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Historial (filtrable por objetivo)
./omega-fold.sh history --target /var/www/misitio --limit 20

# Detalle de un escaneo (texto, JSON o HTML) — 5 temas de exportación a elegir
./omega-fold.sh show <scan_id> --format html --theme omega-base --output informe.html
```

Opciones de `scan`:

| Opción | Por defecto | Efecto |
|---|---|---|
| `--type` | *(obligatorio)* | `local` o `distant` (remoto) |
| `--mode` | `static` | `static` (enlaces externos sin comprobar) o `dynamic` (comprobados por HTTP) |
| `--max-depth` | `5` | Profundidad máxima seguida (escaneo remoto) |
| `--max-pages` | `1000` | Número máximo de páginas rastreadas (escaneo remoto) |
| `--delay` | `100` | Retardo (ms) entre dos peticiones (escaneo remoto) |
| `--user-agent` | `omega-fold/0.1` | Cabecera `User-Agent` enviada (escaneo remoto) |
| `--respect-robots` | desactivado | Respeta `robots.txt` (escaneo remoto) |

En un escaneo remoto, un objetivo sin esquema (`example.org`) se completa automáticamente como `https://example.org` — no hace falta indicarlo salvo para forzar `http://` explícitamente.

Si el sitio tiene más páginas que `--max-pages` (1000 por defecto), el escaneo se detiene en el límite pero lo indica explícitamente: `scan.status` vale `completed_truncated` en lugar de `completed`, con un aviso visible en el resumen CLI, la pantalla de detalle de la TUI y la exportación HTML — el número de archivos indicado no es entonces el tamaño real del sitio; vuelva a lanzarlo con un `--max-pages` más alto para una cobertura completa.

Si `install.sh` creó el alias, `fold scan ...` funciona desde cualquier lugar del terminal, sin el prefijo `./omega-fold.sh`.

## 4. Familias de archivos

Cada archivo se clasifica en una familia según su extensión (gana la primera coincidencia) — detalle completo y tabla extensión por extensión: `docs/FAMILIES.md`.

| Familia | Ejemplos de extensiones |
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
| `other` | todo lo demás |

## 5. Enlaces y comprobación

### Clasificación

Cada enlace encontrado (`href`/`src`/`action`) se clasifica, en este orden de prioridad:

| Tipo | Reconocido cuando | Ejemplo |
|---|---|---|
| `empty` | Cadena vacía | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Esquema especial | `mailto:x@y.z` |
| `anchor` | Empieza directamente por `#` (ancla pura) | `#section` |
| `external` | `http://`, `https://` o `//` (relativo al protocolo) | `https://example.org` |
| `absolute` | Empieza por `/` | `/img/logo.png` |
| `relative` | Todo lo demás | `img/logo.png`, `../page.html` |

`absolute` y `relative` son las dos formas de un enlace **interno** — un enlace `page.html#section` sigue siendo `relative` (el fragmento final no lo convierte en una simple ancla; navega realmente hacia otro recurso).

### Comprobación

- **Enlace interno**: siempre se comprueba contra el conjunto de rutas realmente encontradas durante el escaneo (sin petición de red) — `absolute` resuelto contra la raíz del escaneo, `relative` con separador resuelto contra el directorio del archivo de origen, `relative` sin separador (solo nombre de archivo) buscado en todo el árbol. En un escaneo remoto, la comprobación se hace en una segunda pasada una vez terminado el rastreo, contra el conjunto de páginas realmente visitadas con éxito — una página fuera de las salvaguardas o bloqueada por `robots.txt` queda `unchecked`, nunca `broken` por suposición.
- **Enlace externo**: comprobado mediante una petición HTTP (HEAD y luego GET si HEAD falla) solo en modo `dynamic` — en modo `static`, queda `unchecked`.

## 6. Salvaguardas del rastreo remoto

Siempre activas, nunca desactivables — solo sus umbrales son ajustables:

- **Profundidad** (`--max-depth`): limita únicamente la puesta en cola de nuevas páginas por rastrear; los enlaces encontrados en una página ya visitada siempre se indican en el resultado, aunque la página a la que apuntan no se vaya a seguir.
- **Número de páginas** (`--max-pages`): limita el número total de páginas visitadas, en todas las profundidades.
- **Retardo** (`--delay`): pausa entre dos peticiones HTTP consecutivas.
- **Mismo dominio**: solo se siguen los enlaces internos hacia el mismo `netloc` que la URL de partida — comprobado tanto en la ruta del enlace como en la URL **realmente cargada tras la redirección**: un enlace permanente cuya ruta parece una carpeta interna (`/go/xyz`, `/public/nombre/`) pero que en realidad redirige a un dominio externo nunca se trata como una página del sitio escaneado (su contenido no sería el suyo).
- **`robots.txt`** (`--respect-robots`): refuerza las salvaguardas en lugar de debilitarlas — una página prohibida nunca se visita, sus enlaces salientes quedan `unchecked`.

## 7. Arquitectura

Omega-fold está estructurado en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineada con la plantilla de la suite `omega-` (ver `omega-scan`/`omega-check`/`omega-deep`) y verificada por `import-linter` en cada cambio. Todos los detalles están en **`docs/ARCHITECTURE.md`**.

Vista general muy breve:

```text
src/omega_fold/
├── domain/          Lógica de negocio pura: escaneos, árbol (tree), enlaces, estadísticas, informes
├── application/     Casos de uso (commands/queries) — run_scan (local/remoto), export_scan_report...
├── ports/           Contratos que espera la aplicación (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implementaciones concretas (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    exportadores Jinja2 — Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (scriptable), con paridad funcional estricta
├── app/             Ensamblaje (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulario transversal, utilidades no de negocio
└── plugins/         Estructura preparada, vacía (ningún eje de extensión confirmado)
```

Reglas de diseño:
- `domain/tree/service.py`: agrega en un árbol una lista plana de archivos ya conocida, nunca hace E/S — el recorrido real (`os.walk`) vive en `infrastructure/filesystem/`.
- `domain/scans/policies.py`: salvaguardas de rastreo (profundidad/páginas/dominio), lógica pura comprobable sin red.
- `infrastructure/filesystem/` e `infrastructure/network/`: hacen la E/S (disco, HTTP), nunca juzgan.
- `infrastructure/exporters/`: leen el resultado del escaneo ya ensamblado, nunca recalculan una estadística.
- `infrastructure/storage/sqlite/`: solo almacena los datos de origen (`scans`/`files`/`links`) — el árbol y las estadísticas se recalculan al leer con las mismas funciones puras que el escaneo inicial (ver `DECISIONS_ARCHITECTURE.md`, D-011), nunca se duplican en la base.

## 8. Exportaciones

Los informes de texto y HTML se escriben en el idioma elegido en Ajustes («Idioma de las exportaciones», por defecto el de la interfaz); el JSON sigue siendo un dato, sin traducir. Los informes se generan por defecto en `var/exports/` (ruta de ejecución anclada en la carpeta del proyecto, `$OMEGA_FOLD_VAR_DIR` para cambiarla), o en la ruta indicada (`--output`).

### JSON, fuente de verdad

Estructura completa del resultado (`Scan` + árbol + enlaces + estadísticas), estrictamente serializable en JSON.

### Texto, informe legible compacto

Resumen, reparto por familia, árbol ASCII (limitado a 6 niveles de profundidad — un informe de texto no está pensado para listar un árbol de miles de archivos), lista de enlaces rotos.

### HTML, informe web autónomo

5 temas a elegir (`--theme`). El tamaño total del sitio se destaca en primer lugar (es el objetivo principal de un informe de escaneo) y se muestra en formato legible (KB/MB/GB...) en todas partes — CLI, TUI, exportaciones — en lugar de en bytes brutos. Maquetación propia: contenedor, cuadrícula de estadísticas, histograma SVG del reparto por familia (dibujado a mano, sin dependencia pesada de gráficos — misma técnica que el diagrama de arquitectura de `omega-deep`), tablas de extensiones/archivos más grandes. Los dominios externos enlazados muestran los 20 primeros directamente y el resto en un panel plegable (útil en un sitio con cientos de redirecciones externas); la lista de enlaces rotos aparece plegada por defecto.

El árbol se muestra en HTML nativo **multinivel**: un `<details>` por directorio, solo la raíz abierta por defecto, cada subcarpeta se despliega de forma independiente al hacer clic (inspirado en un script de generación de índices del usuario) — un navegador solo maqueta el contenido abierto, así que sigue siendo utilizable incluso para un sitio de varias decenas de miles de archivos, sin JavaScript.

## 9. Historial

Cada escaneo se guarda (SQLite, `var/db/omega-fold.db`). Historial consultable por objetivo (`omega-fold history --target ...`), detalle de un escaneo anterior (`omega-fold show <scan_id>`), o desde el menú Historial de la TUI (repetición incluida).

## 10. Compatibilidad con terminales

La TUI (Textual) detecta automáticamente las capacidades del terminal (emulador, tamaño) y adapta en consecuencia su hoja de estilo estructural (`complete`/`standard`/`reduced`/`mono`), sin opción manual. El modo CLI siempre sigue en texto simple, independiente del terminal. Política compartida por toda la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil según el emulador detectado

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antiguo | `mono` |
| Emulador no reconocido | `reduced` (valor de reserva por defecto) |

### Perfil según el tamaño del terminal

| Tamaño mínimo (columnas × líneas) | Tope de perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| por debajo | `mono` |

El perfil final es **el más restrictivo de los dos** (emulador y tamaño) — se puede actualizar en directo con la tecla `r`.

## 11. Pruebas

```bash
source .venv/bin/activate
lint-imports        # comprueba la Dependency Rule (6 contratos)
pytest -q           # 186 pruebas
ruff check src tests
mypy -p omega_fold
```

Estructura: `tests/unit/` (dominio e infraestructura sin E/S real — exportadores, gráfico SVG, marcado de la pantalla de inicio TUI), `tests/integration/` (sistema de archivos real mediante `tmp_path`, servidor HTTP ficticio `pytest-httpserver`, base SQLite real, CLI de extremo a extremo), `tests/tui/` (navegación mediante `Pilot`, estructural — sin verificación visual autoproclamada, ver `docs/ARCHITECTURE.md` §Interfaz TUI).

## 12. Fuera de alcance

- Análisis de contenido/SEO
- Renderizado de JavaScript del lado del cliente
- Rastreo sin salvaguardas
- Escaneo activo de vulnerabilidades, fuzzing, fuerza bruta
- Panel web

---

> Omega-fold — Cartografiar una estructura, comprobar sus enlaces, nunca adivinar lo que no se ha visitado.
