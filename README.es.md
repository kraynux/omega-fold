<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licencia MIT (véase el archivo LICENSE) -->
<div align="center">
  <img src="docs/assets/omega-fold.png" alt="Omega-Fold" width="256">
</div>

#  OMEGA-FOLD

**Analizador de estructura de sitios/directorios (local y remoto)**

> Desarrollado por **kraynux** para **Omega-server**  
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Página oficial: [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/) &nbsp; Vistas previas: [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-uso)

**Idiomas:**  
[Français](README.md) · [English](README.en.md) · [Español](README.es.md) · [Русский](README.ru.md) · [中文](README.zh-CN.md)

---

**Omega-fold** es una herramienta TUI + CLI que analiza la estructura de un directorio local o de un sitio remoto (crawl HTTP limitado por mecanismos de protección): árbol completo, estadísticas por extensión/familia de archivos, mapeo de enlaces (internos/externos, de todos los tipos) y detección de enlaces rotos. Es la quinta herramienta de la suite `omega-` (después de `omega-scan`, `omega-stress`, `omega-check` y `omega-deep`), estructurada según Clean Architecture. Consulte `docs/ARCHITECTURE.md` para conocer todos los detalles técnicos.

## 1. Visión y alcance

### Qué hace Omega-fold

- Escanea un directorio local (`os.walk` real) o realiza crawl de un sitio remoto con BFS, limitado por mecanismos de protección estrictos.
- Construye el árbol completo (archivos/directorios, profundidad y tamaño) y lo clasifica por familia (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`). Consulte [§4](#4-familias-de-archivos).
- Extrae todos los enlaces (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) de cada página/archivo HTML, los clasifica (interno absoluto/relativo, externo, ancla, `mailto:`/`tel:`/`javascript:`/`data:`) y comprueba su existencia. Consulte [§5](#5-enlaces-y-verificación).
- Calcula estadísticas: distribución por extensión/familia, archivos más grandes, archivos con más enlaces salientes y dominios externos más enlazados.
- Muestra el resultado en TUI (Textual) o en CLI programable mediante scripts, con tres exportaciones (JSON, texto y HTML con 5 temas).
- Conserva un historial persistente de los escaneos (SQLite), que se puede repetir y consultar.

### Qué no hace Omega-fold

- Análisis de contenido o SEO (títulos, metadescripciones, densidad de palabras clave).
- Crawl sin mecanismos de protección: la profundidad, el número de páginas y el retraso entre solicitudes siempre están activos.
- Renderizado de JavaScript del lado del cliente (la página se recupera tal como se sirve, sin ejecutarse en un navegador headless).
- Escaneo activo de vulnerabilidades, fuzzing o fuerza bruta.
- Panel web.

## 2. Instalación

### Requisitos previos

- Python 3.10+
- Conexión a Internet para las dependencias
- Para la TUI: una [Nerd Font](https://www.nerdfonts.com/) instalada en el terminal para el icono del encabezado. Sin ella, el carácter aparece como un cuadrado vacío (la misma limitación que un emoji, aunque está mucho más disponible entre los usuarios de terminal). Su ausencia no afecta al funcionamiento y es puramente estética.

### Instalación

```bash
[ -d omega-fold ] && echo "ℹ️ Ya se ha extraído aquí; se omite este paso." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh`:

1. Crea el entorno virtual `.venv` si todavía no existe.
2. Instala las dependencias (`vendor/omega-lib/` y después `pip install -e .`; `pyproject.toml` sigue siendo la única fuente de verdad).
3. Hace ejecutables `omega-fold.sh` e `install.sh`.
4. Añade el alias `fold` a `~/.bashrc` y `~/.zshrc` (sin duplicarlo si ya está presente).

### Dependencias

Declaradas en `pyproject.toml` (no existe `requirements.txt`):
- `omega-lib`: biblioteca compartida de la suite (temas de exportación, `ConfidenceLevel`), incluida en `vendor/omega-lib/`
- `httpx`: verificación síncrona de enlaces externos (`LinkChecker`)
- `aiohttp`: crawl HTTP asíncrono (`DistantCrawler`)
- `beautifulsoup4` + `lxml`: extracción de enlaces HTML
- `jinja2`: plantillas para la exportación HTML
- Dependencias de desarrollo (`pip install -e ".[dev]"`): `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Uso

### Modo interactivo (TUI)

Recomendado para el uso diario; se inicia sin argumentos:

```bash
./omega-fold.sh
```
Si ha creado el alias, escriba simplemente `fold` en el terminal:
```bash
fold
```

Flujo: pantalla de inicio (se cierra al pulsar una tecla o hacer clic) → menú principal (Scanner / History / Settings / Help) → entrada del objetivo, tipo (local/remoto), modo (estático/dinámico) y mecanismos de protección del crawl remoto, con una etiqueta explícita para cada campo → escaneo (indicador indeterminado, registro de operaciones en directo, botón Cancelar disponible en todo momento) → detalle del escaneo (distribución por familia y extensión, árbol, enlaces rotos, exportación) → historial (ver detalle, **exportar directamente** sin volver a pasar por el detalle, repetir) y ajustes desde el menú principal. La adaptación al terminal (colores, tamaño y degradación estructural) es automática.

#### Atajos de teclado

| Tecla | Acción |
|---|---|
| `↑` / `↓` | Moverse entre los elementos de una pantalla |
| `Tab` / `Shift+Tab` | Moverse entre los campos de un formulario |
| `Esc` | Volver a la pantalla anterior (confirmación de salida en la pantalla de inicio) |
| `t` | Siguiente tema (se aplica inmediatamente, sin confirmación) |
| `r` | Actualizar la detección del terminal |
| `a` | Mostrar la ayuda |
| `q` | Salir (con confirmación) |

### Modo programable (CLI)

Cualquier subcomando activa el modo CLI:

```bash
# Escaneo local (árbol + enlaces internos)
./omega-fold.sh scan /var/www/monsite --type local

# Escaneo local en modo dinámico (también verifica enlaces externos mediante HTTP)
./omega-fold.sh scan /var/www/monsite --type local --mode dynamic

# Escaneo remoto (crawl BFS desde la URL inicial)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Historial (filtrable por objetivo)
./omega-fold.sh history --target /var/www/monsite --limit 20

# Detalle de un escaneo (texto, JSON o HTML) — 5 temas de exportación disponibles
./omega-fold.sh show <scan_id> --format html --theme omega-base --output rapport.html
```

Opciones de `scan`:

| Opción | Valor predeterminado | Efecto |
|---|---|---|
| `--type` | *(obligatorio)* | `local` o `distant` |
| `--mode` | `static` | `static` (enlaces externos sin verificar) o `dynamic` (verificados mediante HTTP) |
| `--max-depth` | `5` | Profundidad máxima seguida (escaneo remoto) |
| `--max-pages` | `1000` | Número máximo de páginas rastreadas (escaneo remoto) |
| `--delay` | `100` | Retraso (ms) entre dos solicitudes (escaneo remoto) |
| `--user-agent` | `omega-fold/0.1` | Cabecera `User-Agent` enviada (escaneo remoto) |
| `--respect-robots` | desactivado | Respeta `robots.txt` (escaneo remoto) |

Para un escaneo remoto, un objetivo sin esquema (`example.org`) se completa automáticamente como `https://example.org`; no hace falta indicarlo salvo para forzar `http://` explícitamente.

Si el sitio tiene más páginas que `--max-pages` (1000 de forma predeterminada), el escaneo se detiene en el límite pero lo informa explícitamente: `scan.status` toma el valor `completed_truncated` en lugar de `completed`, con una advertencia visible en el resumen de CLI, la pantalla de detalle de la TUI y la exportación HTML. El número de archivos informado no representa entonces el tamaño real del sitio; vuelva a ejecutar con un `--max-pages` superior para obtener una cobertura completa.

Si `install.sh` creó el alias, `fold scan ...` funciona desde cualquier ubicación del terminal, sin el prefijo `./omega-fold.sh`.

## 4. Familias de archivos

Cada archivo se clasifica en una familia según su extensión (la primera coincidencia gana). Los detalles completos y la tabla extensión por extensión están en `docs/FAMILIES.md`.

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

## 5. Enlaces y verificación

### Clasificación

Cada enlace encontrado (`href`/`src`/`action`) se clasifica en este orden de prioridad:

| Tipo | Se reconoce cuando | Ejemplo |
|---|---|---|
| `empty` | Cadena vacía | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Esquema especial | `mailto:x@y.z` |
| `anchor` | Comienza directamente con `#` (ancla pura) | `#section` |
| `external` | `http://`, `https://` o `//` (protocol-relative) | `https://example.org` |
| `absolute` | Comienza con `/` | `/img/logo.png` |
| `relative` | Todo lo demás | `img/logo.png`, `../page.html` |

`absolute` y `relative` son las dos formas de un enlace **interno**. Un enlace `page.html#section` sigue siendo `relative` (el fragmento final no lo convierte en una simple ancla; sigue navegando hacia otro recurso).

### Verificación

- **Enlace interno**: siempre se verifica contra el conjunto de rutas encontradas realmente durante el escaneo (sin solicitud de red). `absolute` se resuelve respecto a la raíz del escaneo; `relative` con un separador se resuelve respecto al directorio del archivo de origen; `relative` sin separador (solo el nombre del archivo) se busca en todo el árbol. En un escaneo remoto, la verificación se realiza en una segunda pasada tras finalizar el crawl, contra el conjunto de páginas visitadas correctamente. Una página fuera de los mecanismos de protección o bloqueada por `robots.txt` permanece como `unchecked`; nunca se asume como `broken`.
- **Enlace externo**: se verifica mediante una solicitud HTTP (HEAD y luego GET si HEAD falla) únicamente en modo `dynamic`; en modo `static`, permanece como `unchecked`.

## 6. Mecanismos de protección del crawl remoto

Siempre están activos y nunca se pueden desactivar; solo se pueden ajustar sus umbrales:

- **Profundidad** (`--max-depth`): limita únicamente la puesta en cola de nuevas páginas que se van a rastrear; los enlaces encontrados en una página ya visitada siempre se incluyen en el resultado, aunque no se siga la página a la que apuntan.
- **Número de páginas** (`--max-pages`): limita el número total de páginas visitadas, en todas las profundidades.
- **Retraso** (`--delay`): pausa entre dos solicitudes HTTP consecutivas.
- **Mismo dominio**: solo se siguen enlaces internos hacia el mismo `netloc` que la URL inicial. Se comprueba tanto la ruta del enlace como la URL **realmente cargada tras una redirección**: un permalink cuya ruta parezca una carpeta interna (`/go/xyz`, `/public/nom/`) pero que en realidad redirija a un dominio externo nunca se trata como una página del sitio escaneado.
- **`robots.txt`** (`--respect-robots`): refuerza los mecanismos de protección en lugar de debilitarlos; una página prohibida nunca se visita y sus enlaces salientes permanecen como `unchecked`.

## 7. Arquitectura

Omega-fold está estructurado según **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alineada con la plantilla de la suite `omega-` (consulte `omega-scan`/`omega-check`/`omega-deep`) y verificada por `import-linter` después de cada modificación. Los detalles completos están en **`docs/ARCHITECTURE.md`**.

Vista general muy breve:

```text
src/omega_fold/
├── domain/          Lógica de negocio pura: escaneos, árbol (tree), enlaces, estadísticas, informes
├── application/     Casos de uso (commands/queries) — run_scan (local/distant), export_scan_report...
├── ports/           Contratos esperados por la aplicación (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implementaciones concretas (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    exportadores Jinja2 — Textual NO está aquí)
├── interfaces/      tui/ (Textual) y cli/ (programable), con paridad funcional estricta
├── app/             Ensamblaje (DependencyContainer, bootstrap, ciclo de vida)
├── core/, shared/   Vocabulario transversal, utilidades no relacionadas con el negocio
└── plugins/         Estructura preparada, vacía (sin eje de extensión confirmado)
```

Reglas de diseño:
- `domain/tree/service.py`: agrega una lista plana de archivos ya conocida en un árbol, sin realizar nunca I/O; el recorrido real (`os.walk`) está en `infrastructure/filesystem/`.
- `domain/scans/policies.py`: mecanismos de protección del crawl (profundidad/páginas/dominio), lógica pura que puede probarse sin red.
- `infrastructure/filesystem/` e `infrastructure/network/`: realizan I/O (disco, HTTP), nunca emiten juicios.
- `infrastructure/exporters/`: leen el resultado del escaneo ya ensamblado, nunca recalculan una estadística.
- `infrastructure/storage/sqlite/`: almacena solo los datos fuente (`scans`/`files`/`links`); el árbol y las estadísticas se recalculan al leer mediante las mismas funciones puras que en el escaneo inicial (consulte `DECISIONS_ARCHITECTURE.md`, D-011), sin duplicarlos nunca en la base de datos.

## 8. Exportaciones

Los informes se generan en `var/exports/` de forma predeterminada (ruta de ejecución anclada al directorio del proyecto, `$OMEGA_FOLD_VAR_DIR` para sobrescribirla), o en la ruta indicada por `--output`.

### JSON, fuente de verdad

Estructura completa del resultado (`Scan` + árbol + enlaces + estadísticas), estrictamente serializable como JSON.

### Texto, informe humano compacto

Resumen, distribución por familia, árbol ASCII (limitado a 6 niveles de profundidad; un informe de texto no pretende enumerar un árbol de miles de archivos) y lista de enlaces rotos.

### HTML, informe web autónomo

5 temas disponibles (`--theme`). El tamaño total del sitio se destaca primero (es el objetivo principal de un informe de escaneo) y se muestra en un formato legible (KB/MB/GB...) en todas partes — CLI, TUI y exportaciones — en lugar de bytes sin procesar. Diseño específico: contenedor, cuadrícula de estadísticas, histograma SVG de distribución por familia (dibujado a mano, sin dependencia pesada de gráficos; misma técnica que el diagrama de arquitectura de `omega-deep`), tablas de extensiones/archivos más grandes. Los dominios externos enlazados muestran los 20 primeros directamente, y el resto en un panel desplegable; la lista de enlaces rotos aparece contraída de forma predeterminada.

El árbol se renderiza en HTML nativo **multinivel**: un `<details>` por directorio, solo la raíz abierta de forma predeterminada y cada subdirectorio se despliega de manera independiente al hacer clic, sin JavaScript.

## 9. Historial

Cada escaneo se conserva (SQLite, `var/db/omega-fold.db`). El historial se puede consultar por objetivo (`omega-fold history --target ...`), ver el detalle de un escaneo anterior (`omega-fold show <scan_id>`) o acceder desde el menú Historial de la TUI (incluida la repetición).

## 10. Compatibilidad con terminales

La TUI (Textual) detecta automáticamente las capacidades del terminal (emulador y tamaño) y adapta en consecuencia su hoja de estilos estructural (`complete`/`standard`/`reduced`/`mono`), sin necesidad de una opción manual. El modo CLI sigue siendo siempre texto simple e independiente del terminal. Esta política es compartida por toda la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Perfil según el emulador detectado

| Emulador | Perfil inicial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderno | `reduced` |
| TTY Linux, SSH antiguo | `mono` |
| Emulador no reconocido | `reduced` (fallback predeterminado) |

### Perfil según el tamaño del terminal

| Tamaño mínimo (columnas × filas) | Límite del perfil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| inferior | `mono` |

El perfil final es **el más restrictivo de los dos** (emulador y tamaño) y puede actualizarse en directo con la tecla `r`.

## 11. Pruebas

```bash
source .venv/bin/activate
lint-imports        # comprueba la Dependency Rule (6 contratos)
pytest -q           # 165 pruebas
ruff check src tests
mypy -p omega_fold
```

Estructura: `tests/unit/` (domain e infrastructure sin I/O real: exportadores, gráfico SVG y marcado de la pantalla de inicio TUI), `tests/integration/` (filesystem real mediante `tmp_path`, servidor HTTP falso con `pytest-httpserver`, base de datos SQLite real y CLI de extremo a extremo), `tests/tui/` (navegación mediante `Pilot`, estructural; no se afirma verificación visual automatizada; consulte `docs/ARCHITECTURE.md` §Interfaz TUI).

## 12. Fuera de alcance

- Análisis de contenido/SEO
- Renderizado de JavaScript del lado del cliente
- Crawl sin mecanismos de protección
- Escaneo activo de vulnerabilidades, fuzzing o fuerza bruta
- Panel web

---

> Omega-fold — Cartografiar una estructura, verificar sus enlaces y nunca adivinar lo que no se ha visitado.