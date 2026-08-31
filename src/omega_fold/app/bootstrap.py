# Copyright (c) 2026 kraynux - Licence MIT
"""Racine de composition : construit un DependencyContainer avec les
adaptateurs concrets de production. Seul module autorise a importer a la
fois infrastructure/ ET app/dependency_container.py."""
from __future__ import annotations

from pathlib import Path

from omega_lib.infrastructure.terminal.detector import SystemTerminalDetector
from omega_lib.shared.clock import utc_now
from omega_lib.shared.ids import new_id

from omega_fold.app.dependency_container import DependencyContainer
from omega_fold.infrastructure.config import paths
from omega_fold.infrastructure.exporters.exporter import CompositeReportExporter
from omega_fold.infrastructure.filesystem.local_fs_walker import LocalFsWalker
from omega_fold.infrastructure.logging.config import APP_LOG_FILENAME, configure_logging
from omega_fold.infrastructure.network.aiohttp_crawler import AiohttpCrawler
from omega_fold.infrastructure.network.bs4_link_extractor import Bs4LinkExtractor
from omega_fold.infrastructure.network.http_link_checker import HttpLinkChecker
from omega_fold.infrastructure.storage.files.json_settings_store import JsonSettingsStore
from omega_fold.infrastructure.storage.sqlite.connection import open_connection
from omega_fold.infrastructure.storage.sqlite.scan_repository import SqliteScanRepository


def bootstrap(*, var_dir: Path | None = None, console_logging: bool = True) -> DependencyContainer:
    """`console_logging=False` pour le TUI : Textual prend le controle
    exclusif de l'ecran, une ecriture de log directe sur stderr pendant
    un scan corromprait son rendu. Le CLI garde `console_logging=True`
    par defaut."""
    base = var_dir if var_dir is not None else paths.resolve_var_dir()
    configure_logging(log_path=base / APP_LOG_FILENAME, console=console_logging)
    connection = open_connection(paths.default_db_path(base))
    exports_dir = paths.default_exports_dir(base)
    screenshots_dir = paths.default_screenshots_dir(base)

    return DependencyContainer(
        local_fs_reader=LocalFsWalker(),
        html_link_extractor=Bs4LinkExtractor(),
        distant_crawler=AiohttpCrawler(),
        link_checker=HttpLinkChecker(),
        scan_repository=SqliteScanRepository(connection),
        report_exporter=CompositeReportExporter(),
        settings_store=JsonSettingsStore(paths.default_settings_path(base)),
        terminal_detector=SystemTerminalDetector(),
        default_exports_dir=exports_dir,
        default_screenshots_dir=screenshots_dir,
        id_factory=new_id,
        clock=utc_now,
        connection=connection,
    )
