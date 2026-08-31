# Architecture technique

Clean Architecture à 9 couches, identique dans son principe à `omega-scan`/`omega-check`/`omega-deep` (voir `~/DEV/SUITE/DECISIONS_ARCHITECTURE.md`, décisions D-000 et D-007 pour le rationnel du choix et la manière dont les contrats ont été portés).

## Dependency Rule

```
app                                     -- racine de composition
infrastructure | interfaces | plugins   -- adaptateurs, indépendants entre eux
application                             -- cas d'usage (commands/queries)
ports                                   -- contrats (Protocol)
domain                                  -- métier pur
core                                    -- vocabulaire transverse
```

Une couche ne peut importer que les couches strictement en dessous d'elle dans cette liste (l'extérieur dépend de l'intérieur, jamais l'inverse). Vérifié à chaque modification par `import-linter` (`lint-imports`), 6 contrats :

1. **Dependency Rule** (`type = "layers"`) : l'ordre ci-dessus.
2. **`interfaces` ne dépend jamais directement de `infrastructure`** : la CLI/TUI passe toujours par `application/`, jamais de raccourci vers un adaptateur concret.
3. **`httpx`/`aiohttp`/`bs4`/`lxml` confinés à `infrastructure.network`** — `httpx` pour la vérification synchrone des liens externes (`HttpLinkChecker`), `aiohttp` pour le crawl asynchrone (`AiohttpCrawler`), `bs4`/`lxml` pour l'extraction de liens (`Bs4LinkExtractor`).
4. **`sqlite3` confiné à `infrastructure.storage.sqlite`**.
5. **`jinja2` confiné à `infrastructure.exporters.html_exporter`** — seul module autorisé à en importer ; le composite `infrastructure/exporters/exporter.py` importe légitimement `html_exporter.py` par composition et est explicitement exclu de la liste des `source_modules` du contrat (même point déjà rencontré côté `omega-deep`).
6. **`textual` confiné à `interfaces.tui`** (avec `interfaces.cli` explicitement dans les `source_modules` interdits, pour qu'il reste lui aussi indépendant de `textual`) — voir §Interface TUI plus bas.

## Pourquoi `Protocol` et pas `ABC`

Tous les ports (`ports/*.py`) sont des `typing.Protocol`, pas des `abc.ABC`. Les implémentations ne héritent pas explicitement du port — typage structurel, juste une docstring notant quel port est implémenté (ex. `"""Implemente ports/local_fs_reader.py::LocalFsReader."""`).

## Bounded contexts de `domain/`

| Sous-package | Contenu | Remarque |
|---|---|---|
| `domain/scans/` | `Scan` (cycle de vie, statistiques globales), garde-fous purs de crawl (`policies.py::is_depth_allowed`/`is_page_count_allowed`/`is_same_domain`) | Les garde-fous vivent ici et non dans un `application/pipeline/guards/` (D-010) — précédent direct : `domain/discovery/policies.py` d'omega-deep. |
| `domain/tree/` | `FileEntry`, `DirEntry`, agrégation pure (`service.py::build_tree`/`flatten_files`/`max_depth`/`count_all_dirs`) | Aucune E/S — le parcours réel (`os.walk`) vit dans `infrastructure/filesystem/local_fs_walker.py`. |
| `domain/links/` | `LinkEntry`, classification (`policies.py::classify_link_type`/`is_internal`), vérification d'existence d'un lien interne (`service.py::verify_internal_link`) | Pure — la vérification d'un lien EXTERNE (requête HTTP) vit dans `infrastructure/network/http_link_checker.py`. |
| `domain/stats/` | `ExtensionStats`, `FamilyStats`, `TopFile`, `ExternalDomainStats`, classification par famille (`policies.py::classify_family`, catalogue `families.py::FAMILIES`), calcul (`service.py::compute_*`) | Pure, opère sur des listes `FileEntry`/`LinkEntry` déjà construites. |
| `domain/reports/` | `ScanResult` — assemblage complet d'un scan (`Scan` + arborescence + liens + statistiques) | Forme de donnée pure, construite par l'orchestration applicative (`application/commands/run_scan.py`). |

## Le pipeline de scan

```
application/commands/run_scan.py::run_scan(target_type=...)   -- dispatcher async
  │
  ├─ LOCAL → run_scan_local (sync)
  │    ├─ ports/local_fs_reader.py::read_tree()                → infrastructure/filesystem/local_fs_walker.py
  │    │    └─ domain/tree/service.py::build_tree               → agrégation pure
  │    ├─ pour chaque fichier .html : read_file() + ports/html_link_extractor.py::extract()
  │    │    └─ infrastructure/network/bs4_link_extractor.py
  │    ├─ domain/links/policies.py::classify_link_type (chaque lien)
  │    ├─ lien interne : domain/links/service.py::verify_internal_link (filesystem déjà connu, aucune E/S)
  │    └─ domain/stats/service.py::compute_* (extensions/familles/top fichiers/domaines externes)
  │
  └─ DISTANT → run_scan_distant (async)
       ├─ boucle BFS, tant que is_page_count_allowed :
       │    ├─ ports/distant_crawler.py::fetch() (async)        → infrastructure/network/aiohttp_crawler.py
       │    │    ├─ robots.txt vérifié + mis en cache par domaine DANS le crawler (même nature d'E/S)
       │    │    └─ NE LÈVE JAMAIS pour un échec réseau (timeout/connexion refusée/DNS) — retourne
       │    │         `CrawledPage.fetch_error` renseigné à la place (bug réel trouvé en usage : un
       │    │         `TimeoutError` sur une seule page faisait échouer tout le crawl, sans que
       │    │         l'échec soit rattrapable en amont dans `application/` sans violer la
       │    │         Dependency Rule — le port lui-même garantit ne jamais lever). `ValueError`
       │    │         (yarl/URL syntaxiquement invalide, ex. caractère de contrôle dans un href
       │    │         extrait d'un HTML cassé) capturée au même titre — même bug reel trouvé cote
       │    │         `HttpLinkChecker.check()` : `httpx.InvalidURL` n'est PAS une sous-classe de
       │    │         `httpx.HTTPError`, donc pas rattrapée par le `except` générique existant
       │    ├─ domain/scans/policies.py::is_same_domain(page.final_url, ...) → une page dont le
       │    │    CHEMIN demandé ressemblait à un lien interne mais qui a redirigé (3xx) vers un
       │    │    domaine externe (permalien/raccourci) n'est jamais traitée comme une page du
       │    │    site scanné — ni arborescence, ni liens extraits (bug réel trouvé en usage,
       │    │    `CrawledPage.final_url` distingue l'URL demandée de l'URL réellement chargée)
       │    ├─ extension/famille dérivées du CHEMIN réel de l'URL (`domain/stats/policies.py::
       │    │    classify_family`), pas seulement "HTML ou pas" — bug réel trouvé en usage : les
       │    │    ressources non-HTML (CSS/images/...) finissaient toutes en `extension=""`/
       │    │    `family="other"`, faute d'extraire l'extension du chemin
       │    ├─ extraction des liens de la page (toujours, même hors garde-fous de profondeur)
       │    ├─ domain/scans/policies.py::is_depth_allowed         → borne uniquement la MISE EN FILE
       │    ├─ lien externe + mode DYNAMIC : ports/link_checker.py::check() (sync, via asyncio.to_thread)
       │    │    → infrastructure/network/http_link_checker.py (HEAD puis GET, httpx)
       │    └─ lien interne : mis en attente (pas encore vérifiable, page pas forcément visitée)
       ├─ deuxième passe (après le crawl complet) : vérifie chaque lien interne contre
       │    l'ensemble des pages réellement visitées avec succès (`visited_status`) — une page
       │    hors garde-fous/robots.txt reste UNCHECKED, jamais BROKEN par supposition
       └─ domain/tree/service.py::build_tree("/", files)         → arborescence virtuelle (`_page_url_to_path`)
  │
  └─ (LOCAL et DISTANT) si `scan_repository` fourni :
       ports/scan_repository.py::save() + save_result()          → infrastructure/storage/sqlite/scan_repository.py
```

`run_scan_local` reste synchrone (aucune E/S bloquante à masquer, `os.walk` est déjà rapide) ; `run_scan` (le dispatcher) est `async` dans les deux cas pour donner un point d'entrée unique à `await` à l'appelant (`interfaces/cli/commands/scan_command.py`, seule commande async de la CLI, voir `interfaces/cli/main.py::run()`).

## Stockage SQLite (D-011)

Schéma volontairement simplifié : seulement 3 tables (`scans`/`files`/`links`), pas de table séparée pour l'arborescence ou les statistiques dérivées. `SqliteScanRepository.save_result` aplatit `ScanResult.root_dir` via `domain/tree/service.py::flatten_files` avant d'écrire (delete-then-insert par `scan_id`, pas de `ON DELETE CASCADE` fiable sur `sqlite3` par défaut). `get_result` relit `files`+`links` puis rappelle `build_tree`+`domain/stats/service.py::compute_*` à chaque lecture plutôt que de stocker leur résultat — la racine passée à `build_tree` est `scan.target` pour un scan LOCAL, toujours `"/"` pour un scan DISTANT (chemins virtuels posés par `_page_url_to_path`). Rationnel complet : `~/DEV/SUITE/DECISIONS_ARCHITECTURE.md`, D-011.

## Graphique SVG (histogramme par famille)

`infrastructure/exporters/family_chart.py::render_family_bar_chart(family_stats, palette)` — une barre par famille, proportionnelle à `total_size`, mise en page calculée en Python pur (même technique que `graph_layout.py` d'omega-deep, D-009). N'importe **pas** `jinja2` : construit une chaîne `<svg>...</svg>` autonome, insérée par le template via `| safe`. `width`/`height` fixés à la taille naturelle du graphique (pas `"100%"`) — une colonne `_VALUE_WIDTH` est réservée à droite de chaque barre pour son étiquette de taille, sans quoi la barre la plus longue pousse son étiquette hors du `viewBox` (bug réel trouvé et corrigé lors du smoke test manuel de la Phase 4+5, couvert depuis par un test de non-régression).

L'arborescence ASCII (export texte ET export HTML) est rendue en Python pur (`infrastructure/exporters/text_exporter.py::render_tree_lines`), pas en macro Jinja2 récursive — le contrôle de l'espacement d'une récursion en template s'est révélé trop fragile à maintenir, le prérendu en `<pre>` est plus simple et plus sûr.

## Bibliothèque partagée (`omega-lib`)

Les utilitaires transverses (`clock`, `ids`, `typing`) et le système de thème d'export (`theme/policies.py::EXPORT_PALETTES`, 5 thèmes) viennent de `~/DEV/LIB/omega-lib` (vendorisé dans `vendor/omega-lib/` pour l'installation packagée, voir D-005/D-008) — identique à omega-check/omega-deep. `ConfidenceLevel` est re-exporté depuis `core/enums.py` par cohérence de vocabulaire (D-005) mais n'est utilisé qu'à la marge dans FOLD (`LinkEntry.confidence`) : FOLD n'a pas de logique de qualification de confiance aussi développée que CHECK/DEEP (pas de service/rôle inféré), la plupart des faits qu'il rapporte sont directement vérifiés (existence d'un lien, code HTTP), pas déclarés par une cible potentiellement mensongère.

`ports/settings_store.py`/`ports/terminal_detector.py` existent (re-export `omega_lib`, ajoutés dès la Phase 1 par anticipation, D-008) et sont câblés dans `DependencyContainer`/`bootstrap.py` (`JsonSettingsStore`/`SystemTerminalDetector`) depuis la construction du TUI — voir §Interface TUI ci-dessous.

## Interface TUI

**Construite** (`interfaces/tui/`), sur le même patron que CHECK/DEEP (D-007/D-008) : `app.py` (résout thème + profil de rendu au démarrage, enchaîne splash → accueil), `screens/_base.py::OmegaScreen` (retour `Échap` uniforme), `controllers/startup_controller.py`, `rendering/{stylesheet_loader,textual_theme_builder}.py` — tous portés verbatim. Les feuilles de style (`styles/{base,complete,standard,reduced,mono}.tcss`) sont copiées telles quelles (génériques, aucune classe spécifique à un outil).

Écrans : `splash`/`home` (menu Scanner/Historique/Réglages/Aide/Quitter — ni "Profils" ni "Cibles", FOLD n'a aucun des deux concepts), `scan_setup` (cible + type local/distant + mode static/dynamic + garde-fous de crawl distant, chaque champ portant une étiquette explicite au-dessus — un `placeholder` seul ne s'affiche que si le champ est vide, invisible dès qu'une valeur par défaut y est posée, bug d'UX réel signalé par l'utilisateur), `scan_progress` (voir ci-dessous, avec un bouton Annuler visible dès le lancement), `show_detail` (résumé + `FamilyStatsTable` + `ExtensionStatsTable` + `TreeView` + `BrokenLinksTable` + export), `history` (voir détail / **exporter directement sans repasser par le détail** / rejouer, table rafraîchie à chaque retour sur l'écran — `on_screen_resume`), `settings_screen`/`help_screen`/`quit_confirm`/`confirm`/`export_dialog`/`terminal_warning` — portés verbatim ou quasi (vocabulaire FOLD).

**Annulation d'un scan en cours** (`widgets/progress_panel.py` + `screens/scan_progress.py`) : bouton "Annuler" toujours visible pendant le déroulé, appelle `Worker.cancel()` — `asyncio.CancelledError` n'est jamais rattrapée par le `except Exception` de `_run_scan` (c'est une `BaseException` depuis Python 3.8, pas une `Exception`), le `finally` (nettoyage du handler de log) s'exécute quand même normalement. Pour un scan LOCAL (enveloppé dans `asyncio.to_thread`), le thread sous-jacent continue jusqu'à sa fin naturelle en arrière-plan (Python ne peut pas tuer un thread de force) — sans conséquence, son résultat est simplement jeté.

**`scan_progress.py` ne délègue pas à `run_scan()`** (le dispatcher de `application/commands/run_scan.py`) : il reproduit lui-même le choix local/distant, parce que les deux branches doivent être traitées différemment côté UI — `run_scan_local` est synchrone (`os.walk` réel) et doit être enveloppé dans `asyncio.to_thread` pour ne pas geler l'event loop Textual, alors que `run_scan_distant` est déjà `async` nativement et s'attend directement. `run_scan()` lui-même ne fait pas cette distinction (correct pour la CLI, qui n'a pas d'event loop UI à préserver). Les logs émis par `run_scan.py` (logger `omega_fold.scan`, ajouté pour cette occasion — additif pur, n'affecte aucun retour de fonction ni test existant) sont relayés vers le `RichLog` du `ProgressPanel` via un `logging.Handler`, même mécanisme que CHECK/DEEP.

`widgets/tree_view.py` peuple un `Tree` natif Textual de façon eager (pas de chargement paresseux) depuis `ScanResult.root_dir` — aucun autre outil de la suite n'avait besoin d'un arbre de fichiers avant FOLD, pas de patron existant à porter.

**Art ASCII** (`~/DEV/FOLD/ascii.txt`, fourni par l'utilisateur) : `widgets/home_wordmark.py` (bandeau nu 3 lignes, vif/clair/vif) et `widgets/splash_hero.py` (composition dense : boîte titre, boîte version, bandeau encadré, icône dossier/réseau/serveur, tagline) — lignes brutes conservées telles quelles (`rstrip()` uniquement, aucun recentrage). Le dégradé à 4 niveaux (`█▓▒░`) et les deux voyants explicitement vifs (un `█` à l'intérieur du rack serveur, un `▓` en bas d'écran) sont une interprétation documentée dans le docstring du module — assomption facile à ajuster si la lecture ne correspond pas à l'intention de l'utilisateur, même discipline que les décorations sans règle explicite de CHECK. **Vérification** : la transcription a été contrôlée programmatiquement ligne par ligne contre la source au moment de l'écriture (`tests/unit/interfaces/test_splash_hero.py` couvre la cohérence structurelle du balisage généré, pas le fichier source lui-même — absent du paquet/repo) ; le pipeline `export_screenshot()` (SVG) → PNG est connu peu fiable pour ce jeu de caractères (constat déjà acté côté CHECK/DEEP) — la revue visuelle réelle se fait en direct avec l'utilisateur, pas via une capture automatisée.

**Icône du header** (`app.py::TITLE`) : glyphe Nerd Font (`nf-fa-folder_open`, U+F07C) plutôt qu'un emoji (📁 utilisé initialement) — demande explicite de l'utilisateur, un emoji n'étant pas fiable sur tous les terminaux (rendu en tofu sans police d'emoji, déjà observé sur les captures Chromium headless de cette session). Nécessite une police Nerd Font installée côté terminal ; absence sans conséquence fonctionnelle (glyphe manquant rendu en carré vide, purement cosmétique), documenté comme prérequis optionnel dans le README.

Vérifié pour de vrai via l'API `Pilot` de Textual (assertions structurelles sur la pile d'écrans/l'état des widgets, `tests/tui/test_navigation.py`) : démarrage, navigation vers chaque écran du menu, un **vrai** scan local et un **vrai** scan distant (pas mockés, y compris un scénario de redirection hors domaine, de timeout et de lien malformé) jusqu'à `ShowDetailScreen`, consultation de l'historique après un scan, export direct depuis l'historique, annulation d'un scan en cours, présence des étiquettes explicites du formulaire, cycle de thème, confirmation de sortie.
