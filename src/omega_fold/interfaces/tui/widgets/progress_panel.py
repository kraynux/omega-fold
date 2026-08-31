# Copyright (c) 2026 kraynux - Licence MIT
"""Indicateur de progression indetermine, avec le detail des operations en
cours. Porte depuis omega-scan/omega-stress/omega-check/omega-deep
(D-007/D-008) — deux ajouts propres a FOLD, demandes explicitement :

- `mark_failed` : un scan rate doit rester VISIBLE (message d'erreur +
  bouton Retour explicite) plutot que de disparaitre derriere une
  notification ephemere et un dismiss() automatique (bug d'UX reel
  signale par l'utilisateur : un scan qui echoue pendant un rejeu depuis
  l'historique repartait silencieusement vers l'ecran precedent, sans
  que l'echec soit lisible).
- Un bouton Annuler visible DES le debut (pas d'attente possible pour un
  scan distant potentiellement long sur un site enorme) — retire au
  profit du bouton Retour des que `mark_failed` est appele (le scan est
  deja termine, annuler n'a plus de sens)."""
from __future__ import annotations

from textual.containers import Container, Horizontal, Middle
from textual.widgets import Button, LoadingIndicator, RichLog, Static


class ProgressPanel(Middle):
    """Ecran d'attente pendant l'execution d'un scan."""

    def __init__(self, *, message: str) -> None:
        super().__init__(
            Static(message, id="progress-message", classes="omega-subtitle"),
            LoadingIndicator(id="progress-spinner"),
            RichLog(classes="omega-progress-log", max_lines=200, auto_scroll=True, markup=False),
            Horizontal(
                Container(Button("Annuler", id="progress-cancel", variant="error"), classes="omega-btn-frame"),
                classes="omega-actions",
                id="progress-actions",
            ),
            classes="omega-progress-panel",
        )

    def write_line(self, line: str) -> None:
        self.query_one(RichLog).write(line)

    def mark_failed(self, message: str) -> None:
        """Remplace le spinner et le bouton Annuler par un bouton Retour
        explicite, ecrit l'erreur dans le journal (reste visible/
        scrollable, contrairement a une notification qui disparait toute
        seule)."""
        self.query_one("#progress-message", Static).update("Scan echoue")
        self.query_one("#progress-spinner", LoadingIndicator).display = False
        self.write_line(f"ERREUR : {message}")
        actions = self.query_one("#progress-actions")
        actions.remove_children()
        actions.mount(Container(Button("Retour", id="progress-back", variant="primary"), classes="omega-btn-frame"))
