# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'reports' : assemblage complet du resultat d'un scan
(OMEGA-FOLD_SPECIFICATIONS.md §2.10). Formes de donnees pures — construit
par l'orchestration applicative une fois le scan (local ou distant)
termine, pas de logique ici."""
from __future__ import annotations

from dataclasses import dataclass, field

from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.scans.models import Scan
from omega_fold.domain.stats.models import ExtensionStats, ExternalDomainStats, FamilyStats, TopFile
from omega_fold.domain.tree.models import DirEntry


@dataclass
class ScanResult:
    scan: Scan
    root_dir: DirEntry | None = None  # pour un scan local
    links: list[LinkEntry] = field(default_factory=list)
    extension_stats: list[ExtensionStats] = field(default_factory=list)
    family_stats: list[FamilyStats] = field(default_factory=list)
    top_files_by_size: list[TopFile] = field(default_factory=list)
    top_files_by_links: list[TopFile] = field(default_factory=list)
    external_domains: list[ExternalDomainStats] = field(default_factory=list)
    broken_links: list[LinkEntry] = field(default_factory=list)
