from datetime import UTC, datetime
from pathlib import Path

from omega_fold.application.commands.run_scan import run_scan_local
from omega_fold.core.enums import ScanMode, ScanTargetType
from omega_fold.domain.reports.models import ScanResult
from omega_fold.infrastructure.filesystem.local_fs_walker import LocalFsWalker
from omega_fold.infrastructure.network.bs4_link_extractor import Bs4LinkExtractor
from omega_fold.infrastructure.storage.sqlite.connection import open_connection
from omega_fold.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository


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


def _run_and_save(tmp_path: Path, repo: SqliteScanRepository) -> ScanResult:
    tmp_path.mkdir(parents=True, exist_ok=True)
    _build_site(tmp_path)
    return run_scan_local(
        root_path=str(tmp_path),
        scan_mode=ScanMode.STATIC,
        local_fs_reader=LocalFsWalker(),
        html_link_extractor=Bs4LinkExtractor(),
        id_factory=lambda: "test-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        scan_repository=repo,
    )


def test_save_and_get_scan(tmp_path: Path) -> None:
    connection = open_connection(tmp_path / "db.sqlite3")
    repo = SqliteScanRepository(connection)

    original = _run_and_save(tmp_path / "site", repo)

    stored = repo.get(original.scan.id)
    assert stored is not None
    assert stored.id == original.scan.id
    assert stored.target == original.scan.target
    assert stored.target_type == ScanTargetType.LOCAL
    assert stored.total_files == original.scan.total_files
    assert stored.total_links == original.scan.total_links
    assert stored.broken_links == original.scan.broken_links


def test_get_result_reconstructs_full_scan_result(tmp_path: Path) -> None:
    connection = open_connection(tmp_path / "db.sqlite3")
    repo = SqliteScanRepository(connection)

    original = _run_and_save(tmp_path / "site", repo)

    reloaded = repo.get_result(original.scan.id)
    assert reloaded is not None
    assert reloaded.scan.id == original.scan.id
    assert len(reloaded.links) == len(original.links)
    assert len(reloaded.broken_links) == len(original.broken_links)
    assert reloaded.root_dir is not None
    assert reloaded.root_dir.total_size == original.root_dir.total_size
    assert {f.family for stats in reloaded.family_stats for f in [stats]} == {
        stats.family for stats in original.family_stats
    }
    assert reloaded.external_domains and reloaded.external_domains[0].domain == "example.org"


def test_get_result_unknown_scan_returns_none(tmp_path: Path) -> None:
    connection = open_connection(tmp_path / "db.sqlite3")
    repo = SqliteScanRepository(connection)

    assert repo.get("does-not-exist") is None
    assert repo.get_result("does-not-exist") is None


def test_list_history_and_clear(tmp_path: Path) -> None:
    connection = open_connection(tmp_path / "db.sqlite3")
    repo = SqliteScanRepository(connection)

    _run_and_save(tmp_path / "site-a", repo)

    history = repo.list_history()
    assert len(history) == 1

    repo.clear()
    assert repo.list_history() == ()
    assert repo.get(history[0].id) is None
