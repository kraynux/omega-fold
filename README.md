<div align="center">
  <img src="assets/omega-fold.png" alt="Omega-Fold" width="160">
</div>

#  OMEGA-FOLD

**Analyseur de structure de site/répertoire (local et distant)**

Élaboré par kraynux pour Omega-server
[https://kraynux.snake-mackarel.ts.net](https://kraynux.snake-mackarel.ts.net)

Page officiel : [OMEGA-FOLD](https://kraynux.snake-mackarel.ts.net/omega-fold/)  
Aperçus : [SCREENSHOTS](https://kraynux.snake-mackarel.ts.net/omega-fold/screenshots/)  


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![Interface](https://img.shields.io/badge/Interface-TUI%20%2B%20CLI-cyan.svg)](#3-utilisation)

---

Omega-fold est un outil TUI + CLI qui analyse la structure d'un répertoire local ou d'un site distant (crawl HTTP borné par des garde-fous) : arborescence complète, statistiques par extension/famille de fichier, cartographie des liens (internes/externes, tous types confondus), détection des liens cassés. Cinquième outil de la suite `omega-` (après `omega-scan`, `omega-stress`, `omega-check` et `omega-deep`), structuré en Clean Architecture — voir `docs/ARCHITECTURE.md` pour le détail technique complet.

## 1. Vision et périmètre

### Ce que fait Omega-fold

- Scanne un répertoire local (`os.walk` réel) ou crawle un site distant en BFS, borné par des garde-fous stricts.
- Construit l'arborescence complète (fichiers/répertoires, profondeur, taille) et la classifie par famille (`images`/`documents`/`code`/`data`/`archives`/`fonts`/`video`/`audio`/`text`/`other`) — voir [§4](#4-familles-de-fichiers).
- Extrait tous les liens (`<a href>`, `<img src>`, `<script src>`, `<link href>`, `<form action>`) de chaque page/fichier HTML, les classe (interne absolu/relatif, externe, ancre, `mailto:`/`tel:`/`javascript:`/`data:`), et vérifie leur existence — voir [§5](#5-liens-et-vérification).
- Calcule des statistiques : répartition par extension/famille, plus gros fichiers, fichiers avec le plus de liens sortants, domaines externes les plus liés.
- Restitue le résultat en TUI (Textual) ou en CLI scriptable, avec trois exports (JSON, texte, HTML 5 thèmes).
- Conserve un historique persistant des scans (SQLite), rejouable et consultable.

### Ce qu'Omega-fold ne fait pas

- Analyse de contenu ou de SEO (titres, méta-descriptions, densité de mots-clés).
- Crawl sans garde-fous — profondeur, nombre de pages et délai entre requêtes toujours actifs.
- Rendu JavaScript côté client (page récupérée telle que servie, pas exécutée dans un navigateur headless).
- Scan de vulnérabilités actives, fuzzing, bruteforce.
- Dashboard web.

## 2. Installation

### Prérequis

- Python 3.10+
- Connexion Internet, pour les dépendances
- Pour le TUI : une police [Nerd Font](https://www.nerdfonts.com/) installée dans le terminal, pour l'icône du header — sans elle, ce caractère se rend en carré vide (même limite qu'un emoji, mais bien plus largement disponible chez les utilisateurs de terminal). Absence sans conséquence sur le fonctionnement, purement cosmétique.

### Installation

```bash
[ -d omega-fold ] && echo "ℹ️ Déjà extrait ici, étape ignorée." || tar -xzf omega-fold.tar.gz
cd omega-fold/
chmod +x install.sh
./install.sh
```

`install.sh` :

1. Crée l'environnement virtuel `.venv` s'il n'existe pas déjà.
2. Installe les dépendances (`vendor/omega-lib/` puis `pip install -e .`, `pyproject.toml` reste l'unique source de vérité).
3. Rend `omega-fold.sh` et `install.sh` exécutables.
4. Ajoute l'alias `fold` à `~/.bashrc` et `~/.zshrc` (sans doublon si déjà présent).

### Dépendances

Déclarées dans `pyproject.toml` (pas de `requirements.txt`) :
- `omega-lib` : bibliothèque partagée de la suite (thèmes d'export, `ConfidenceLevel`) — vendorisée dans `vendor/omega-lib/`
- `httpx` : vérification synchrone des liens externes (`LinkChecker`)
- `aiohttp` : crawl HTTP asynchrone (`DistantCrawler`)
- `beautifulsoup4` + `lxml` : extraction des liens HTML
- `jinja2` : templating pour l'export HTML
- Dépendances de développement (`pip install -e ".[dev]"`) : `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-httpserver`, `ruff`, `mypy`, `import-linter`

## 3. Utilisation

### Mode interactif (TUI)

Recommandé pour l'usage quotidien — lancé sans argument :

```bash
./omega-fold.sh
```
si vous avez créé l'alias, tapez juste `fold` dans le terminal :
```bash
fold
```

Parcours : écran de démarrage (se ferme sur une touche ou un clic) → menu principal (Scanner / Historique / Réglages / Aide) → saisie de la cible, du type (local/distant), du mode (statique/dynamique) et des garde-fous de crawl distant, chaque champ portant son étiquette explicite → scan (jauge indéterminée, déroulé des opérations en direct, bouton Annuler à tout moment) → détail du scan (répartition par famille et par extension, arborescence, liens cassés, export) → historique (voir détail, **exporter directement** sans repasser par le détail, rejouer) et réglages depuis le menu principal. L'adaptation au terminal (couleurs, taille, dégradation structurelle) est automatique.

#### Raccourcis clavier

| Touche | Action |
|---|---|
| `↑` / `↓` | Naviguer entre les éléments d'un écran |
| `Tab` / `Maj+Tab` | Naviguer entre les champs d'un formulaire |
| `Échap` | Retour à l'écran précédent (confirmation de sortie sur l'accueil) |
| `t` | Thème suivant (appliqué immédiatement, sans confirmation) |
| `r` | Rafraîchir la détection du terminal |
| `a` | Afficher l'aide |
| `q` | Quitter (avec confirmation) |

### Mode scriptable (CLI)

Toute sous-commande déclenche le mode CLI :

```bash
# Scan local (arborescence + liens internes)
./omega-fold.sh scan /var/www/monsite --type local

# Scan local en mode dynamique (verifie aussi les liens externes par HTTP)
./omega-fold.sh scan /var/www/monsite --type local --mode dynamic

# Scan distant (crawl BFS depuis l'URL de depart)
./omega-fold.sh scan https://example.org --type distant --mode dynamic \
    --max-depth 3 --max-pages 200 --delay 200 --respect-robots

# Historique (filtrable par cible)
./omega-fold.sh history --target /var/www/monsite --limit 20

# Detail d'un scan (texte, JSON ou HTML) — 5 themes d'export au choix
./omega-fold.sh show <scan_id> --format html --theme omega-base --output rapport.html
```

Options de `scan` :

| Option | Défaut | Effet |
|---|---|---|
| `--type` | *(requis)* | `local` ou `distant` |
| `--mode` | `static` | `static` (liens externes non vérifiés) ou `dynamic` (vérifiés par HTTP) |
| `--max-depth` | `5` | Profondeur maximale suivie (scan distant) |
| `--max-pages` | `1000` | Nombre maximal de pages crawlées (scan distant) |
| `--delay` | `100` | Délai (ms) entre deux requêtes (scan distant) |
| `--user-agent` | `omega-fold/0.1` | En-tête `User-Agent` envoyé (scan distant) |
| `--respect-robots` | désactivé | Respecte `robots.txt` (scan distant) |

Pour un scan distant, une cible sans schéma (`example.org`) est automatiquement complétée en `https://example.org` — inutile de le préciser sauf pour forcer `http://` explicitement.

Si le site a plus de pages que `--max-pages` (1000 par défaut), le scan s'arrête à la limite mais le rapporte explicitement : `scan.status` vaut `completed_truncated` plutôt que `completed`, avec un avertissement visible dans le résumé CLI, l'écran de détail du TUI et l'export HTML — le nombre de fichiers rapporté n'est alors pas la taille réelle du site, relancer avec `--max-pages` plus élevé pour une couverture complète.

Si l'alias a été créé par `install.sh`, `fold scan ...` fonctionne de partout dans le terminal, sans le préfixe `./omega-fold.sh`.

## 4. Familles de fichiers

Chaque fichier est classé dans une famille selon son extension (premier match gagnant) — détail complet et tableau extension par extension : `docs/FAMILIES.md`.

| Famille | Exemples d'extensions |
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
| `other` | tout le reste |

## 5. Liens et vérification

### Classification

Chaque lien trouvé (`href`/`src`/`action`) est classé, dans cet ordre de priorité :

| Type | Reconnu quand | Exemple |
|---|---|---|
| `empty` | Chaîne vide | `href=""` |
| `mailto` / `tel` / `javascript` / `data` | Schéma spécial | `mailto:x@y.z` |
| `anchor` | Commence directement par `#` (ancre pure) | `#section` |
| `external` | `http://`, `https://` ou `//` (protocol-relative) | `https://example.org` |
| `absolute` | Commence par `/` | `/img/logo.png` |
| `relative` | Tout le reste | `img/logo.png`, `../page.html` |

`absolute` et `relative` sont les deux formes d'un lien **interne** — un lien `page.html#section` reste `relative` (le fragment de fin n'en fait pas une simple ancre, il navigue bien vers une autre ressource).

### Vérification

- **Lien interne** : toujours vérifié contre l'ensemble des chemins réellement trouvés pendant le scan (pas de requête réseau) — `absolute` résolu contre la racine du scan, `relative` avec un séparateur résolu contre le répertoire du fichier source, `relative` sans séparateur (nom de fichier seul) recherché dans tout l'arbre. Pour un scan distant, la vérification se fait en une seconde passe une fois le crawl terminé, contre l'ensemble des pages réellement visitées avec succès — une page hors garde-fous ou bloquée par `robots.txt` reste `unchecked`, jamais `broken` par supposition.
- **Lien externe** : vérifié par une requête HTTP (HEAD puis GET si HEAD échoue) uniquement en mode `dynamic` — en mode `static`, il reste `unchecked`.

## 6. Garde-fous de crawl distant

Toujours actifs, jamais désactivables — seuls leurs seuils sont ajustables :

- **Profondeur** (`--max-depth`) : borne uniquement la mise en file de nouvelles pages à crawler ; les liens trouvés sur une page déjà visitée restent toujours rapportés dans le résultat, même si la page qu'ils ciblent ne sera pas suivie.
- **Nombre de pages** (`--max-pages`) : borne le nombre total de pages visitées, toutes profondeurs confondues.
- **Délai** (`--delay`) : pause entre deux requêtes HTTP consécutives.
- **Même domaine** : seuls les liens internes vers le même `netloc` que l'URL de départ sont suivis — vérifié aussi bien sur le chemin du lien que sur l'URL **réellement chargée après redirection** : un permalien dont le chemin ressemble à un dossier interne (`/go/xyz`, `/public/nom/`) mais qui redirige en réalité vers un domaine externe n'est jamais traité comme une page du site scanné (son contenu ne serait pas le vôtre).
- **`robots.txt`** (`--respect-robots`) : renforce les garde-fous plutôt que de les affaiblir — une page interdite n'est jamais visitée, ses liens sortants restent `unchecked`.

## 7. Architecture

Omega-fold est structuré en **Clean Architecture** (domain / application / infrastructure / interfaces / ports / core / app / plugins / shared), alignée sur le gabarit de la suite `omega-` (voir `omega-scan`/`omega-check`/`omega-deep`) et vérifiée par `import-linter` à chaque modification. Le détail complet vit dans **`docs/ARCHITECTURE.md`**.

Vue d'ensemble très courte :

```text
src/omega_fold/
├── domain/          Logique métier pure : scans, arborescence (tree), liens, statistiques, rapports
├── application/     Cas d'usage (commands/queries) — run_scan (local/distant), export_scan_report...
├── ports/           Contrats attendus par l'application (local_fs_reader, distant_crawler,
│                    html_link_extractor, link_checker, scan_repository, report_exporter...)
├── infrastructure/  Implémentations concrètes (os.walk, aiohttp, httpx, BeautifulSoup, SQLite,
│                    exporteurs Jinja2 — Textual n'est PAS ici)
├── interfaces/      tui/ (Textual) et cli/ (scriptable), à parité fonctionnelle stricte
├── app/             Assemblage (DependencyContainer, bootstrap, cycle de vie)
├── core/, shared/   Vocabulaire transverse, utilitaires non métier
└── plugins/         Structure posée, vide (aucun axe d'extension confirmé)
```

Règles de conception :
- `domain/tree/service.py` : agrège une liste plate de fichiers déjà connue en arborescence, ne fait jamais d'E/S — le parcours réel (`os.walk`) vit dans `infrastructure/filesystem/`.
- `domain/scans/policies.py` : garde-fous de crawl (profondeur/pages/domaine), pure logique testable sans réseau.
- `infrastructure/filesystem/` et `infrastructure/network/` : font l'E/S (disque, HTTP), ne jugent jamais.
- `infrastructure/exporters/` : lisent le résultat de scan déjà assemblé, ne recalculent jamais une statistique.
- `infrastructure/storage/sqlite/` : ne stocke que les données source (`scans`/`files`/`links`) — l'arborescence et les statistiques sont recalculées à la lecture par les mêmes fonctions pures que le scan initial (voir `DECISIONS_ARCHITECTURE.md`, D-011), jamais dupliquées en base.

## 8. Exports

Les rapports sont générés dans `var/exports/` par défaut (chemin runtime ancré sur le dossier du projet, `$OMEGA_FOLD_VAR_DIR` pour le surcharger), ou au chemin indiqué (`--output`).

### JSON, source de vérité

Structure complète du résultat (`Scan` + arborescence + liens + statistiques), strictement JSON-sérialisable.

### Texte, rapport humain compact

Résumé, répartition par famille, arborescence ASCII (bornée à 6 niveaux de profondeur — un rapport texte n'a pas vocation à lister un arbre de milliers de fichiers), liste des liens cassés.

### HTML, rapport web autonome

5 thèmes au choix (`--theme`). La taille totale du site est mise en avant en premier (c'est l'objectif premier d'un rapport de scan) et affichée en format lisible (Ko/Mo/Go...) partout — CLI, TUI, exports — plutôt qu'en octets bruts. Mise en page dédiée : conteneur, grille de statistiques, histogramme SVG de répartition par famille (dessiné à la main, aucune dépendance de charting lourde — même technique que le diagramme d'architecture d'`omega-deep`), tableaux extensions/plus gros fichiers. Les domaines externes liés affichent les 20 premiers directement, le reste dans un volet repliable (utile sur un site aux centaines de redirections externes) ; la liste des liens cassés est présentée repliée par défaut.

L'arborescence est rendue en HTML natif **multi-niveaux** : un `<details>` par répertoire, seule la racine ouverte par défaut, chaque sous-dossier se développe indépendamment au clic (inspiré d'un script de génération d'index de l'utilisateur) — un navigateur ne met en page que le contenu ouvert, donc ça reste utilisable même pour un site de plusieurs dizaines de milliers de fichiers, sans JavaScript.

## 9. Historique

Chaque scan est persisté (SQLite, `var/db/omega-fold.db`). Historique consultable par cible (`omega-fold history --target ...`), détail d'un scan passé (`omega-fold show <scan_id>`), ou depuis le menu Historique du TUI (rejeu compris).

## 10. Compatibilité terminaux

Le TUI (Textual) détecte automatiquement les capacités du terminal (émulateur, taille) et adapte sa feuille de style structurelle en conséquence (`complete`/`standard`/`reduced`/`mono`), sans flag manuel. Le mode CLI reste toujours en texte simple, indépendant du terminal. Politique partagée par toute la suite `omega-` (`omega-lib`, `terminal/policies.py`).

### Profil selon l'émulateur détecté

| Émulateur | Profil initial |
|---|---|
| Ghostty, Alacritty, WezTerm, Kitty | `complete` |
| Konsole, GNOME Terminal, Terminator, Xfce4 Terminal | `standard` |
| xterm, urxvt, SSH moderne | `reduced` |
| TTY Linux, SSH legacy | `mono` |
| Émulateur non reconnu | `reduced` (repli par défaut) |

### Profil selon la taille du terminal

| Taille minimale (colonnes × lignes) | Plafond de profil |
|---|---|
| 120 × 32 | `complete` |
| 100 × 28 | `standard` |
| 80 × 24 | `reduced` |
| en dessous | `mono` |

Le profil final retenu est **le plus restrictif des deux** (émulateur et taille) — rafraîchissable en direct par la touche `r`.

## 11. Tests

```bash
source .venv/bin/activate
lint-imports        # verifie la Dependency Rule (6 contrats)
pytest -q           # 165 tests
ruff check src tests
mypy -p omega_fold
```

Structure : `tests/unit/` (domaine et infrastructure sans I/O reelle — exporteurs, graphique SVG, balisage du splash TUI), `tests/integration/` (vrai filesystem via `tmp_path`, serveur HTTP factice `pytest-httpserver`, vraie base SQLite, CLI de bout en bout), `tests/tui/` (navigation via `Pilot`, structurel — pas de vérification visuelle auto-revendiquée, voir `docs/ARCHITECTURE.md` §Interface TUI).

## 12. Hors périmètre

- Analyse de contenu/SEO
- Rendu JavaScript côté client
- Crawl sans garde-fous
- Scan de vulnérabilités actives, fuzzing, bruteforce
- Dashboard web

---

> Omega-fold — Cartographier une structure, vérifier ses liens, jamais deviner ce qui n'a pas été visité.
