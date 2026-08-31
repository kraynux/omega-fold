# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran Aide : reference statique des raccourcis et fonctions de
l'application. Adapte du patron screens/help_screen.py de CHECK/DEEP
(D-007/D-008) — le tableau des profils systeme (sans equivalent FOLD)
est remplace par le catalogue des familles de fichiers
(`domain/stats/families.py::FAMILIES`)."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_fold.domain.stats.families import FAMILIES
from omega_fold.interfaces.tui.screens._base import OmegaScreen

_SHORTCUTS = (
    ("Haut / Bas", "Naviguer entre les elements d'un ecran"),
    ("Tab / Maj+Tab", "Naviguer entre les champs d'un formulaire"),
    ("Echap", "Retour a l'ecran precedent (confirmation de sortie sur l'accueil)"),
    ("t", "Theme suivant (applique immediatement, sans confirmation)"),
    ("r", "Rafraichir la detection du terminal"),
    ("a", "Cette aide"),
    ("q", "Quitter (avec confirmation)"),
)

_SECTIONS = (
    (
        "Scanner",
        (
            "Saisir une cible (repertoire local ou URL), le type (local/distant), le mode "
            "(statique ou dynamique) et, pour un scan distant, les garde-fous de crawl "
            "(profondeur max, nombre de pages, delai entre requetes, User-Agent, respect de "
            "robots.txt)."
        ),
    ),
    (
        "Historique",
        (
            "Liste tous les scans passes : detail complet (arborescence, familles, liens "
            "casses), ou rejouer un scan sur la meme cible (un scan distant rejoue utilise "
            "les garde-fous par defaut, pas ceux du scan original — non persistes)."
        ),
    ),
    (
        "Export",
        (
            "Depuis le detail d'un scan : JSON (structure complete), texte (rapport compact) "
            "ou HTML (rapport visuel avec histogramme par famille, theme d'export independant "
            "du theme de l'interface)."
        ),
    ),
)

_SCOPE_NOTICE = (
    "Omega-fold analyse un repertoire local ou crawle un site distant sous des garde-fous "
    "toujours actifs (profondeur, nombre de pages, delai, meme domaine) : un lien externe "
    "n'est verifie par HTTP qu'en mode dynamique, un lien interne est toujours verifie contre "
    "les fichiers/pages reellement trouves, jamais par supposition."
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static("AIDE", classes="omega-title")
            yield Static("Raccourcis clavier", classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(f"{key:<14} {description}")
            yield Static("")
            yield Static("Fonctions", classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static("Familles de fichiers", classes="omega-subtitle")
            yield DataTable(id="family-table")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"), Container(classes="omega-btn-frame"):
                yield Button("Retour", id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#family-table", DataTable)
        table.add_columns("Famille", "Extensions")
        for family, extensions in FAMILIES.items():
            table.add_row(family, ", ".join(extensions) if extensions else "(le reste)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
