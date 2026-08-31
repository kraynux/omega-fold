# Copyright (c) 2026 kraynux - Licence MIT
"""Tests structurels du TUI (Textual Pilot) : verifie que l'app demarre,
que chaque ecran du menu principal s'ouvre/se ferme, et qu'un scan local
reel (via tmp_path, pas mocke) aboutit au detail attendu — aucune
verification visuelle (le pipeline SVG->rsvg-convert->PNG est connu peu
fiable pour ce jeu de caracteres, cf. la meme note deja actee cote
CHECK/DEEP ; une revue visuelle reelle se fait en direct avec
l'utilisateur, pas ici)."""
from __future__ import annotations

import time
from pathlib import Path

import pytest
from pytest_httpserver import HTTPServer
from textual.widgets import Input, Select, Static
from werkzeug.wrappers import Request, Response

from omega_fold.app.bootstrap import bootstrap
from omega_fold.interfaces.tui.app import OmegaFoldApp
from omega_fold.interfaces.tui.screens.export_dialog import ExportDialogScreen
from omega_fold.interfaces.tui.screens.help_screen import HelpScreen
from omega_fold.interfaces.tui.screens.history import HistoryScreen
from omega_fold.interfaces.tui.screens.home import HomeScreen
from omega_fold.interfaces.tui.screens.scan_setup import ScanSetupScreen
from omega_fold.interfaces.tui.screens.settings_screen import SettingsScreen
from omega_fold.interfaces.tui.screens.show_detail import ShowDetailScreen
from omega_fold.interfaces.tui.screens.splash import SplashScreen
from omega_fold.interfaces.tui.widgets.family_stats_table import FamilyStatsTable


@pytest.fixture
def app(tmp_path: Path) -> OmegaFoldApp:
    container = bootstrap(var_dir=tmp_path, console_logging=False)
    app = OmegaFoldApp(container)
    app._test_container = container  # type: ignore[attr-defined]
    return app


async def test_splash_then_home(app: OmegaFoldApp) -> None:
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        assert isinstance(app.screen, SplashScreen)
        await pilot.press("space")
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)
    app._test_container.close()  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    ("button_id", "expected_screen"),
    [
        ("scan", ScanSetupScreen),
        ("history", HistoryScreen),
        ("settings", SettingsScreen),
        ("help", HelpScreen),
    ],
)
async def test_home_menu_opens_and_closes_each_screen(
    app: OmegaFoldApp, button_id: str, expected_screen: type
) -> None:
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        await pilot.press("space")  # dismiss splash
        await pilot.pause()

        await pilot.click(f"#{button_id}")
        await pilot.pause()
        assert isinstance(app.screen, expected_screen)

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)
    app._test_container.close()  # type: ignore[attr-defined]


async def test_full_local_scan_reaches_show_detail(app: OmegaFoldApp, tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text(
        '<html><body><a href="/about.html">About</a><a href="/missing.html">Missing</a></body></html>',
        encoding="utf-8",
    )
    (site / "about.html").write_text("<html><body>About</body></html>", encoding="utf-8")

    async with app.run_test(size=(120, 80)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()

        await pilot.click("#scan")
        await pilot.pause()
        assert isinstance(app.screen, ScanSetupScreen)

        target_input = app.screen.query_one("#target-input")
        target_input.value = str(site)
        await pilot.pause()

        await pilot.click("#launch")
        # laisse le worker de scan se terminer (scan local reel, rapide sur ce petit site)
        await pilot.pause(0.5)
        for _ in range(20):
            if isinstance(app.screen, ShowDetailScreen):
                break
            await pilot.pause(0.2)

        assert isinstance(app.screen, ShowDetailScreen)
        family_table = app.screen.query_one(FamilyStatsTable)
        assert family_table.row_count > 0
    app._test_container.close()  # type: ignore[attr-defined]


async def test_history_view_after_scan(app: OmegaFoldApp, tmp_path: Path) -> None:
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<html><body>hello</body></html>", encoding="utf-8")

    async with app.run_test(size=(120, 80)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()

        await pilot.click("#scan")
        await pilot.pause()
        app.screen.query_one("#target-input").value = str(site)
        await pilot.pause()
        await pilot.click("#launch")
        await pilot.pause(0.5)
        for _ in range(20):
            if isinstance(app.screen, ShowDetailScreen):
                break
            await pilot.pause(0.2)
        assert isinstance(app.screen, ShowDetailScreen)

        # La pile est Home -> ScanSetup -> ShowDetail (switch_screen remplace
        # ScanProgressScreen, pousse sur ScanSetup, sans repasser par Home) :
        # un echap ramene a ScanSetup, un second a Home.
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, ScanSetupScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)

        await pilot.click("#history")
        await pilot.pause()
        assert isinstance(app.screen, HistoryScreen)

        history_table = app.screen.query_one("#history-table")
        assert history_table.row_count == 1
    app._test_container.close()  # type: ignore[attr-defined]


async def test_settings_theme_persistence(app: OmegaFoldApp) -> None:
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        await pilot.click("#settings")
        await pilot.pause()
        assert isinstance(app.screen, SettingsScreen)

        stored = app._test_container.settings_store.get("theme")  # type: ignore[attr-defined]
        assert stored is None  # rien de persiste avant tout changement explicite
    app._test_container.close()  # type: ignore[attr-defined]


async def test_theme_cycle_binding(app: OmegaFoldApp) -> None:
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        initial_theme = app.theme
        await pilot.press("t")
        await pilot.pause()
        assert app.theme != initial_theme
    app._test_container.close()  # type: ignore[attr-defined]


async def test_quit_confirm_flow(app: OmegaFoldApp) -> None:
    async with app.run_test(size=(100, 40)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        await pilot.press("q")
        await pilot.pause()
        assert app.screen.__class__.__name__ == "QuitConfirmScreen"
        # QuitConfirmScreen ne declare aucun binding "escape" (porte verbatim
        # depuis CHECK/DEEP) : seul un clic explicite sur un des deux boutons
        # dismiss() l'ecran.
        await pilot.click("#cancel")
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)
    app._test_container.close()  # type: ignore[attr-defined]


async def test_distant_scan_reaches_show_detail_without_thread_error(
    app: OmegaFoldApp, httpserver: HTTPServer
) -> None:
    """Regression : un scan DISTANT journalise depuis le thread de l'app
    elle-meme (`run_scan_distant` est `await`e sur son event loop, jamais
    dans un `asyncio.to_thread` comme le scan local) — appeler
    `call_from_thread` sans condition dans ce cas levait `RuntimeError`
    ('must run in a different thread from the app'), laissant
    l'utilisateur bloque sur ScanProgressScreen (voir screens/
    scan_progress.py::ScanProgressScreen._on_log_record)."""
    httpserver.expect_request("/").respond_with_data(
        '<html><body><a href="/about">a</a></body></html>', content_type="text/html"
    )
    httpserver.expect_request("/about").respond_with_data("<html><body>about</body></html>", content_type="text/html")
    base_url = httpserver.url_for("/")

    async with app.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        await pilot.click("#scan")
        await pilot.pause()

        app.screen.query_one("#target-input", Input).value = base_url
        app.screen.query_one("#type-select", Select).value = "distant"
        await pilot.pause()

        await pilot.click("#launch")
        await pilot.pause(0.5)
        for _ in range(30):
            if isinstance(app.screen, ShowDetailScreen):
                break
            await pilot.pause(0.3)

        assert isinstance(app.screen, ShowDetailScreen)
    app._test_container.close()  # type: ignore[attr-defined]


async def test_scan_setup_shows_explicit_field_labels(app: OmegaFoldApp) -> None:
    """Regression : les champs de garde-fous (profondeur/pages/delai/
    user-agent) etaient pre-remplis d'une valeur par defaut sans aucune
    etiquette visible (le `placeholder` d'un Input ne s'affiche que si le
    champ est vide) — impossible de savoir a quoi "5" ou "1000"
    correspondait (signale par l'utilisateur)."""
    async with app.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        await pilot.click("#scan")
        await pilot.pause()

        label_texts = {str(s.render()) for s in app.screen.query(".omega-field-label").results(Static)}
        for expected in ("Type", "Mode", "Profondeur max", "Pages max", "Delai entre requetes (ms)", "User-Agent"):
            assert expected in label_texts
    app._test_container.close()  # type: ignore[attr-defined]


async def test_cancel_button_stops_scan_and_returns_without_reaching_detail(app: OmegaFoldApp) -> None:
    """Regression : rien ne permettait d'annuler un scan en cours, un
    scan distant potentiellement long forcait a attendre jusqu'au bout ou
    l'echec (demande explicite de l'utilisateur)."""

    def _slow_handler(request: Request) -> Response:
        time.sleep(2.0)
        return Response("<html><body>trop tard</body></html>", content_type="text/html")

    server = HTTPServer(threaded=True)
    server.start()
    try:
        server.expect_request("/").respond_with_handler(_slow_handler)
        base_url = server.url_for("/")

        async with app.run_test(size=(120, 60)) as pilot:
            await pilot.pause()
            await pilot.press("space")
            await pilot.pause()
            await pilot.click("#scan")
            await pilot.pause()

            app.screen.query_one("#target-input", Input).value = base_url
            app.screen.query_one("#type-select", Select).value = "distant"
            await pilot.pause()

            await pilot.click("#launch")
            await pilot.pause(0.3)  # le scan est lance, la page /  n'a pas encore repondu (sleep 2s)

            await pilot.click("#progress-cancel")
            await pilot.pause()

            assert isinstance(app.screen, ScanSetupScreen)
            # meme apres le delai du handler lent, jamais atteint ShowDetailScreen
            await pilot.pause(2.2)
            assert isinstance(app.screen, ScanSetupScreen)
    finally:
        server.stop()
    app._test_container.close()  # type: ignore[attr-defined]


async def test_history_export_button_opens_export_dialog_directly(app: OmegaFoldApp, tmp_path: Path) -> None:
    """Regression : exporter un scan passe depuis l'historique necessitait
    de passer par "Voir le detail" — demande explicite d'un bouton
    Exporter direct sur l'ecran Historique lui-meme."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "index.html").write_text("<html><body>hello</body></html>", encoding="utf-8")

    async with app.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()

        await pilot.click("#scan")
        await pilot.pause()
        app.screen.query_one("#target-input", Input).value = str(site)
        await pilot.pause()
        await pilot.click("#launch")
        await pilot.pause(0.5)
        for _ in range(20):
            if isinstance(app.screen, ShowDetailScreen):
                break
            await pilot.pause(0.2)
        assert isinstance(app.screen, ShowDetailScreen)

        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, ScanSetupScreen)
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, HomeScreen)

        await pilot.click("#history")
        await pilot.pause()
        history_screen = app.screen
        assert isinstance(history_screen, HistoryScreen)
        scan_id = next(iter(history_screen._scans_by_id))
        history_screen._selected_scan_id = scan_id

        await pilot.click("#export")
        await pilot.pause()
        assert isinstance(app.screen, ExportDialogScreen)
    app._test_container.close()  # type: ignore[attr-defined]
