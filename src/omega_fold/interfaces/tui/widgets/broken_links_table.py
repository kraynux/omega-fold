# Copyright (c) 2026 kraynux - Licence MIT
"""Tableau des liens casses d'un resultat de scan."""
from __future__ import annotations

from textual.widgets import DataTable

from omega_fold.domain.links.models import LinkEntry


class BrokenLinksTable(DataTable[str]):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("URL", "Trouve dans")

    def set_links(self, links: list[LinkEntry]) -> None:
        self.clear()
        for index, link in enumerate(links):
            self.add_row(link.url, link.source_file, key=str(index))
