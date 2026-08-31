# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat d'export de rapport (OMEGA-FOLD_SPECIFICATIONS.md §9). Trois
formats en un seul port (les consommateurs choisissent le format a
l'execution, pas au moment de l'injection de dependance) — meme
convention que omega-check/omega-deep."""
from __future__ import annotations

from typing import Protocol

from omega_fold.domain.reports.models import ScanResult


class ReportExporter(Protocol):
    """Implemente par infrastructure/exporters/exporter.py."""

    def export_json(self, result: ScanResult) -> str: ...

    def export_text(self, result: ScanResult) -> str: ...

    def export_html(self, result: ScanResult, theme_name: str) -> str: ...
