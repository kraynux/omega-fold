# Copyright (c) 2026 kraynux - Licence MIT
"""Erreurs du bounded context 'scans'."""
from __future__ import annotations

from omega_fold.domain.errors import DomainError


class ScanNotFoundError(DomainError):
    def __init__(self, scan_id: str) -> None:
        super().__init__(f"Scan introuvable : '{scan_id}'")
        self.scan_id = scan_id
