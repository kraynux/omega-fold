# Copyright (c) 2026 kraynux - Licence MIT
"""Export HTML (Jinja2 + theme d'export choisi). Seul module autorise a
importer jinja2 directement — voir contrat import-linter 'jinja2 seulement
dans infrastructure.exporters.html_exporter'."""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from omega_lib.theme.policies import DEFAULT_EXPORT_THEME

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.stats.formatting import format_size
from omega_fold.infrastructure.exporters.family_chart import render_family_bar_chart
from omega_fold.infrastructure.exporters.html_theme_resolver import resolve_export_palette
from omega_fold.infrastructure.exporters.tree_html import render_tree_html

_TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = Environment(
    loader=FileSystemLoader(_TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)
_env.filters["format_size"] = format_size


def export_html(result: ScanResult, theme_name: str = DEFAULT_EXPORT_THEME) -> str:
    template = _env.get_template("scan_report.html.j2")
    palette = resolve_export_palette(theme_name)
    chart_svg = render_family_bar_chart(result.family_stats, palette)
    tree_html = render_tree_html(result.root_dir) if result.root_dir is not None else ""
    return template.render(result=result, scan=result.scan, chart_svg=chart_svg, tree_html=tree_html, palette=palette)
