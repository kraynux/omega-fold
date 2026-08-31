import json
from pathlib import Path

from omega_fold.app.bootstrap import bootstrap
from omega_fold.interfaces.cli.main import run


def _build_site(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text(
        '<html><body><a href="/about.html">About</a><a href="/missing.html">Missing</a></body></html>',
        encoding="utf-8",
    )
    (root / "about.html").write_text("<html><body>About</body></html>", encoding="utf-8")


def test_scan_history_and_show_round_trip(tmp_path: Path) -> None:
    site = tmp_path / "site"
    _build_site(site)

    container = bootstrap(var_dir=tmp_path / "var", console_logging=False)
    try:
        exit_code = run(container, ["scan", str(site), "--type", "local"])
        assert exit_code == 0

        history = container.scan_repository.list_history()
        assert len(history) == 1
        scan_id = history[0].id
        assert scan_id is not None

        assert run(container, ["history"]) == 0

        assert run(container, ["show", scan_id, "--format", "text"]) == 0
        assert run(container, ["show", scan_id, "--format", "json"]) == 0

        output_path = tmp_path / "report.html"
        assert run(container, ["show", scan_id, "--format", "html", "--output", str(output_path)]) == 0
        assert output_path.exists()
        assert "OMEGA-FOLD" in output_path.read_text(encoding="utf-8")
    finally:
        container.close()


def test_show_unknown_scan_id_returns_error_exit_code(tmp_path: Path) -> None:
    container = bootstrap(var_dir=tmp_path / "var", console_logging=False)
    try:
        exit_code = run(container, ["show", "does-not-exist"])
        assert exit_code == 1
    finally:
        container.close()


def test_history_json_export_is_valid(tmp_path: Path, capsys) -> None:
    site = tmp_path / "site"
    _build_site(site)

    container = bootstrap(var_dir=tmp_path / "var", console_logging=False)
    try:
        run(container, ["scan", str(site), "--type", "local"])
        scan_id = container.scan_repository.list_history()[0].id
        capsys.readouterr()

        run(container, ["show", scan_id, "--format", "json"])
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["scan"]["id"] == scan_id
        assert payload["scan"]["total_files"] == 2
    finally:
        container.close()
