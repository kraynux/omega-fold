# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : vider l'historique des scans (ecran Reglages)."""
from __future__ import annotations

from omega_fold.ports.scan_repository import ScanRepository


def clear_scan_history(*, scan_repository: ScanRepository) -> None:
    scan_repository.clear()
