# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'scans' : l'agregat Scan, cycle de vie d'un scan de
structure (local ou distant).

`id` est un UUID (str), pas un entier auto-incremente (D-006 : "scan_id en
UUID via omega_lib.shared.ids" s'applique a CHECK/DEEP/FOLD/SUITE) — la
version `Optional[int]` d'OMEGA-FOLD_SPECIFICATIONS.md §2.2 est un
vocabulaire non mis a jour apres D-006 (meme tolerance deja acceptee pour
les specs de CHECK/DEEP, D-001)."""
from __future__ import annotations

from dataclasses import dataclass

from omega_fold.core.enums import ScanMode, ScanTargetType


@dataclass
class Scan:
    id: str | None = None  # UUID (omega_lib.shared.ids.new_id), voir D-006
    created_at: str = ""
    target: str = ""  # chemin local ou URL distante
    target_type: ScanTargetType = ScanTargetType.LOCAL
    scan_mode: ScanMode = ScanMode.STATIC
    status: str = "running"
    """"running", "completed", "failed", ou "completed_truncated" — ce
    dernier pour un scan DISTANT arrete par `--max-pages` alors qu'il
    restait des pages en file (le site a probablement plus de pages que
    ce qui a ete rapporte ; distinct d'un arret sur `--max-depth`, qui
    borne intentionnellement la portee et n'est pas une troncature)."""

    # Statistiques globales
    total_files: int = 0
    total_dirs: int = 0
    total_size: int = 0  # en octets
    max_depth: int = 0

    # Liens
    total_links: int = 0
    internal_links: int = 0
    external_links: int = 0
    broken_links: int = 0
