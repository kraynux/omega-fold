# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau de repartition par famille (voir domain/stats/families.py)."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.stats.models import FamilyStats


class FamilyStatsTable(DataTable[str]):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Famille", "Fichiers", "Taille", "%")

    def set_family_stats(self, stats: list[FamilyStats]) -> None:
        self.clear()
        for entry in stats:
            self.add_row(
                entry.family,
                str(entry.files_count),
                format_size(entry.total_size),
                f"{entry.percentage_of_total:.1f}%",
                key=entry.family,
            )
