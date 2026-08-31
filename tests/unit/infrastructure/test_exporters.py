import json

from omega_fold.core.enums import LinkStatus, LinkType, ScanMode, ScanTargetType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.models import Scan
from omega_fold.domain.stats.models import ExternalDomainStats, FamilyStats
from omega_fold.domain.tree.models import DirEntry, FileEntry
from omega_fold.infrastructure.exporters.exporter import CompositeReportExporter
from omega_fold.infrastructure.exporters.html_exporter import export_html
from omega_fold.infrastructure.exporters.json_exporter import export_json
from omega_fold.infrastructure.exporters.text_exporter import export_text


def _scan() -> Scan:
    return Scan(
        id="scan-1",
        created_at="2026-08-31T00:00:00+00:00",
        target="/tmp/site",
        target_type=ScanTargetType.LOCAL,
        scan_mode=ScanMode.STATIC,
        status="completed",
        total_files=2,
        total_dirs=1,
        total_size=42,
        max_depth=1,
        total_links=2,
        internal_links=1,
        external_links=1,
        broken_links=1,
    )


def _result() -> ScanResult:
    subdir = DirEntry(
        path="/tmp/site/assets",
        name="assets",
        depth=1,
        files_count=1,
        dirs_count=0,
        total_size=10,
        files=[FileEntry(path="/tmp/site/assets/style.css", name="style.css", extension=".css", size=10, depth=1, family="code")],
    )
    root = DirEntry(
        path="/tmp/site",
        name="site",
        depth=0,
        files_count=1,
        dirs_count=1,
        total_size=52,
        children=[subdir],
        files=[FileEntry(path="/tmp/site/index.html", name="index.html", extension=".html", size=42, depth=0, family="code")],
    )
    broken = LinkEntry(
        url="/missing.html", link_type=LinkType.ABSOLUTE, source_file="/tmp/site/index.html",
        attribute="href", status=LinkStatus.BROKEN, target_exists=False,
    )
    return ScanResult(
        scan=_scan(),
        root_dir=root,
        links=[broken],
        family_stats=[FamilyStats(family="code", files_count=1, total_size=42, percentage_of_total=100.0)],
        external_domains=[ExternalDomainStats(domain="example.org", links_count=1)],
        broken_links=[broken],
    )


def test_export_json_round_trips_via_json_loads() -> None:
    output = export_json(_result())
    parsed = json.loads(output)

    assert parsed["scan"]["id"] == "scan-1"
    assert parsed["root_dir"]["files"][0]["name"] == "index.html"
    assert parsed["broken_links"][0]["url"] == "/missing.html"


def test_export_text_contains_key_facts() -> None:
    output = export_text(_result())
    assert "scan-1" in output
    assert "site/" in output
    assert "index.html" in output
    assert "/missing.html" in output


def test_export_text_handles_missing_root_dir() -> None:
    result = _result()
    result.root_dir = None
    output = export_text(result)
    assert "Arborescence" not in output


def test_export_html_renders_tree_and_chart() -> None:
    output = export_html(_result())
    assert "OMEGA-FOLD" in output
    assert "index.html" in output
    assert "<svg" in output
    assert "/missing.html" in output


def test_export_html_renders_multi_level_collapsible_tree() -> None:
    """Regression : l'arborescence multi-niveaux (un `<details>` par
    repertoire, inspiree du script generate_cd_index.py de l'utilisateur)
    doit ouvrir la RACINE par defaut mais laisser chaque sous-repertoire
    FERME — sans quoi un site enorme afficherait tout d'un coup ("page
    d'un kilometre", signale par l'utilisateur)."""
    output = export_html(_result())
    assert "tree-folder" in output
    root_pos = output.index('<details class="tree-folder" open>')
    subdir_pos = output.index('<details class="tree-folder">')  # "assets", sans "open"
    assert root_pos < subdir_pos
    assert "assets/" in output
    assert "style.css" in output


def test_export_html_wraps_broken_links_in_collapsed_details() -> None:
    """Regression : une liste de liens casses volumineuse rendait la page
    "d'un kilometre" (signale par l'utilisateur) — cette section doit
    etre repliee par defaut (`<details>` sans `open`), pas affichee en
    clair."""
    output = export_html(_result())
    broken_links_summary_pos = output.index("Afficher les 1 lien(s) casse(s)")
    details_before_broken = output.rindex("<details", 0, broken_links_summary_pos)
    assert output[details_before_broken : details_before_broken + 20] == '<details class="box"'


def test_export_html_caps_external_domains_to_top_20_with_expandable_rest() -> None:
    """Regression : un site avec des centaines de domaines externes lies
    (redirections/permaliens) rendait la page ingerable — top 20 affiches
    directement, le reste dans un `<details>` replie."""
    result = _result()
    result.external_domains = [
        ExternalDomainStats(domain=f"site{i}.example", links_count=30 - i) for i in range(25)
    ]
    output = export_html(result)

    assert "Domaines externes lies (25)" in output
    assert "site19.example" in output  # 20eme (index 19), encore visible directement
    assert "Voir les 5 domaine(s) restant(s)" in output
    # site24 (le dernier, 25eme) est bien present mais SEULEMENT dans la section repliee
    visible_part = output[: output.index("Voir les 5 domaine(s) restant(s)")]
    assert "site24.example" not in visible_part
    assert "site24.example" in output


def test_export_html_uses_requested_export_theme_palette() -> None:
    from omega_lib.theme.policies import EXPORT_PALETTES

    output = export_html(_result(), theme_name="omega-neon")
    assert EXPORT_PALETTES["omega-neon"].background in output
    assert EXPORT_PALETTES["omega-base"].background not in output


def test_export_html_unknown_theme_falls_back_to_default() -> None:
    from omega_lib.theme.policies import EXPORT_PALETTES

    output = export_html(_result(), theme_name="does-not-exist")
    assert EXPORT_PALETTES["omega-base"].background in output


def test_composite_exporter_delegates_to_each_format() -> None:
    exporter = CompositeReportExporter()
    result = _result()
    assert exporter.export_json(result) == export_json(result)
    assert exporter.export_text(result) == export_text(result)
    assert exporter.export_html(result, "omega-neon") == export_html(result, "omega-neon")
