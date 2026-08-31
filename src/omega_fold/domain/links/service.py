# Copyright (c) 2026 kraynux - Licence MIT
"""Verification d'existence d'un lien INTERNE (OMEGA-FOLD_SPECIFICATIONS.md
§5.2) contre un ensemble de chemins DEJA CONNU (collecte pendant le
parcours reel du filesystem, voir infrastructure/filesystem/
local_fs_walker.py) — aucun nouvel acces disque ici, pure fonction de
correspondance de chaines, testable sans filesystem reel."""
from __future__ import annotations

import posixpath

from omega_fold.core.enums import LinkType


def verify_internal_link(
    link_type: LinkType, url: str, source_file: str, root_path: str, known_paths: frozenset[str]
) -> bool:
    """`known_paths` : ensemble des chemins absolus (normalises avec des
    '/') de tous les fichiers reellement trouves pendant le scan.

    - ABSOLUTE (`/path/to/file`) : verifie `<root_path>/path/to/file`.
    - RELATIVE avec un separateur (`path/to/file`, `../img/x.png`) :
      resolu relativement au REPERTOIRE du fichier source (resolution
      standard d'un lien HTML relatif — le spec dit juste "verifier si
      ./path/to/file existe" sans preciser par rapport a quoi, choix
      explicite ici : par rapport a la page qui contient le lien, pas a
      la racine du scan).
    - RELATIVE sans separateur (`file.html`, nom seul) : recherche dans
      TOUT l'arbre (spec §5.2 "chercher dans tout le repertoire") — le
      premier chemin dont le nom de fichier correspond, s'il y en a un.

    Toute autre valeur de `link_type` (EXTERNAL, ANCHOR, MAILTO, TEL,
    JAVASCRIPT, DATA, EMPTY) n'est jamais interne : retourne toujours
    False (l'appelant ne devrait pas appeler cette fonction pour ces
    cas-la, mais un defaut sûr est preferable a une exception)."""
    root_path = root_path.rstrip("/") or "/"
    stripped = url.strip()

    if link_type == LinkType.ABSOLUTE:
        candidate = posixpath.normpath(posixpath.join(root_path, stripped.lstrip("/")))
        return candidate in known_paths

    if link_type == LinkType.RELATIVE:
        if "/" in stripped:
            source_dir = posixpath.dirname(source_file)
            candidate = posixpath.normpath(posixpath.join(source_dir, stripped))
            return candidate in known_paths
        return any(posixpath.basename(path) == stripped for path in known_paths)

    return False
