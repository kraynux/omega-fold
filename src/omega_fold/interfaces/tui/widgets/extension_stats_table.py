# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau de repartition par extension (type/nombre/taille), demande
explicitement en complement de FamilyStatsTable (plus grossiere, par
famille) — meme donnees que la colonne "Extensions" de l'export HTML."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.stats.models import ExtensionStats


class ExtensionStatsTable(DataTable[str]):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Extension", "Fichiers", "Taille", "%")

    def set_extension_stats(self, stats: list[ExtensionStats]) -> None:
        self.clear()
        for entry in stats:
            self.add_row(
                entry.extension or "(sans extension)",
                str(entry.files_count),
                format_size(entry.total_size),
                f"{entry.percentage_of_total:.1f}%",
                key=entry.extension or "-",
            )
