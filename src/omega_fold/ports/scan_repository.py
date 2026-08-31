# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de persistance et d'historique des scans (voir
~/DEV/SUITE/DECISIONS_ARCHITECTURE.md D-006 : scan_id en UUID, colonne
`tool`, DB separee par outil pour l'instant ;
OMEGA-FOLD_SPECIFICATIONS.md §7.1 pour le schema complet : tables
scans/files/dirs/links/extension_stats/family_stats/top_files/
external_domains)."""
from __future__ import annotations

from typing import Protocol

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.models import Scan


class ScanRepository(Protocol):
    """Implemente par infrastructure/storage/sqlite/scan_repository.py."""

    def save(self, scan: Scan) -> None: ...

    def get(self, scan_id: str) -> Scan | None: ...

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]: ...

    def clear(self) -> None: ...

    def save_result(self, scan_id: str, result: ScanResult) -> None:
        """Persiste l'agregat complet (arborescence, liens, statistiques)
        associe a `scan_id`. Remplace tout resultat deja associe a ce
        scan."""
        ...

    def get_result(self, scan_id: str) -> ScanResult | None: ...
