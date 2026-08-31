# Copyright (c) 2026 kraynux - Licence MIT
"""Rendu d'un histogramme SVG (repartition des fichiers par famille, en
taille) pour l'export HTML — meme technique que
`graph_layout.py` d'omega-deep (D-009) : mise en page calculee ici en
Python, aucune dependance de charting lourde, `width`/`height` fixes a la
taille naturelle du graphique (pas "100%" — un petit jeu de familles ne
doit pas s'etirer pour remplir la largeur de la page).

N'importe PAS jinja2 (voir html_exporter.py, seul module autorise a le
faire) : construit une chaine `<svg>...</svg>` complete et autonome,
directement embarquee par le template via `| safe`. Les noms de famille
proviennent d'un catalogue interne ferme (`domain/stats/families.py`),
jamais d'une entree utilisateur — `xml.sax.saxutils.escape` est tout de
meme applique par prudence (meme discipline que DEEP)."""
from __future__ import annotations

from xml.sax.saxutils import escape

from omega_lib.theme.policies import Palette

from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.stats.models import FamilyStats

_BAR_HEIGHT = 26
_BAR_GAP = 12
_LABEL_WIDTH = 110
_VALUE_WIDTH = 90
"""Colonne reservee a droite de chaque barre pour son etiquette de taille
("12345 o") — sans elle, une barre a sa longueur maximale (famille la
plus lourde) pousse son etiquette hors du `viewBox`, coupee au rendu."""
_CHART_WIDTH = 420
_MARGIN = 20


def render_family_bar_chart(family_stats: list[FamilyStats], palette: Palette) -> str:
    if not family_stats:
        return ""

    max_size = max(stats.total_size for stats in family_stats) or 1
    bar_area_width = _CHART_WIDTH - _LABEL_WIDTH - _VALUE_WIDTH - _MARGIN
    row_height = _BAR_HEIGHT + _BAR_GAP
    height = _MARGIN * 2 + len(family_stats) * row_height - _BAR_GAP
    width = _CHART_WIDTH

    parts: list[str] = [
        (
            f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Repartition par famille">'
        )
    ]

    for index, stats in enumerate(family_stats):
        y = _MARGIN + index * row_height
        bar_width = max(2.0, (stats.total_size / max_size) * bar_area_width)
        label = escape(f"{stats.family} ({stats.files_count})")
        parts.append(
            f'<text x="0" y="{y + _BAR_HEIGHT / 2 + 4:.1f}" font-size="11" '
            f'font-family="ui-monospace, monospace" fill="{palette.foreground}">{label}</text>'
        )
        parts.append(
            f'<rect x="{_LABEL_WIDTH}" y="{y}" width="{bar_width:.1f}" height="{_BAR_HEIGHT}" '
            f'fill="{palette.accent}" rx="3"/>'
        )
        size_label = escape(format_size(stats.total_size))
        parts.append(
            f'<text x="{_LABEL_WIDTH + bar_width + 6:.1f}" y="{y + _BAR_HEIGHT / 2 + 4:.1f}" '
            f'font-size="10" font-family="ui-monospace, monospace" fill="{palette.secondary}">{size_label}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)
