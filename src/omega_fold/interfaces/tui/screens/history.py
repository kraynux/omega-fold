# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran Historique : liste des scans passes, detail, rejeu. Adapte du
patron screens/history.py de CHECK/DEEP (D-007/D-008) — pas de
comparaison (FOLD n'en a pas dans sa CLI, pas ajoutee ici sans demande
explicite).

Rejouer un scan DISTANT utilise les garde-fous PAR DEFAUT (`--max-depth`
5/`--max-pages` 1000/`--delay` 100ms, meme valeurs que scan_command.py) :
`Scan` ne persiste que la profondeur ATTEINTE (une statistique de
resultat), pas les garde-fous d'ENTREE du crawl original — les
reproduire a l'identique demanderait d'etendre le schema, pas fait sans
demande explicite (voir domain/scans/models.py::Scan)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Input, Static

from omega_fold.application.queries.get_scan_details import get_scan_details
from omega_fold.application.queries.get_scan_history import get_scan_history
from omega_fold.domain.scans.models import Scan
from omega_fold.interfaces.tui.screens._base import OmegaScreen
from omega_fold.interfaces.tui.screens.export_dialog import ExportDialogScreen
from omega_fold.interfaces.tui.widgets.history_table import HistoryTable

if TYPE_CHECKING:
    from omega_fold.app.dependency_container import DependencyContainer

_DEFAULT_MAX_DEPTH = 5
_DEFAULT_MAX_PAGES = 1000
_DEFAULT_DELAY_MS = 100
_DEFAULT_USER_AGENT = "omega-fold/0.1"


class HistoryScreen(OmegaScreen):
    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container
        self._selected_scan_id: str | None = None
        self._scans_by_id: dict[str, Scan] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-panel"):
            yield Static("HISTORIQUE", classes="omega-title")
            yield Input(placeholder="Filtrer par cible...", id="target-filter")
            yield HistoryTable(id="history-table")
            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button("Voir le detail", id="view")
                with Container(classes="omega-btn-frame"):
                    yield Button("Exporter", id="export")
                with Container(classes="omega-btn-frame"):
                    yield Button("Rejouer", id="replay")
                with Container(classes="omega-btn-frame"):
                    yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        self._refresh(None)

    def on_screen_resume(self) -> None:
        """Redemarrage de l'ecran quand un ecran pousse par-dessus (detail,
        rejeu) est retire — sans ceci, un rejeu qui echoue (ou meme un
        rejeu reussi) laisserait le tableau affiche avec les donnees
        d'AVANT le rejeu (bug d'UX reel signale par l'utilisateur : retour
        silencieux sur l'historique avec les anciennes donnees)."""
        self._refresh(self.query_one("#target-filter", Input).value.strip())

    def _refresh(self, target_filter: str | None) -> None:
        scans = get_scan_history(self._container.scan_repository, target=target_filter or None, limit=100)
        self._scans_by_id = {scan.id: scan for scan in scans if scan.id is not None}
        self.query_one(HistoryTable).set_scans(scans)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "target-filter":
            self._refresh(event.value.strip())

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._selected_scan_id = str(event.row_key.value)
        self._push_details(self._selected_scan_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if self._selected_scan_id is None:
            self.app.notify("Selectionnez d'abord une ligne.", severity="warning")
            return

        if event.button.id == "view":
            self._push_details(self._selected_scan_id)
        elif event.button.id == "export":
            self._export(self._selected_scan_id)
        elif event.button.id == "replay":
            self._replay(self._selected_scan_id)

    def _push_details(self, scan_id: str) -> None:
        from omega_fold.interfaces.tui.screens.show_detail import ShowDetailScreen

        result = get_scan_details(self._container.scan_repository, scan_id)
        self.app.push_screen(ShowDetailScreen(container=self._container, result=result))

    def _export(self, scan_id: str) -> None:
        """Export direct depuis l'historique, sans passer par l'ecran de
        detail — demande explicite de l'utilisateur (un export ne
        necessite pas de rejouer le scan, seulement de le retrouver deja
        enregistre)."""
        scan = self._scans_by_id.get(scan_id)
        if scan is None:
            self.app.notify("Scan introuvable.", severity="error")
            return
        self.app.push_screen(
            ExportDialogScreen(container=self._container, scan=scan, active_theme=self.app.theme)
        )

    def _replay(self, scan_id: str) -> None:
        from omega_fold.interfaces.tui.screens.scan_progress import ScanProgressScreen

        scan = self._scans_by_id.get(scan_id)
        if scan is None:
            self.app.notify("Scan introuvable.", severity="error")
            return
        self.app.push_screen(
            ScanProgressScreen(
                container=self._container,
                target=scan.target,
                target_type=scan.target_type,
                scan_mode=scan.scan_mode,
                max_depth=_DEFAULT_MAX_DEPTH,
                max_pages=_DEFAULT_MAX_PAGES,
                delay_ms=_DEFAULT_DELAY_MS,
                user_agent=_DEFAULT_USER_AGENT,
                respect_robots=False,
            )
        )
