from datetime import UTC, datetime
from pathlib import Path

from omega_fold.application.commands.run_scan import run_scan_local
from omega_fold.core.enums import LinkStatus, LinkType, ScanMode
from omega_fold.infrastructure.filesystem.local_fs_walker import LocalFsWalker
from omega_fold.infrastructure.network.bs4_link_extractor import Bs4LinkExtractor


def _build_site(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text(
        """
        <html><body>
          <a href="/about.html">About</a>
          <a href="/missing.html">Missing</a>
          <a href="https://example.org">External</a>
          <img src="img/logo.png">
        </body></html>
        """,
        encoding="utf-8",
    )
    (tmp_path / "about.html").write_text("<html><body>About page</body></html>", encoding="utf-8")
    img_dir = tmp_path / "img"
    img_dir.mkdir()
    (img_dir / "logo.png").write_bytes(b"\x89PNG" + b"0" * 96)


def test_run_scan_local_end_to_end(tmp_path: Path) -> None:
    _build_site(tmp_path)

    result = run_scan_local(
        root_path=str(tmp_path),
        scan_mode=ScanMode.STATIC,
        local_fs_reader=LocalFsWalker(),
        html_link_extractor=Bs4LinkExtractor(),
        id_factory=lambda: "test-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
    )

    scan = result.scan
    assert scan.id == "test-scan-id"
    assert scan.status == "completed"
    assert scan.total_files == 3  # index.html, about.html, logo.png
    assert scan.total_links == 4
    assert scan.internal_links == 3  # /about.html, /missing.html, img/logo.png
    assert scan.external_links == 1
    assert scan.broken_links == 1

    assert result.root_dir is not None
    assert len(result.broken_links) == 1
    assert result.broken_links[0].url == "/missing.html"

    about_link = next(link for link in result.links if link.url == "/about.html")
    assert about_link.link_type == LinkType.ABSOLUTE
    assert about_link.status == LinkStatus.EXISTS
    assert about_link.target_exists is True

    external_link = next(link for link in result.links if link.link_type == LinkType.EXTERNAL)
    assert external_link.status == LinkStatus.UNCHECKED  # jamais verifie en local

    assert result.external_domains[0].domain == "example.org"

    family_names = {stats.family for stats in result.family_stats}
    assert family_names == {"code", "images"}
