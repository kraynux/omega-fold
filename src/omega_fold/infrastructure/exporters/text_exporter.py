# Copyright (c) 2026 kraynux - Licence MIT
"""Export TXT (rapport, avec arborescence ASCII). Distinct de
interfaces/cli/formatters/text_formatter.py (affichage ephemere de
console, plus compact) — les deux ont vocation a diverger."""
from __future__ import annotations

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.tree.models import DirEntry

_MAX_TREE_DEPTH = 6
"""Profondeur maximale rendue dans l'arborescence ASCII — un rapport
texte n'a pas vocation a lister un arbre de fichiers entier sur des
milliers de lignes, contrairement au JSON (deja complet) ou au HTML
(navigable)."""


def render_tree_lines(entry: DirEntry, prefix: str = "", is_last: bool = True, depth: int = 0) -> list[str]:
    """Rendu recursif d'une arborescence ASCII a partir de `DirEntry` —
    reutilise tel quel par html_exporter.py (bloc `<pre>`) pour eviter de
    dupliquer cette logique en Jinja2 (recursion fragile a controler pour
    l'espacement en template)."""
    if depth == 0:
        lines = [f"{entry.path}/"]
    else:
        connector = "└── " if is_last else "├── "
        lines = [f"{prefix}{connector}{entry.name}/"]

    if depth >= _MAX_TREE_DEPTH:
        return lines

    child_prefix = prefix if depth == 0 else prefix + ("    " if is_last else "│   ")
    children = sorted(entry.children, key=lambda d: d.name)
    files = sorted(entry.files, key=lambda f: f.name)
    items_count = len(children) + len(files)

    for index, child in enumerate(children):
        is_last_item = index == items_count - 1
        lines.extend(render_tree_lines(child, child_prefix, is_last_item, depth + 1))

    for index, file in enumerate(files):
        is_last_item = len(children) + index == items_count - 1
        connector = "└── " if is_last_item else "├── "
        lines.append(f"{child_prefix}{connector}{file.name}")

    return lines


def export_text(result: ScanResult) -> str:
    scan = result.scan
    lines = [
        "=== OMEGA-FOLD — Rapport de scan ===",
        f"Scan ID       : {scan.id}",
        f"Cible         : {scan.target}",
        f"Type          : {scan.target_type.value}",
        f"Date          : {scan.created_at}",
        f"Mode          : {scan.scan_mode.value}",
        f"Statut        : {scan.status}",
        *(
            [
                "",
                "ATTENTION : limite --max-pages atteinte, le site a probablement plus de",
                "pages que ce qui est rapporte ici — relancer avec --max-pages plus eleve.",
            ]
            if scan.status == "completed_truncated"
            else []
        ),
        "",
        # Taille totale du site en premier : c'est l'information la plus
        # attendue d'un rapport de scan (objectif premier, avant tout le
        # reste — demande explicite de l'utilisateur), format lisible
        # (Ko/Mo/Go...) plutot que le nombre brut d'octets.
        f"Taille totale : {format_size(scan.total_size)}",
        f"Fichiers      : {scan.total_files}",
        f"Repertoires   : {scan.total_dirs}",
        f"Profondeur max: {scan.max_depth}",
        "",
        f"Liens totaux  : {scan.total_links}",
        f"Liens internes: {scan.internal_links}",
        f"Liens externes: {scan.external_links}",
        f"Liens casses  : {scan.broken_links}",
        "",
    ]

    if result.family_stats:
        lines.append("=== Repartition par famille ===")
        for stats in result.family_stats:
            lines.append(
                f"  {stats.family:<12} {stats.files_count:>5} fichier(s)  "
                f"{format_size(stats.total_size):>10}  ({stats.percentage_of_total:.1f}%)"
            )
        lines.append("")

    if result.extension_stats:
        lines.append("=== Repartition par extension ===")
        for ext in result.extension_stats:
            lines.append(
                f"  {(ext.extension or '(sans extension)'):<16} {ext.files_count:>5} fichier(s)  "
                f"{format_size(ext.total_size):>10}  ({ext.percentage_of_total:.1f}%)"
            )
        lines.append("")

    if result.root_dir is not None:
        lines.append("=== Arborescence ===")
        lines.extend(render_tree_lines(result.root_dir))
        lines.append("")

    if result.broken_links:
        lines.append("=== Liens casses ===")
        for link in result.broken_links:
            lines.append(f"  {link.url}  (trouve dans {link.source_file})")
        lines.append("")

    return "\n".join(lines)
