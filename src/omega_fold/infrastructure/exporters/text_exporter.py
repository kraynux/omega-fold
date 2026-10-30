# Copyright (c) 2026 kraynux - Licence MIT
"""Export TXT (rapport, avec arborescence ASCII). Distinct de
interfaces/cli/formatters/text_formatter.py (affichage ephemere de
console, plus compact) — les deux ont vocation a diverger."""
from __future__ import annotations

from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.tree.models import DirEntry
from omega_fold.shared.i18n import _

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
        _("=== OMEGA-FOLD — Rapport de scan ==="),
        _("Scan ID       : {id}").format(id=scan.id),
        _("Cible         : {target}").format(target=scan.target),
        _("Type          : {value}").format(value=scan.target_type.value),
        _("Date          : {created_at}").format(created_at=scan.created_at),
        _("Mode          : {value}").format(value=scan.scan_mode.value),
        _("Statut        : {status}").format(status=scan.status),
        *(
            [
                "",
                _("ATTENTION : limite --max-pages atteinte, le site a probablement plus de"),
                _("pages que ce qui est rapporté ici — relancer avec --max-pages plus élevé."),
            ]
            if scan.status == "completed_truncated"
            else []
        ),
        "",
        # Taille totale du site en premier : c'est l'information la plus
        # attendue d'un rapport de scan (objectif premier, avant tout le
        # reste — demande explicite de l'utilisateur), format lisible
        # (Ko/Mo/Go...) plutot que le nombre brut d'octets.
        _("Taille totale : {value}").format(value=format_size(scan.total_size)),
        _("Fichiers      : {total_files}").format(total_files=scan.total_files),
        _("Répertoires   : {total_dirs}").format(total_dirs=scan.total_dirs),
        _("Profondeur max: {max_depth}").format(max_depth=scan.max_depth),
        "",
        _("Liens totaux  : {total_links}").format(total_links=scan.total_links),
        _("Liens internes: {internal_links}").format(internal_links=scan.internal_links),
        _("Liens externes: {external_links}").format(external_links=scan.external_links),
        _("Liens cassés  : {broken_links}").format(broken_links=scan.broken_links),
        "",
    ]

    if result.family_stats:
        lines.append(_("=== Répartition par famille ==="))
        for stats in result.family_stats:
            lines.append(
                _("  {family:<12} {files_count:>5} fichier(s)  {value:>10}  "
                  "({percentage_of_total:.1f}%)").format(family=stats.family, files_count=stats.files_count, value=format_size(stats.total_size), percentage_of_total=stats.percentage_of_total)
            )
        lines.append("")

    if result.extension_stats:
        lines.append(_("=== Répartition par extension ==="))
        for ext in result.extension_stats:
            lines.append(
                _("  {value:<16} {files_count:>5} fichier(s)  {value2:>10}  "
                  "({percentage_of_total:.1f}%)").format(value=ext.extension or _("(sans extension)"), files_count=ext.files_count, value2=format_size(ext.total_size), percentage_of_total=ext.percentage_of_total)
            )
        lines.append("")

    if result.root_dir is not None:
        lines.append(_("=== Arborescence ==="))
        lines.extend(render_tree_lines(result.root_dir))
        lines.append("")

    if result.broken_links:
        lines.append(_("=== Liens cassés ==="))
        for link in result.broken_links:
            lines.append(_("  {url}  (trouvé dans {source_file})").format(url=link.url, source_file=link.source_file))
        lines.append("")

    return "\n".join(lines)
