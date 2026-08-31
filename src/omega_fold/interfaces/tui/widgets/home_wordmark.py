# Copyright (c) 2026 kraynux - Licence MIT
"""Bandeau texte OMEGA-FOLD affiche en haut de screens/home.py (logo fourni
par l'utilisateur, voir ~/DEV/FOLD/ascii.txt — caracteres non modifies,
meme regle que les logos de CHECK/DEEP). Couleur par jetons de theme Rich/
Textual (`$accent`/`$foreground`) directement dans le markup — pas des
couleurs hex figees a la construction (meme mecanisme que
widgets/splash_hero.py : reactif au changement de theme)."""
from __future__ import annotations

from textual.widgets import Static

_WORDMARK_LINES = (
    "┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐    ┌╦═══╦┐ ┌╦═══╦┐ ┌╦      ┌╦╦══╦┐",
    "│║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═  ├╬══    │║   ║│ │║      │║║  ║│",
    "└╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘    └╩      └╩═══╩┘ └╩═══╩┘ └╩╩══╩┘",
)
"""OMEGA-FOLD en un seul bandeau de lettres, fourni par l'utilisateur
(~/DEV/FOLD/ascii.txt, lignes 44-46), caracteres non modifies."""

_MARKUP = "\n".join((
    f"[$accent]{_WORDMARK_LINES[0]}[/]",
    f"[$foreground]{_WORDMARK_LINES[1]}[/]",
    f"[$accent]{_WORDMARK_LINES[2]}[/]",
))


class HomeWordmark(Static):
    """Bandeau decoratif centre en haut de screens/home.py."""

    def __init__(self) -> None:
        super().__init__(_MARKUP, classes="omega-home-wordmark")
