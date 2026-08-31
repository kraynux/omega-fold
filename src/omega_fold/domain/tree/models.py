# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'tree' : arborescence filesystem (locale ou reconstruite
depuis un crawl distant). Formes de donnees pures — le parcours reel
(filesystem ou HTTP) et l'agregation de profondeur/taille vivent dans
`service.py` (phase ulterieure, a besoin de donnees reelles)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FileEntry:
    path: str
    name: str
    extension: str
    size: int  # en octets
    depth: int
    family: str  # "images", "documents", "code", etc. (voir domain/stats/families.py)
    mime_type: str | None = None
    is_binary: bool = False


@dataclass
class DirEntry:
    path: str
    name: str
    depth: int
    files_count: int = 0
    dirs_count: int = 0
    total_size: int = 0  # taille totale des fichiers dans ce repertoire (recursif)
    children: list[DirEntry] = field(default_factory=list)
    files: list[FileEntry] = field(default_factory=list)
