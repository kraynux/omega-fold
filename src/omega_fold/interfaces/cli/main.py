# Copyright (c) 2026 kraynux - Licence MIT
"""Dispatch CLI (scan/history/show — OMEGA-FOLD_ARBORESCENCE.md §2).

Ne demarre pas l'application lui-meme : __main__.py appelle bootstrap()
puis run(container, argv). `scan_command.handle_scan` est la seule
commande async de la CLI (`run_scan` est async, voir
application/commands/run_scan.py) — `run()` detecte ce cas via
`inspect.iscoroutinefunction` plutot que de forcer tout le reste de la
CLI (history/show, purement synchrones) a devenir async."""
from __future__ import annotations

import argparse
import asyncio
import inspect
import sys
from typing import TYPE_CHECKING

from omega_fold.interfaces.cli.commands import history_command, scan_command, show_command
from omega_fold.interfaces.cli.formatters.text_formatter import format_error

if TYPE_CHECKING:
    from omega_fold.app.dependency_container import DependencyContainer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omega-fold", description="Analyse de structure de site/repertoire (local et distant)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_command.register(subparsers)
    history_command.register(subparsers)
    show_command.register(subparsers)
    return parser


def run(container: DependencyContainer, argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if inspect.iscoroutinefunction(args.handler):
            result = asyncio.run(args.handler(args, container))
        else:
            result = args.handler(args, container)
    except Exception as exc:  # noqa: BLE001 — filet de securite generique (meme choix que CHECK/DEEP)
        print(format_error(str(exc)), file=sys.stderr)
        return 1

    print(result)
    return 0
