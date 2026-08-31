# Copyright (c) 2026 kraynux - Licence MIT
"""Use case (lecture pure) : construire un nom de fichier d'export explicite
et horodate ('scan-{cible-nettoyee}-{date}.ext'). Plus simple que
CHECK/DEEP : FOLD n'a pas de notion de profil, seulement une cible."""
from __future__ import annotations

import re
from datetime import datetime

from omega_fold.domain.scans.models import Scan

_EXTENSIONS = {"json": "json", "text": "txt", "html": "html"}
_UNSAFE_CHARS = re.compile(r"[^a-zA-Z0-9._-]+")


def _sanitize_target(target: str) -> str:
    cleaned = _UNSAFE_CHARS.sub("-", target.strip()).strip("-")
    return (cleaned or "scan")[:60]


def build_export_filename(scan: Scan, fmt: str) -> str:
    date_str = datetime.fromisoformat(scan.created_at).strftime("%Y%m%d-%H%M%S")
    stem = _sanitize_target(scan.target)
    return f"scan-{stem}-{date_str}.{_EXTENSIONS[fmt]}"
