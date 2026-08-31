# Exemples d'usage

Toutes les sorties ci-dessous sont réelles, capturées lors d'un scan effectif contre un petit site synthétique de démonstration (`index.html` → `about.html` + `assets/style.css`, un lien cassé `/old-page.html`, un lien externe vers `example.org`) — pas des exemples inventés. Les chemins ont été remplacés par `/var/www/monsite` pour la lisibilité, tous les chiffres (tailles, comptes, identifiants) sont ceux réellement produits par l'outil.

## Scanner un répertoire local

```bash
$ omega-fold scan /var/www/monsite --type local
Scan e9e5f06cab9443b68005f396523686f9 — cible /var/www/monsite (local) — statut completed
  taille totale: 256 o  fichiers: 3  repertoires: 1
  liens: 5 (internes: 4, externes: 1, casses: 1)
```

## Consulter l'historique

```bash
$ omega-fold history
e9e5f06cab9443b68005f396523686f9  2026-08-31T11:15:14.936322+00:00  /var/www/monsite (local)  completed  taille=256 o fichiers=3 liens=5
```

## Détail d'un scan (texte)

```bash
$ omega-fold show e9e5f06cab9443b68005f396523686f9
=== OMEGA-FOLD — Rapport de scan ===
Scan ID       : e9e5f06cab9443b68005f396523686f9
Cible         : /var/www/monsite
Type          : local
Date          : 2026-08-31T11:15:14.936322+00:00
Mode          : static
Statut        : completed

Taille totale : 256 o
Fichiers      : 3
Repertoires   : 1
Profondeur max: 1

Liens totaux  : 5
Liens internes: 4
Liens externes: 1
Liens casses  : 1

=== Repartition par famille ===
  code             3 fichier(s)       256 o  (100.0%)

=== Repartition par extension ===
  .html                2 fichier(s)       236 o  (92.2%)
  .css                 1 fichier(s)        20 o  (7.8%)

=== Arborescence ===
/var/www/monsite/
├── assets/
│   └── style.css
├── about.html
└── index.html

=== Liens casses ===
  /old-page.html  (trouve dans /var/www/monsite/index.html)
```

Le lien `/old-page.html` est signalé cassé parce qu'aucun fichier de ce chemin n'a été trouvé pendant le scan — vérification filesystem pure, aucune requête réseau (voir README §5). La taille (`Taille totale`) est toujours affichée en premier et en format lisible (Ko/Mo/Go...) — c'est l'information la plus attendue d'un rapport de scan.

## Exporter un rapport

```bash
# JSON complet (structure de l'agrégat ScanResult)
omega-fold show e9e5f06cab9443b68005f396523686f9 --format json

# HTML avec histogramme de repartition par famille et arborescence multi-niveaux, ecrit dans un fichier
omega-fold show e9e5f06cab9443b68005f396523686f9 --format html --theme omega-neon --output rapport.html
```

Depuis le TUI, l'export est aussi accessible **directement depuis l'écran Historique** (bouton "Exporter"), sans avoir à ouvrir le détail du scan au préalable.

## Scanner un site distant

```bash
$ omega-fold scan http://127.0.0.1:8959/index.html --type distant --mode dynamic --max-depth 2
Scan d374e083ffe7449f8986713e0bd7ed9d — cible http://127.0.0.1:8959/index.html (distant) — statut completed
  taille totale: 716 o  fichiers: 4  repertoires: 1
  liens: 5 (internes: 4, externes: 1, casses: 1)
```

En mode `dynamic`, le lien externe vers `example.org` est vérifié par une vraie requête HTTP (HEAD puis GET) — en mode `static` (par défaut), il resterait `unchecked`. Une cible sans schéma (`example.org` au lieu de `https://example.org`) est automatiquement complétée en `https://`.

## Un site plus grand que `--max-pages`

```bash
$ omega-fold scan http://127.0.0.1:8959/index.html --type distant --max-pages 1
Scan 585bd07149a14e59b2c4b9074f2609c0 — cible http://127.0.0.1:8959/index.html (distant) — statut completed_truncated
  taille totale: 179 o  fichiers: 1  repertoires: 0
  liens: 4 (internes: 3, externes: 1, casses: 0)
  ATTENTION : limite --max-pages atteinte, le site a probablement plus de pages que ce qui est rapporte ici — relancer avec --max-pages plus eleve.
```

Le statut `completed_truncated` (au lieu de `completed`) et l'avertissement explicite évitent de confondre "le site ne contient qu'une page" avec "le scan s'est arrêté prématurément" — le même avertissement apparaît dans l'écran de détail du TUI et dans l'export HTML (bandeau visible). Un scan distant interrompu par `Ctrl+C`/le bouton "Annuler" du TUI n'aboutit à aucun résultat persisté (rien à distinguer, il n'y a simplement pas de scan à consulter).

## Restreindre ou élargir le crawl distant

```bash
# Découverte désactivée de fait : profondeur 0 = seule la page de depart est crawlée
omega-fold scan https://example.org --type distant --max-depth 0

# Garde-fous élargis, délai augmenté pour un site plus lourd, robots.txt respecté
omega-fold scan https://example.org --type distant --mode dynamic \
    --max-depth 5 --max-pages 500 --delay 300 --respect-robots

# User-Agent personnalisé
omega-fold scan https://example.org --type distant --user-agent "mon-outil/1.0"
```

## Isoler l'environnement runtime (base SQLite, exports)

```bash
# Utile pour scanner sans mélanger l'historique avec var/ du projet
OMEGA_FOLD_VAR_DIR=/tmp/fold-test omega-fold scan /tmp/mon-site --type local
OMEGA_FOLD_VAR_DIR=/tmp/fold-test omega-fold history
```

## Workflow typique (audit de liens cassés avant déploiement)

```bash
# 1. Scan du répertoire de build local, statistiques + liens
omega-fold scan ./dist --type local

# 2. Revue du rapport HTML (arborescence, familles, liens cassés)
omega-fold show <scan_id> --format html --output audit.html

# 3. Après correction, nouveau scan pour vérifier que les liens cassés ont disparu
omega-fold scan ./dist --type local
omega-fold history --target ./dist
```
