# Copyright (c) 2026 kraynux - Licence MIT
"""Cablage des adaptateurs concrets derriere les ports — consomme
uniquement par app/bootstrap.py (racine de composition) et par
interfaces/ (sous TYPE_CHECKING uniquement, jamais a l'execution).

`settings_store`/`terminal_detector`/`default_screenshots_dir` cables
pour la TUI (ports deja scaffoldes Phase 1, voir leur docstring)."""
from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from omega_lib.shared.typing import IdFactory

from omega_fold.ports.distant_crawler import DistantCrawler
from omega_fold.ports.html_link_extractor import HtmlLinkExtractor
from omega_fold.ports.link_checker import LinkChecker
from omega_fold.ports.local_fs_reader import LocalFsReader
from omega_fold.ports.report_exporter import ReportExporter
from omega_fold.ports.scan_repository import ScanRepository
from omega_fold.ports.settings_store import SettingsStore
from omega_fold.ports.terminal_detector import TerminalDetector


@dataclass
class DependencyContainer:
    local_fs_reader: LocalFsReader
    html_link_extractor: HtmlLinkExtractor
    distant_crawler: DistantCrawler
    link_checker: LinkChecker
    scan_repository: ScanRepository
    report_exporter: ReportExporter
    settings_store: SettingsStore
    terminal_detector: TerminalDetector
    default_exports_dir: Path
    default_screenshots_dir: Path
    id_factory: IdFactory
    clock: Callable[[], datetime]
    connection: sqlite3.Connection

    def close(self) -> None:
        self.connection.close()
