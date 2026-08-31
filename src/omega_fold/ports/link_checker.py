# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de verification du statut d'un lien
(OMEGA-FOLD_SPECIFICATIONS.md §5.2/§5.3) — fichier local (mode
statique ou dynamique) ou HTTP HEAD/GET (mode dynamique uniquement, lien
externe). Implementation (Phase 2 pour le local, Phase 3 pour le HTTP)."""
from __future__ import annotations

from typing import Protocol

from omega_fold.core.enums import LinkStatus


class LinkChecker(Protocol):
    """Implemente par domain/links/service.py (verification locale, pure
    lecture filesystem) et infrastructure/network/http_link_checker.py
    (verification HTTP, HEAD puis GET si HEAD echoue)."""

    def check(self, url: str, *, timeout: float) -> tuple[LinkStatus, int | None, str | None]:
        """Retourne `(status, status_code, error_message)`.
        `status_code` uniquement pour une verification HTTP reussie
        (None pour un lien local). `error_message` renseigne seulement
        si `status` est `ERROR` ou `TIMEOUT`."""
        ...
