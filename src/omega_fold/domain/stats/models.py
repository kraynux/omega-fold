# Copyright (c) 2026 kraynux - Licence MIT
"""Formes de donnees pures pour les statistiques d'un scan
(OMEGA-FOLD_SPECIFICATIONS.md §2.6-§2.9). Le calcul reel vit dans
`service.py` (phase ulterieure, a besoin d'un jeu de fichiers reel)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExtensionStats:
    extension: str
    files_count: int = 0
    total_size: int = 0  # en octets
    percentage_of_total: float = 0.0  # pourcentage du poids total


@dataclass
class FamilyStats:
    family: str
    files_count: int = 0
    total_size: int = 0  # en octets
    percentage_of_total: float = 0.0  # pourcentage du poids total
    extensions: list[ExtensionStats] = field(default_factory=list)


@dataclass
class TopFile:
    path: str
    size: int
    extension: str
    links_count: int = 0


@dataclass
class ExternalDomainStats:
    domain: str
    links_count: int = 0
