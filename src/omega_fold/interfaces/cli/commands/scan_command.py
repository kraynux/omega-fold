# Copyright (c) 2026 kraynux - Licence MIT
"""Sous-commande `omega-fold scan <cible> --type local|distant
[--mode static|dynamic] [--max-depth N] [--max-pages N] [--delay MS]
[--user-agent UA] [--respect-robots]`. Seule commande async de la CLI
(voir interfaces/cli/main.py qui detecte les handlers coroutine)."""
from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from omega_fold.application.commands.run_scan import run_scan
from omega_fold.core.enums import ScanMode, ScanTargetType
from omega_fold.interfaces.cli.formatters.text_formatter import format_scan_result

if TYPE_CHECKING:
    from omega_fold.app.dependency_container import DependencyContainer


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("scan", help="Scanner une structure locale ou distante")
    parser.add_argument("target", help="Chemin local ou URL de depart")
    parser.add_argument("--type", choices=["local", "distant"], required=True, dest="target_type")
    parser.add_argument("--mode", choices=["static", "dynamic"], default="static")
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--max-pages", type=int, default=1000)
    parser.add_argument("--delay", type=int, default=100, help="Delai (ms) entre deux requetes (scan distant)")
    parser.add_argument("--user-agent", default="omega-fold/0.1")
    parser.add_argument("--respect-robots", action="store_true")
    parser.set_defaults(handler=handle_scan)


async def handle_scan(args: argparse.Namespace, container: DependencyContainer) -> str:
    target_type = ScanTargetType.LOCAL if args.target_type == "local" else ScanTargetType.DISTANT
    scan_mode = ScanMode.STATIC if args.mode == "static" else ScanMode.DYNAMIC

    result = await run_scan(
        target=args.target,
        target_type=target_type,
        scan_mode=scan_mode,
        id_factory=container.id_factory,
        now=container.clock,
        html_link_extractor=container.html_link_extractor,
        local_fs_reader=container.local_fs_reader,
        distant_crawler=container.distant_crawler,
        link_checker=container.link_checker,
        max_depth=args.max_depth,
        max_pages=args.max_pages,
        delay_ms=args.delay,
        user_agent=args.user_agent,
        respect_robots=args.respect_robots,
        scan_repository=container.scan_repository,
    )
    return format_scan_result(result)
