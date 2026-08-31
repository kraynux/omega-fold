import re

from omega_lib.theme.policies import EXPORT_PALETTES

from omega_fold.domain.stats.models import FamilyStats
from omega_fold.infrastructure.exporters.family_chart import render_family_bar_chart

_PALETTE = EXPORT_PALETTES["omega-base"]


def test_render_family_bar_chart_empty_returns_empty_string() -> None:
    assert render_family_bar_chart([], _PALETTE) == ""


def test_render_family_bar_chart_produces_valid_svg() -> None:
    stats = [
        FamilyStats(family="code", files_count=3, total_size=300, percentage_of_total=75.0),
        FamilyStats(family="images", files_count=1, total_size=100, percentage_of_total=25.0),
    ]

    svg = render_family_bar_chart(stats, _PALETTE)

    assert svg.startswith("<svg")
    assert svg.endswith("</svg>")
    assert svg.count("<rect") == 2
    assert "code (3)" in svg
    assert "images (1)" in svg


def test_render_family_bar_chart_bars_stay_within_declared_width() -> None:
    stats = [FamilyStats(family="code", files_count=1, total_size=999999, percentage_of_total=100.0)]

    svg = render_family_bar_chart(stats, _PALETTE)

    width_match = re.search(r'width="(\d+)"', svg)
    assert width_match is not None
    declared_width = int(width_match.group(1))

    for match in re.finditer(r'<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)"', svg):
        x, bar_width = float(match.group(1)), float(match.group(2))
        assert x + bar_width < declared_width
