# Copyright (c) 2026 kraynux - Licence MIT
"""Racine des erreurs domaine (metier pur, aucune dependance externe)."""
from __future__ import annotations

from omega_fold.core.exceptions import OmegaFoldError


class DomainError(OmegaFoldError):
    """Racine de toute erreur metier attendue. Les sous-types specifiques a
    un sous-domaine vivent dans le `exceptions.py` de ce sous-domaine (ex.
    `domain/scans/exceptions.py`), pas ici."""
