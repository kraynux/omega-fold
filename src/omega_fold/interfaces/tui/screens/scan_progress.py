# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran de progression : lance le scan choisi sans bloquer l'UI. Repond
soi-meme au dispatch local/distant plutot que d'appeler `run_scan()`
(application/commands/run_scan.py) : `run_scan_local` est synchrone
(`os.walk` reel) et doit etre enveloppe dans `asyncio.to_thread` pour ne
pas geler l'event loop Textual, alors que `run_scan_distant` est deja
`async` nativement et peut etre `await`e directement — `run_scan()`
lui-meme ne fait pas cette distinction (il appelle `run_scan_local`
directement, sans `to_thread`, ce qui est correct pour la CLI mais
bloquerait le TUI le temps du parcours).

Relais des logs emis par `run_scan.py` (logger 'omega_fold.scan') vers le
RichLog du ProgressPanel, meme mecanisme que CHECK/DEEP — avec UNE
difference : `Textual.App.call_from_thread` leve `RuntimeError` s'il est
appele DEPUIS le thread de l'app elle-meme (reserve aux appels
cross-thread). Un scan LOCAL journalise depuis le thread `asyncio.
to_thread` (cross-thread, `call_from_thread` correct) mais un scan
DISTANT journalise directement depuis le thread de l'app (`run_scan_
distant` est `await`e sur l'event loop de l'app, jamais dans un thread
separe) — `_on_log_record` doit donc distinguer les deux cas plutot que
d'appeler `call_from_thread` sans condition (bug reel trouve via un test
manuel de scan distant, corrige ici)."""
from __future__ import annotations

import asyncio
import logging
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button

from omega_fold.application.commands.run_scan import run_scan_distant, run_scan_local
from omega_fold.core.enums import ScanMode, ScanTargetType
from omega_fold.interfaces.tui.screens.show_detail import ShowDetailScreen
from omega_fold.interfaces.tui.widgets.progress_panel import ProgressPanel

if TYPE_CHECKING:
    from textual.worker import Worker

    from omega_fold.app.dependency_container import DependencyContainer


class _RelayHandler(logging.Handler):
    """Relaie chaque record du logger 'omega_fold.scan' vers un callback,
    sans formattage, juste le message."""

    def __init__(self, callback: Callable[[str], None]) -> None:
        super().__init__()
        self._callback = callback

    def emit(self, record: logging.LogRecord) -> None:
        self._callback(record.getMessage())


class ScanProgressScreen(Screen[None]):
    """Ecran transitoire : disparait des que le scan se termine (succes
    -> ShowDetailScreen remplace cet ecran)."""

    def __init__(
        self,
        *,
        container: DependencyContainer,
        target: str,
        target_type: ScanTargetType,
        scan_mode: ScanMode,
        max_depth: int,
        max_pages: int,
        delay_ms: int,
        user_agent: str,
        respect_robots: bool,
    ) -> None:
        super().__init__()
        self._container = container
        self._target = target
        self._target_type = target_type
        self._scan_mode = scan_mode
        self._max_depth = max_depth
        self._max_pages = max_pages
        self._delay_ms = delay_ms
        self._user_agent = user_agent
        self._respect_robots = respect_robots
        self._app_thread_id = threading.get_ident()
        self._worker: Worker[None] | None = None

    def compose(self) -> ComposeResult:
        yield ProgressPanel(message=f"Scan de {self._target} en cours...")

    def on_mount(self) -> None:
        self._worker = self.run_worker(self._run_scan(), exclusive=True)

    async def _run_scan(self) -> None:
        container = self._container
        logger = logging.getLogger("omega_fold.scan")
        handler = _RelayHandler(self._on_log_record)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        try:
            if self._target_type == ScanTargetType.LOCAL:
                result = await asyncio.to_thread(
                    run_scan_local,
                    root_path=self._target,
                    scan_mode=self._scan_mode,
                    local_fs_reader=container.local_fs_reader,
                    html_link_extractor=container.html_link_extractor,
                    id_factory=container.id_factory,
                    now=container.clock,
                    scan_repository=container.scan_repository,
                )
            else:
                result = await run_scan_distant(
                    base_url=self._target,
                    scan_mode=self._scan_mode,
                    max_depth=self._max_depth,
                    max_pages=self._max_pages,
                    delay_ms=self._delay_ms,
                    user_agent=self._user_agent,
                    respect_robots=self._respect_robots,
                    distant_crawler=container.distant_crawler,
                    html_link_extractor=container.html_link_extractor,
                    link_checker=container.link_checker,
                    id_factory=container.id_factory,
                    now=container.clock,
                    scan_repository=container.scan_repository,
                )
        except Exception as exc:
            # rate ne doit jamais laisser l'utilisateur bloque SANS EXPLICATION sur cet
            # ecran transitoire (voir widgets/progress_panel.py::mark_failed) — journalise
            # aussi la trace complete (pas seulement le message) pour un vrai diagnostic
            # a posteriori dans var/app.log, meme raisonnement que app.py::_handle_exception.
            logging.getLogger("omega_fold").error("Scan echoue (%s)", self._target, exc_info=exc)
            self.query_one(ProgressPanel).mark_failed(str(exc) or type(exc).__name__)
            return
        finally:
            logger.removeHandler(handler)

        self.app.switch_screen(ShowDetailScreen(container=container, result=result))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "progress-back":
            self.dismiss()
        elif event.button.id == "progress-cancel":
            # Un scan distant peut etre long sur un site enorme, rien
            # n'empechait auparavant d'attendre jusqu'au bout ou l'echec
            # (demande explicite de l'utilisateur). `Worker.cancel()` leve
            # `asyncio.CancelledError` au prochain point d'attente dans
            # `_run_scan` — jamais rattrapee par le `except Exception`
            # ci-dessus (CancelledError est une BaseException depuis
            # Python 3.8, pas une Exception), le `finally` (nettoyage du
            # handler de log) s'execute quand meme normalement. Pour un
            # scan LOCAL (enveloppe dans `asyncio.to_thread`), le thread
            # sous-jacent continue jusqu'a sa fin naturelle en arriere-plan
            # (Python ne peut pas tuer un thread de force) — sans
            # consequence, son resultat est simplement jete a son retour.
            if self._worker is not None:
                self._worker.cancel()
            self.app.notify("Scan annule.", title="Annulation")
            self.dismiss()

    def _on_log_record(self, message: str) -> None:
        if threading.get_ident() == self._app_thread_id:
            # Scan distant : `run_scan_distant` est `await`e sur l'event loop de
            # l'app elle-meme, pas dans un thread separe — `call_from_thread`
            # lever ait `RuntimeError` s'il etait appele ici (reserve au cas
            # cross-thread ci-dessous, scan local via `asyncio.to_thread`).
            self._write_log_line(message)
        else:
            self.app.call_from_thread(self._write_log_line, message)

    def _write_log_line(self, message: str) -> None:
        if self.is_mounted:
            self.query_one(ProgressPanel).write_line(message)
