# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de detail d'un scan : resume + repartition par famille +
arborescence + liens casses + export. Adapte de screens/show_detail.py
de CHECK/DEEP (D-007/D-008) — vocabulaire propre a FOLD (pas de
ports/services/roles ni de graphe d'architecture)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Static

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.stats.formatting import format_size
from omega_fold.interfaces.tui.screens._base import OmegaScreen
from omega_fold.interfaces.tui.screens.export_dialog import ExportDialogScreen
from omega_fold.interfaces.tui.widgets.broken_links_table import BrokenLinksTable
from omega_fold.interfaces.tui.widgets.extension_stats_table import ExtensionStatsTable
from omega_fold.interfaces.tui.widgets.family_stats_table import FamilyStatsTable
from omega_fold.interfaces.tui.widgets.tree_view import TreeView
from omega_fold.shared.i18n import _

if TYPE_CHECKING:
    from omega_fold.app.dependency_container import DependencyContainer


class ShowDetailScreen(OmegaScreen):
    def __init__(self, *, container: DependencyContainer, result: ScanResult) -> None:
        super().__init__()
        self._container = container
        self._result = result

    def compose(self) -> ComposeResult:
        scan = self._result.scan
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("SCAN {id}").format(id=scan.id), classes="omega-title")
            yield Static(
                _("Cible : {target} ({value}) — mode {value2} — statut {status}").format(target=scan.target, value=scan.target_type.value, value2=scan.scan_mode.value, status=scan.status),
                classes="omega-subtitle",
            )
            yield Static(
                _("[b]{value}[/b] — {total_files} fichier(s) — {total_dirs} répertoire(s) — "
                  "profondeur max {max_depth} — {total_links} lien(s) ({broken_links} cassé(s))").format(value=format_size(scan.total_size), total_files=scan.total_files, total_dirs=scan.total_dirs, max_depth=scan.max_depth, total_links=scan.total_links, broken_links=scan.broken_links),
                classes="omega-subtitle",
            )
            if scan.status == "completed_truncated":
                yield Static(
                    _("[$warning]⚠ Limite --max-pages atteinte : le site a probablement plus "
                      "de pages que ce qui est rapporté ici. Rejouer avec un --max-pages plus "
                      "élevé pour une couverture complète.[/]"),
                    classes="omega-subtitle",
                )

            yield Static(_("Répartition par famille"), classes="omega-subtitle")
            yield FamilyStatsTable(id="family-table")

            yield Static(_("Répartition par extension"), classes="omega-subtitle")
            yield ExtensionStatsTable(id="extension-table")

            yield Static(_("Arborescence"), classes="omega-subtitle")
            yield TreeView(id="tree-view", classes="omega-tree-view")

            yield Static(_("Liens cassés"), classes="omega-subtitle")
            yield BrokenLinksTable(id="broken-links-table")

            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Exporter"), id="export", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(FamilyStatsTable).set_family_stats(self._result.family_stats)
        self.query_one(ExtensionStatsTable).set_extension_stats(self._result.extension_stats)
        self.query_one(BrokenLinksTable).set_links(self._result.broken_links)
        if self._result.root_dir is not None:
            self.query_one(TreeView).set_root_dir(self._result.root_dir)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id == "export":
            self.app.push_screen(
                ExportDialogScreen(container=self._container, scan=self._result.scan, active_theme=self.app.theme)
            )
