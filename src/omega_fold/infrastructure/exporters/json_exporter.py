# Copyright (c) 2026 kraynux - Licence MIT
"""Export JSON. `dataclasses.asdict` suffit pour l'integralite de
l'agregat `ScanResult` (contrairement au stockage SQLite qui doit
aplatir en colonnes) : les enums str (LinkStatus/LinkType/ConfidenceLevel/
ScanMode/ScanTargetType) sont serialisees nativement par `json.dumps`
sous leur valeur texte."""
from __future__ import annotations

import json
from dataclasses import asdict

from omega_fold.domain.reports.models import ScanResult


def export_json(result: ScanResult) -> str:
    return json.dumps(asdict(result), indent=2, ensure_ascii=False)
