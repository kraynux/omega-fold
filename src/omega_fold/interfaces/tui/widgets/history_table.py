# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau de l'historique des scans (adapte du patron CHECK/DEEP,
D-007/D-008)."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_fold.domain.scans.models import Scan
from omega_fold.domain.stats.formatting import format_size


class HistoryTable(DataTable[str]):
    """Une ligne par scan passe, le plus recent en premier."""

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Cible", "Type", "Date", "Statut", "Taille", "Fichiers", "Liens")

    def set_scans(self, scans: tuple[Scan, ...]) -> None:
        self.clear()
        for scan in scans:
            assert scan.id is not None
            self.add_row(
                scan.target,
                scan.target_type.value,
                scan.created_at,
                scan.status,
                format_size(scan.total_size),
                str(scan.total_files),
                str(scan.total_links),
                key=scan.id,
            )
