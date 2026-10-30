# Copyright (c) 2026 kraynux - Licence MIT
"""Lot N (langue des exports, OMEGA-SUITE_PLAN-DETAILLE_I18N.md Q5) : un rapport s'ecrit dans la
langue des exports, quelle que soit celle de l'interface."""
from __future__ import annotations

from omega_fold.infrastructure.exporters.html_exporter import export_html
from omega_fold.infrastructure.exporters.text_exporter import export_text
from omega_fold.shared.i18n import LANGUAGE, translating_as

from test_exporters import _result


def test_reports_follow_the_export_language() -> None:
    with translating_as(LANGUAGE.load_state("en")):
        html = export_html(_result())
        text = export_text(_result())
    assert '<html lang="en" dir="ltr">' in html
    assert "Scan report" in html and "Rapport de scan" not in html
    assert "Total size" in text


def test_reports_stay_in_the_interface_language_by_default() -> None:
    html = export_html(_result())
    assert '<html lang="fr" dir="ltr">' in html
    assert "Rapport de scan" in html


def test_arabic_report_is_right_to_left() -> None:
    with translating_as(LANGUAGE.load_state("ar")):
        assert 'dir="rtl"' in export_html(_result())
