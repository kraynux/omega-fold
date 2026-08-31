# Copyright (c) 2026 kraynux - Licence MIT
"""Erreurs techniques d'infrastructure (E/S) — memes conventions que
CHECK/DEEP."""
from __future__ import annotations

from omega_fold.core.exceptions import OmegaFoldError


class InfrastructureError(OmegaFoldError):
    """Racine des echecs techniques d'infrastructure (E/S)."""


class StorageError(InfrastructureError):
    """Echec de persistance (SQLite)."""
