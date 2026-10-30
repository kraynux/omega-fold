# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de saisie : cible, type (local/distant), mode (static/dynamic) et
garde-fous de crawl distant. Adapte du patron screens/scan_setup.py de
CHECK/DEEP (D-007/D-008) — pas de picker de profil (FOLD n'en a pas), les
champs specifiques au crawl distant restent toujours visibles avec un
texte d'aide plutot qu'un affichage conditionnel (simplicite, meme choix
que le reste de la suite)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Select, Static, Switch

from omega_fold.core.enums import ScanMode, ScanTargetType
from omega_fold.interfaces.tui.screens._base import OmegaScreen
from omega_fold.interfaces.tui.screens.scan_progress import ScanProgressScreen
from omega_fold.shared.i18n import _

if TYPE_CHECKING:
    from omega_fold.app.dependency_container import DependencyContainer

_DEFAULT_MAX_DEPTH = "5"
_DEFAULT_MAX_PAGES = "1000"
_DEFAULT_DELAY_MS = "100"
_DEFAULT_USER_AGENT = "omega-fold/0.1"


class ScanSetupScreen(OmegaScreen):
    """Formulaire de lancement d'un scan."""

    def __init__(self, *, container: DependencyContainer) -> None:
        super().__init__()
        self._container = container

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(classes="omega-form-panel"):
            yield Static(_("SCANNER UNE CIBLE"), classes="omega-title")

            yield Static(_("Cible"), classes="omega-subtitle")
            yield Input(placeholder=_("ex. /var/www/monsite, https://example.org"), id="target-input")

            with Horizontal(classes="omega-form-row"):
                with Vertical(classes="omega-form-row-item"):
                    yield Static(_("Type"), classes="omega-field-label")
                    yield Select(
                        [(_("Local (répertoire)"), "local"), (_("Distant (crawl HTTP)"), "distant")],
                        value="local",
                        id="type-select",
                    )
                with Vertical(classes="omega-form-row-item-last"):
                    yield Static(_("Mode"), classes="omega-field-label")
                    yield Select(
                        [(_("Statique"), "static"), (_("Dynamique (vérifié par HTTP)"), "dynamic")],
                        value="static",
                        id="mode-select",
                    )

            yield Static(
                _("Garde-fous de crawl distant (ignorés pour un scan local)"), classes="omega-subtitle"
            )
            with Horizontal(classes="omega-form-row"):
                with Vertical(classes="omega-form-row-item"):
                    yield Static(_("Profondeur max"), classes="omega-field-label")
                    yield Input(value=_DEFAULT_MAX_DEPTH, id="max-depth-input")
                with Vertical(classes="omega-form-row-item-last"):
                    yield Static(_("Pages max"), classes="omega-field-label")
                    yield Input(value=_DEFAULT_MAX_PAGES, id="max-pages-input")
            with Horizontal(classes="omega-form-row"):
                with Vertical(classes="omega-form-row-item"):
                    yield Static(_("Délai entre requêtes (ms)"), classes="omega-field-label")
                    yield Input(value=_DEFAULT_DELAY_MS, id="delay-input")
                with Vertical(classes="omega-form-row-item-last"):
                    yield Static("User-Agent", classes="omega-field-label")
                    yield Input(value=_DEFAULT_USER_AGENT, id="user-agent-input")
            with Horizontal(classes="omega-form-row"):
                yield Static(_("Respecter robots.txt"), classes="omega-switch-label")
                yield Switch(value=False, id="respect-robots-switch")

            with Horizontal(classes="omega-actions"):
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Lancer"), id="launch", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
            return
        if event.button.id != "launch":
            return

        target = self.query_one("#target-input", Input).value.strip()
        if not target:
            self.app.notify(_("Saisissez une cible."), severity="warning")
            return

        guardrails = self._read_guardrails()
        if guardrails is None:
            return
        max_depth, max_pages, delay_ms = guardrails
        user_agent = self.query_one("#user-agent-input", Input).value.strip() or _DEFAULT_USER_AGENT
        respect_robots = self.query_one("#respect-robots-switch", Switch).value

        target_type = ScanTargetType.LOCAL if self.query_one("#type-select", Select).value == "local" else ScanTargetType.DISTANT
        scan_mode = ScanMode.STATIC if self.query_one("#mode-select", Select).value == "static" else ScanMode.DYNAMIC

        self.app.push_screen(
            ScanProgressScreen(
                container=self._container,
                target=target,
                target_type=target_type,
                scan_mode=scan_mode,
                max_depth=max_depth,
                max_pages=max_pages,
                delay_ms=delay_ms,
                user_agent=user_agent,
                respect_robots=respect_robots,
            )
        )

    def _read_guardrails(self) -> tuple[int, int, int] | None:
        try:
            max_depth = int(self.query_one("#max-depth-input", Input).value.strip() or _DEFAULT_MAX_DEPTH)
            max_pages = int(self.query_one("#max-pages-input", Input).value.strip() or _DEFAULT_MAX_PAGES)
            delay_ms = int(self.query_one("#delay-input", Input).value.strip() or _DEFAULT_DELAY_MS)
        except ValueError:
            self.app.notify(_("Profondeur/pages/délai : entiers attendus."), severity="warning")
            return None
        if max_depth < 0 or max_pages < 1 or delay_ms < 0:
            self.app.notify(_("Profondeur >= 0, pages >= 1 et délai >= 0 attendus."), severity="warning")
            return None
        return max_depth, max_pages, delay_ms
