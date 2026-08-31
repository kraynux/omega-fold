# Copyright (c) 2026 kraynux - Licence MIT
"""Re-export depuis omega_lib (D-008) : garde la convention 'importer
depuis omega_fold.ports.X' uniforme dans tout le reste du code, meme
principe que core/enums.py::ConfidenceLevel (D-005). Ajoute des la Phase 1
(contrairement a DEEP, ou ce port n'avait pas ete prevu des le depart —
oubli corrige plus tard, D-009 — pas repete ici)."""
from __future__ import annotations

from omega_lib.ports.settings_store import SettingsStore

__all__ = ["SettingsStore"]
