# Copyright (c) 2026 kraynux - Licence MIT
"""Rendu de l'arborescence en HTML natif multi-niveaux (`<details>`
imbriques, un par repertoire) pour l'export HTML — demande explicite de
l'utilisateur, inspiree de son propre script `generate_cd_index.py` :
seule la racine est ouverte par defaut, chaque sous-repertoire se
developpe independamment au clic. Pour un site enorme (des dizaines de
milliers de fichiers), c'est le seul rendu qui reste utilisable : le
contenu d'un `<details>` ferme n'est ni affiche ni mis en page par le
navigateur tant qu'il n'est pas ouvert (optimisation native, aucun
JavaScript necessaire) — contrairement a l'arborescence ASCII a plat de
text_exporter.py (utile pour un rapport texte, mais imposerait de tout
afficher d'un coup en HTML).

N'importe PAS jinja2 (voir html_exporter.py, seul module autorise a le
faire) : construit une chaine HTML complete, directement embarquee par
le template via `| safe`. Noms de fichiers/repertoires echappes
systematiquement (`html.escape`) : pour un scan DISTANT, ce sont des
segments d'URL d'un serveur tiers, jamais dignes de confiance par
defaut (meme discipline que family_chart.py/graph_layout.py d'omega-deep)."""
from __future__ import annotations

from html import escape

from omega_fold.domain.stats.formatting import format_size
from omega_fold.domain.tree.models import DirEntry


def render_tree_html(root: DirEntry) -> str:
    return _render_dir(root, is_root=True)


def _render_dir(entry: DirEntry, *, is_root: bool) -> str:
    children_html = "".join(
        _render_dir(child, is_root=False) for child in sorted(entry.children, key=lambda d: d.name)
    )
    files_html = "".join(
        (
            f'<div class="tree-file">📄 <span>{escape(file.name)}</span> '
            f'<span class="tree-file-size">({escape(format_size(file.size))})</span></div>'
        )
        for file in sorted(entry.files, key=lambda f: f.name)
    )

    label = escape(entry.path if is_root else entry.name)
    meta = escape(f"{entry.files_count} fichier(s) direct(s), {format_size(entry.total_size)}")
    open_attr = " open" if is_root else ""

    return (
        f'<details class="tree-folder"{open_attr}>'
        f'<summary>📁 {label}/ <span class="tree-folder-meta">({meta})</span></summary>'
        f'<div class="tree-folder-body">{children_html}{files_html}</div>'
        f"</details>"
    )
