# Copyright (c) 2026 kraynux - Licence MIT
"""Bounded context 'links' : un lien trouve dans un fichier/une page
(`<a href>`, `<img src>`, `<script src>`, etc.)."""
from __future__ import annotations

from dataclasses import dataclass

from omega_fold.core.enums import ConfidenceLevel, LinkStatus, LinkType


@dataclass
class LinkEntry:
    url: str
    link_type: LinkType
    source_file: str  # fichier ou page ou le lien a ete trouve
    attribute: str  # "href", "src", "action"
    status: LinkStatus = LinkStatus.UNCHECKED
    status_code: int | None = None  # code HTTP (si verifie)
    error_message: str | None = None
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    target_exists: bool | None = None  # pour liens internes : le fichier existe-t-il ?
