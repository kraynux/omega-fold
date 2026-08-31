# Copyright (c) 2026 kraynux - Licence MIT
"""Arborescence d'un resultat de scan, via le widget `Tree` natif de
Textual. Population EAGER (pas de chargement paresseux) : les arbres de
FOLD restent d'une taille geree sans probleme par `Tree`, pas de
sur-ingenierie ici (aucun autre outil de la suite n'a eu besoin d'un
arbre de fichiers avant FOLD, pas de patron a porter)."""
from __future__ import annotations

from textual.widgets import Tree
from textual.widgets.tree import TreeNode

from omega_fold.domain.tree.models import DirEntry


class TreeView(Tree[str]):
    """`data` de chaque noeud porte le chemin (repertoire ou fichier),
    non exploite pour l'instant (pas de selection de fichier prevue) mais
    disponible pour une extension future sans changer la structure."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__("/", **kwargs)  # type: ignore[arg-type]

    def set_root_dir(self, root: DirEntry) -> None:
        self.clear()
        self.root.set_label(f"{root.path}/")
        self.root.data = root.path
        self._populate(self.root, root)
        self.root.expand()

    def _populate(self, node: TreeNode[str], entry: DirEntry) -> None:
        for child in sorted(entry.children, key=lambda d: d.name):
            child_node = node.add(f"{child.name}/", data=child.path)
            self._populate(child_node, child)
        for file in sorted(entry.files, key=lambda f: f.name):
            node.add_leaf(f"{file.name} ({file.size} o)", data=file.path)
