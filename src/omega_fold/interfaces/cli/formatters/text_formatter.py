# Copyright (c) 2026 kraynux - Licence MIT
"""Mise en forme texte simple pour la CLI (affichage ephemere de console,
distinct de infrastructure/exporters/text_exporter.py — voir sa docstring)."""
from __future__ import annotations

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.stats.formatting import format_size


def format_scan_result(result: ScanResult) -> str:
    scan = result.scan
    lines = [
        f"Scan {scan.id} — cible {scan.target} ({scan.target_type.value}) — statut {scan.status}",
        f"  taille totale: {format_size(scan.total_size)}  fichiers: {scan.total_files}  repertoires: {scan.total_dirs}",
        (
            f"  liens: {scan.total_links} (internes: {scan.internal_links}, "
            f"externes: {scan.external_links}, casses: {scan.broken_links})"
        ),
    ]
    if scan.status == "completed_truncated":
        lines.append(
            "  ATTENTION : limite --max-pages atteinte, le site a probablement plus de "
            "pages que ce qui est rapporte ici — relancer avec --max-pages plus eleve."
        )
    return "\n".join(lines)


def format_error(message: str) -> str:
    return f"erreur : {message}"
