# Copyright (c) 2026 kraynux - Licence MIT
"""Garde-fous purs du crawl distant (OMEGA-FOLD_SPECIFICATIONS.md §4.2/
§8.2) — aucune E/S, testable sans reseau. Emplacement choisi :
`domain/scans/policies.py`, pas `application/pipeline/guards/
crawl_guard.py` comme le suggerait `OMEGA-FOLD_ARBORESCENCE.md` §2 (aucun
`application/pipeline/` n'existe chez omega-check/omega-deep ; le
precedent direct est `omega_deep.domain.discovery.policies` — memes
garde-fous purs de decouverte, D-003 — meme emplacement logique)."""
from __future__ import annotations

from urllib.parse import urlparse


def is_depth_allowed(current_depth: int, max_depth: int) -> bool:
    """True si une page a la profondeur `current_depth` peut encore etre
    suivie (ses propres liens explores) sans depasser `max_depth`."""
    return current_depth < max_depth


def is_page_count_allowed(current_count: int, max_pages: int) -> bool:
    """True si une page de plus peut etre ajoutee a la file de crawl
    sans depasser `max_pages` (deja visitees + en file)."""
    return current_count < max_pages


def is_same_domain(url: str, base_domain: str) -> bool:
    """True si `url` appartient au meme domaine que `base_domain` (le
    domaine de la cible racine) — comparaison du `netloc` (host[:port]),
    insensible a la casse. Un `url` sans netloc (chemin relatif/absolu,
    pas une URL complete) est considere comme appartenant au meme domaine
    (c'est deja une page du meme site par construction)."""
    netloc = urlparse(url).netloc
    if not netloc:
        return True
    return netloc.lower() == base_domain.lower()


def normalize_distant_target(target: str) -> str:
    """Complete une cible distante sans schema avec `https://` (defaut
    moderne, meme convention qu'un navigateur pour une saisie du type
    "example.org" dans la barre d'adresse). Sans ceci, `urlparse` d'une
    chaine sans schema renvoie un `netloc` vide — `run_scan_distant`
    echoue silencieusement a determiner le domaine de base et le premier
    `fetch()` lui-meme echoue (aucun schema a resoudre)."""
    stripped = target.strip()
    if stripped.lower().startswith(("http://", "https://")):
        return stripped
    return f"https://{stripped}"
