# Copyright (c) 2026 kraynux - Licence MIT
"""Classification pure d'une extension vers sa famille
(OMEGA-FOLD_SPECIFICATIONS.md §3.2). Aucune E/S."""
from __future__ import annotations

from omega_fold.domain.stats.families import FAMILIES

_OTHER = "other"


def classify_family(extension: str) -> str:
    """Priorite : premiere famille (dans l'ordre d'iteration de
    `FAMILIES`) dont la liste contient `extension` ; repli sur "other" si
    aucune ne correspond. `extension` est comparee telle quelle (deja
    normalisee en minuscules avec le point, ex. '.png') par l'appelant."""
    normalized = extension.lower()
    for family, extensions in FAMILIES.items():
        if normalized in extensions:
            return family
    return _OTHER


def is_binary_mime(mime_type: str | None) -> bool:
    """Heuristique simple : tout ce qui n'est pas `text/*` ou dans une
    courte liste de types textuels connus (JSON/XML/JS, souvent
    enregistres hors du prefixe `text/`) est considere binaire. Pure
    (opere sur une chaine MIME deja obtenue, aucune E/S) — deplacee
    depuis infrastructure/filesystem/mime_detector.py pour etre
    reutilisable aussi par application/commands/run_scan.py::
    run_scan_distant (la Dependency Rule interdit a application/
    d'importer infrastructure/)."""
    if mime_type is None:
        return False
    if mime_type.startswith("text/"):
        return False
    return mime_type not in (
        "application/json",
        "application/xml",
        "application/javascript",
        "application/x-javascript",
    )
