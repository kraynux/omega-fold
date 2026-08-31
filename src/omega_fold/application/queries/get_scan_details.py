# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : recuperer le resultat complet d'un scan (arborescence,
liens, statistiques). Plus simple que omega-deep (pas de hosts/graphe
separes a assembler) : `ScanRepository.get_result` renvoie deja
l'agregat `ScanResult` complet."""
from __future__ import annotations

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.exceptions import ScanNotFoundError
from omega_fold.ports.scan_repository import ScanRepository


def get_scan_details(repo: ScanRepository, scan_id: str) -> ScanResult:
    scan = repo.get(scan_id)
    if scan is None:
        raise ScanNotFoundError(scan_id)
    result = repo.get_result(scan_id)
    assert result is not None  # coherent avec `scan` deja trouve ci-dessus
    return result
