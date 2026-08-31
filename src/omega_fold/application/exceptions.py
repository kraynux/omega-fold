# Copyright (c) 2026 kraynux - Licence MIT
"""Racine des erreurs de la couche application (use cases, pipeline)."""
from __future__ import annotations

from omega_fold.core.exceptions import OmegaFoldError


class ApplicationError(OmegaFoldError):
    """Racine des echecs techniques inattendus survenant dans application/
    — jamais utilisee pour un echec metier attendu (voir domain/errors.py)."""


class UnknownThemeError(ApplicationError):
    """Nom de theme demande absent du catalogue omega_lib.theme.policies.TUI_THEMES."""

    def __init__(self, theme_name: str) -> None:
        super().__init__(f"Theme inconnu : '{theme_name}'")
        self.theme_name = theme_name
