# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation composite du port ReportExporter, delegue aux modules
specifiques par format — seul point d'entree expose a app/bootstrap.py."""
from __future__ import annotations

from omega_lib.theme.policies import DEFAULT_EXPORT_THEME

from omega_fold.domain.reports.models import ScanResult
from omega_fold.infrastructure.exporters.html_exporter import export_html
from omega_fold.infrastructure.exporters.json_exporter import export_json
from omega_fold.infrastructure.exporters.text_exporter import export_text


class CompositeReportExporter:
    """Implemente ports/report_exporter.py::ReportExporter."""

    def export_json(self, result: ScanResult) -> str:
        return export_json(result)

    def export_text(self, result: ScanResult) -> str:
        return export_text(result)

    def export_html(self, result: ScanResult, theme_name: str = DEFAULT_EXPORT_THEME) -> str:
        return export_html(result, theme_name)
