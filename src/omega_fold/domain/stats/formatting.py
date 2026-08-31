# Copyright (c) 2026 kraynux - Licence MIT
"""Formatage humain d'une taille en octets (ex. `1900000000` -> "1.8 Go").
Pure (aucune E/S), reutilisee par la CLI, le TUI et les exporteurs — la
taille totale d'un site est l'information la plus attendue d'un rapport
(demande explicite de l'utilisateur, avec un exemple de rapport bash en
reference : "1.9G" affiche bien plus lisiblement que le nombre brut
d'octets, en particulier pour un site de plusieurs gigaoctets)."""
from __future__ import annotations

_UNITS: tuple[str, ...] = ("o", "Ko", "Mo", "Go", "To", "Po")


def format_size(size_bytes: int) -> str:
    size = float(size_bytes)
    for unit in _UNITS[:-1]:
        if abs(size) < 1024:
            return f"{int(size)} {unit}" if unit == "o" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} {_UNITS[-1]}"
