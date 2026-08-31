# Copyright (c) 2026 kraynux - Licence MIT
"""Assemblage pur de l'arborescence imbriquee (`DirEntry`) a partir d'une
liste PLATE de `FileEntry` deja construite (chemin/taille/profondeur/
famille deja connus par l'appelant, voir infrastructure/filesystem/
local_fs_walker.py qui fait le parcours reel). Aucune E/S ici : le
parcours reel du filesystem est infra, l'agregation (compter/sommer par
repertoire) est domaine pur, testable avec une fausse liste de
`FileEntry`."""
from __future__ import annotations

import posixpath

from omega_fold.domain.tree.models import DirEntry, FileEntry


def build_tree(root_path: str, files: list[FileEntry]) -> DirEntry:
    """Construit l'arborescence complete sous `root_path` a partir de
    `files` (chemins absolus, deja normalises avec des '/' — voir
    l'appelant). Chaque repertoire intermediaire est cree meme s'il ne
    contient directement aucun fichier (uniquement des sous-repertoires).
    `files_count`/`dirs_count` restent des comptes DIRECTS (enfants
    immediats seulement — utile pour parcourir/afficher un niveau a la
    fois) ; `total_size` seul est recursif (somme tout le sous-arbre —
    utile pour reperer les repertoires les plus lourds)."""
    root_path = root_path.rstrip("/") or "/"
    root_depth = root_path.count("/")
    dirs_by_path: dict[str, DirEntry] = {
        root_path: DirEntry(path=root_path, name=posixpath.basename(root_path) or root_path, depth=0)
    }

    def _ensure_dir(dir_path: str) -> DirEntry:
        if dir_path in dirs_by_path:
            return dirs_by_path[dir_path]
        parent_path = posixpath.dirname(dir_path) or root_path
        parent = _ensure_dir(parent_path)
        entry = DirEntry(
            path=dir_path,
            name=posixpath.basename(dir_path),
            depth=dir_path.count("/") - root_depth,
        )
        parent.children.append(entry)
        parent.dirs_count += 1
        dirs_by_path[dir_path] = entry
        return entry

    for file in files:
        parent_path = posixpath.dirname(file.path) or root_path
        parent = _ensure_dir(parent_path)
        parent.files.append(file)
        parent.files_count += 1

    # Agregation recursive de la SEULE taille totale (post-ordre : les
    # enfants d'abord, pour que chaque parent somme des totaux deja
    # finalises). files_count/dirs_count restent tels que deja poses
    # ci-dessus (comptes directs).
    def _aggregate_size(entry: DirEntry) -> int:
        total_size = sum(f.size for f in entry.files)
        for child in entry.children:
            total_size += _aggregate_size(child)
        entry.total_size = total_size
        return total_size

    root = dirs_by_path[root_path]
    _aggregate_size(root)
    return root


def flatten_files(entry: DirEntry) -> list[FileEntry]:
    """Liste PLATE de tous les `FileEntry` du sous-arbre (recursif) —
    l'inverse de `build_tree` : reutilisee partout ou le code a besoin de
    la liste de fichiers plutot que de l'arbre (calcul de stats,
    persistance)."""
    files = list(entry.files)
    for child in entry.children:
        files.extend(flatten_files(child))
    return files


def max_depth(entry: DirEntry) -> int:
    """Profondeur du sous-repertoire le plus profond (feuille) — sert a
    `Scan.max_depth` pour un scan local."""
    if not entry.children:
        return entry.depth
    return max(max_depth(child) for child in entry.children)


def count_all_dirs(entry: DirEntry) -> int:
    """Compte TOUS les sous-repertoires, recursivement — `DirEntry.
    dirs_count` reste volontairement un compte direct (voir docstring de
    `build_tree`), `Scan.total_dirs` a besoin du total."""
    return len(entry.children) + sum(count_all_dirs(child) for child in entry.children)
