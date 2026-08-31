# Copyright (c) 2026 kraynux - Licence MIT
"""Composition ASCII de l'ecran de demarrage, fournie par l'utilisateur
(~/DEV/FOLD/ascii.txt, lignes 13-33) — caracteres non modifies, lignes
brutes conservees telles quelles (`rstrip()` uniquement, AUCUN
recentrage : reconstruire ligne par ligne casserait l'alignement entre
les elements, meme lecon que la correction du splash d'omega-deep cette
session).

Regles de couleur litterales du fichier source :
- Bordures ("container clair") -> $foreground.
- Texte "LINUX FOLDER ANALYSE" -> $accent (vif).
- Bandeau OMEGA-FOLD encadre : 1ere/3eme ligne interne vif, 2eme clair
  (identique a widgets/home_wordmark.py).
- Tagline : "|" vif, mots clair.
- Degrade a 2 tons/2 intensites sur les caracteres de remplissage :
  '█'=clair (`$foreground`), '▓'=un ton en dessous (`dim $foreground`),
  '▒'=encore en dessous (`$secondary`), '░'=encore en dessous
  (`dim $secondary`) — interpretation directe de "conserve les nuances
  des deux tons sur meme blocs", assomption documentee ici, facile a
  ajuster si la lecture ne correspond pas a l'intention de l'utilisateur
  (meme discipline que les decorations sans regle explicite de CHECK).
- Deux voyants explicitement vif, reperes par position exacte plutot que
  deduits d'un motif general : le '▓' isole ligne 11 ('║▓║', bas
  d'ecran) et les '█' isoles a l'INTERIEUR du rack serveur (lignes 12/14/
  16 — distincts des '█' qui forment les parois du rack, celles-la
  restant '$foreground' via la regle generale)."""
from __future__ import annotations

from textual.widgets import Static

_RAW_LINES: tuple[str, ...] = (
    '                          ┌────────────────────────┐',
    '                          │  LINUX FOLDER ANALYSE  │',
    '                          └────────────────────────┘',
    '                               ┌▄█████████████▄┐',
    '                               │████▒V1.00▒████│',
    '┌────────────────────────────────────────────────────────────────────────────┐',
    '│ ┌╦═══╦┐ ┌╦═╦═╦┐ ┌╦═══╦┐ ┌╦═══╦┐ ┌╦═══╦┐    ┌╦═══╦┐ ┌╦═══╦┐ ┌╦      ┌╦╦══╦┐ │',
    '│ │║   ║│ │║ ║ ║│ ├╬══    │║  ═╦┐ ├╬═══╬┤ ═  ├╬══    │║   ║│ │║      │║║  ║│ │',
    '│ └╩═══╩┘ └╩   ╩┘ └╩═══╩┘ └╩═══╩┘ └╩   ╩┘    └╩      └╩═══╩┘ └╩═══╩┘ └╩╩══╩┘ │',
    '└────────────────────────────────────────────────────────────────────────────┘',
    '                               └███████████████┘    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄',
    '          ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄           ║▓║          ╔█░░░░░░░░░░░░█┐',
    '          █┌─────────────┐█       ┌╦═══════╦┐      ║█░▒▓█▒░░▒▓▓▒░█│',
    '          █│~/tree░░░░░░░│█       └╩═══════╩┘      ║█░░░░░░░░░░░░█│',
    '          █│http:/░░░░░░░│█╗         ║│ │║         ║█░▒▓▓▒░░▒▓█▒░█│',
    '          █└─────────────┘█╠═════════╩┘ │║         ║█░░░░░░░░░░░░█│',
    '          ████████▓████████╝            └╩═════════╣█░▒█▓▒░░▒█▓▒░█│',
    '                ║███║                              ╚█░░░░░░░░░░░░█┘',
    '           ╠█░░░░░░░░░░░█╣                          ██████████████',
    '',
    '             SCAN | FOLDER | NETWORKS | LOCAL | ANALYSE | EXPORT',
)
"""Indices 0-20 = lignes originales 13-33 de ascii.txt."""

_ACCENT_TEXT_SPAN = (1, 29, 49)
"""(ligne, colonne_debut, colonne_fin_exclusive) : "LINUX FOLDER ANALYSE"."""

_WORDMARK_ACCENT_LINES = (6, 8)
"""Lignes 1 et 3 du bandeau OMEGA-FOLD encadre (vif) — tout le contenu
entre les deux parois '│' (colonnes 1 a len-2)."""

_TAGLINE_LINE = 20

_ACCENT_POSITIONS: frozenset[tuple[int, int]] = frozenset({
    (11, 39),  # '▓' isole dans '║▓║', voyant bas d'ecran
    (12, 56),  # '█' interieur rack serveur, rangee 1
    (14, 62),  # '█' interieur rack serveur, rangee 2
    (16, 55),  # '█' interieur rack serveur, rangee 3 (1er voyant)
    (16, 61),  # '█' interieur rack serveur, rangee 3 (2eme voyant)
})

_STYLE_TOKENS: dict[str, str] = {
    "accent": "$accent",
    "foreground": "$foreground",
    "foreground-dim": "dim $foreground",
    "secondary": "$secondary",
    "secondary-dim": "dim $secondary",
}


def _default_style(char: str) -> str:
    if char == "█":
        return "foreground"
    if char == "▓":
        return "foreground-dim"
    if char == "▒":
        return "secondary"
    if char == "░":
        return "secondary-dim"
    return "foreground"


def _classify(line_index: int, col_index: int, char: str, line_length: int) -> str:
    if (line_index, col_index) in _ACCENT_POSITIONS:
        return "accent"
    span_line, start, end = _ACCENT_TEXT_SPAN
    if line_index == span_line and start <= col_index < end:
        return "accent"
    if line_index in _WORDMARK_ACCENT_LINES and 0 < col_index < line_length - 1:
        return "accent"
    if line_index == _TAGLINE_LINE and char == "|":
        return "accent"
    return _default_style(char)


def _render_line(line_index: int, line: str) -> str:
    if not line:
        return ""
    parts: list[str] = []
    current_style: str | None = None
    current_chars: list[str] = []
    for col_index, char in enumerate(line):
        style = _classify(line_index, col_index, char, len(line))
        if style != current_style:
            if current_chars and current_style is not None:
                parts.append(f"[{_STYLE_TOKENS[current_style]}]{''.join(current_chars)}[/]")
            current_style = style
            current_chars = [char]
        else:
            current_chars.append(char)
    if current_chars and current_style is not None:
        parts.append(f"[{_STYLE_TOKENS[current_style]}]{''.join(current_chars)}[/]")
    return "".join(parts)


_MARKUP = "\n".join(_render_line(index, line) for index, line in enumerate(_RAW_LINES))


class SplashHero(Static):
    """Composition ASCII centrale de screens/splash.py."""

    def __init__(self) -> None:
        super().__init__(_MARKUP, classes="omega-splash-hero")
