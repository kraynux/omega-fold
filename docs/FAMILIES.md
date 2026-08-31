# Familles de fichiers

Chaque fichier scanné est classé dans une famille selon son extension — `domain/stats/policies.py::classify_family`, appliqué à chaque `FileEntry` pendant le scan (local ou distant). Catalogue défini dans `domain/stats/families.py::FAMILIES`, verbatim depuis `OMEGA-FOLD_SPECIFICATIONS.md` §3.1.

## Règle de classification

**Premier match gagnant** : les familles sont parcourues dans l'ordre du dictionnaire ci-dessous, la première dont la liste d'extensions contient l'extension du fichier (comparaison insensible à la casse) l'emporte. Une extension absente de toutes les listes tombe dans `other` — jamais d'exception, jamais de fichier non classé.

## Catalogue complet

| Famille | Extensions |
|---|---|
| `images` | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.ico`, `.bmp`, `.tiff`, `.avif` |
| `documents` | `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.odt`, `.ods`, `.odp` |
| `code` | `.html`, `.php`, `.js`, `.ts`, `.py`, `.rb`, `.java`, `.cpp`, `.c`, `.h`, `.css`, `.scss`, `.less`, `.vue`, `.jsx`, `.tsx` |
| `data` | `.json`, `.xml`, `.yaml`, `.yml`, `.csv`, `.sql`, `.db`, `.sqlite`, `.ini`, `.conf`, `.cfg` |
| `archives` | `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, `.bz2`, `.xz` |
| `fonts` | `.ttf`, `.otf`, `.woff`, `.woff2`, `.eot` |
| `video` | `.mp4`, `.webm`, `.avi`, `.mov`, `.mkv`, `.flv` |
| `audio` | `.mp3`, `.wav`, `.ogg`, `.flac`, `.aac` |
| `text` | `.txt`, `.md`, `.rst`, `.log` |
| `other` | *(liste vide — capture tout le reste)* |

## Où c'est utilisé

- `domain/stats/service.py::compute_family_stats` : nombre de fichiers, taille totale et pourcentage du poids total par famille (chaque famille imbrique elle-même ses statistiques par extension, via `compute_extension_stats`).
- `infrastructure/exporters/family_chart.py::render_family_bar_chart` : histogramme SVG dans l'export HTML, une barre par famille, proportionnelle à `total_size`.
- `interfaces/cli` et `infrastructure/exporters/text_exporter.py` : section "Répartition par famille" du rapport.

## Note sur `code`

La famille `code` regroupe à la fois le balisage (`.html`), la logique serveur/côté client (`.php`, `.js`, `.ts`, `.py`...) et les feuilles de style (`.css`, `.scss`, `.less`) — un choix de granularité volontairement large : FOLD ne distingue pas "page HTML" de "script" dans ses statistiques par famille, seul `domain/tree/models.py::FileEntry.extension` porte cette distinction plus fine (visible dans le tableau "Extensions" de l'export HTML/le détail JSON). C'est aussi la famille utilisée pour repérer les fichiers dont le contenu doit être lu pour en extraire des liens (`application/commands/run_scan.py::run_scan_local` ne lit et n'extrait les liens que des fichiers `family == "code"` avec `extension == ".html"`, pas de tous les fichiers `code`).
