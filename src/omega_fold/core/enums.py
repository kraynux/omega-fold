# Copyright (c) 2026 kraynux - Licence MIT
"""Vocabulaire transverse : enums utilises par toutes les couches.

ConfidenceLevel n'est PAS defini ici : il vient de omega_lib.core.confidence
(voir OMEGA-FOLD_ARBORESCENCE.md §1 et ~/DEV/SUITE/DECISIONS_ARCHITECTURE.md
D-005). Re-exporte ici pour que le reste de omega_fold importe tout son
vocabulaire transverse depuis un seul endroit (`omega_fold.core.enums`)
sans se soucier de la frontiere omega-lib/omega-fold — meme convention
que omega_check.core.enums/omega_deep.core.enums.
"""
from __future__ import annotations

from enum import Enum

from omega_lib.core.confidence import ConfidenceLevel

__all__ = ["ConfidenceLevel", "LinkStatus", "LinkType", "ScanMode", "ScanTargetType"]


class ScanTargetType(str, Enum):
    LOCAL = "local"
    DISTANT = "distant"


class ScanMode(str, Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"


class LinkType(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
    ANCHOR = "anchor"
    MAILTO = "mailto"
    TEL = "tel"
    JAVASCRIPT = "javascript"
    DATA = "data"
    EMPTY = "empty"


class LinkStatus(str, Enum):
    EXISTS = "exists"
    BROKEN = "broken"
    REDIRECT = "redirect"
    TIMEOUT = "timeout"
    ERROR = "error"
    UNCHECKED = "unchecked"
