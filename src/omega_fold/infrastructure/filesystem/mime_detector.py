# Copyright (c) 2026 kraynux - Licence MIT
"""Detection MIME via le module standard `mimetypes` (voir
OMEGA-FOLD_ARBORESCENCE.md §5, note dependance : `python-magic` (precis
mais necessite `libmagic` au niveau systeme, friction de packaging) ecarte
au profit de `mimetypes` (zero dependance systeme) — a revisiter
uniquement si la precision s'avere insuffisante en pratique.

`is_binary_mime` vit desormais dans domain/stats/policies.py (pure,
reutilisable par application/commands/run_scan.py, voir sa docstring)."""
from __future__ import annotations

import mimetypes


def detect_mime_type(path: str) -> str | None:
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type
