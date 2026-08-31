# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation reelle du port LocalFsReader (parcours filesystem via
`os.walk`). Construit chaque `FileEntry` (extension/taille/profondeur/
famille/mime), puis delegue l'assemblage de l'arborescence imbriquee et
l'agregation des tailles a `domain/tree/service.py::build_tree` — l'
algorithme d'agregation reste domaine pur, seul le parcours reel est ici."""
from __future__ import annotations

import os
from pathlib import Path

from omega_fold.domain.stats.policies import classify_family, is_binary_mime
from omega_fold.domain.tree.models import DirEntry, FileEntry
from omega_fold.domain.tree.service import build_tree
from omega_fold.infrastructure.filesystem.mime_detector import detect_mime_type


class LocalFsWalker:
    """Implemente ports/local_fs_reader.py::LocalFsReader."""

    def read_tree(self, root_path: str) -> DirEntry:
        root_path = os.path.abspath(root_path)
        if not os.path.isdir(root_path):
            raise NotADirectoryError(f"'{root_path}' n'est pas un repertoire lisible")

        root_depth = root_path.rstrip("/").count("/")
        files: list[FileEntry] = []

        for current_dir, _dir_names, file_names in os.walk(root_path):
            depth = current_dir.rstrip("/").count("/") - root_depth
            for file_name in file_names:
                full_path = os.path.join(current_dir, file_name)
                try:
                    size = os.path.getsize(full_path)
                except OSError:
                    continue  # lien symbolique casse ou fichier disparu pendant le parcours : ignore, pas fatal
                extension = os.path.splitext(file_name)[1].lower()
                mime_type = detect_mime_type(full_path)
                files.append(
                    FileEntry(
                        path=full_path,
                        name=file_name,
                        extension=extension,
                        size=size,
                        depth=depth + 1,  # profondeur du FICHIER = profondeur de son dossier + 1
                        family=classify_family(extension),
                        mime_type=mime_type,
                        is_binary=is_binary_mime(mime_type),
                    )
                )

        return build_tree(root_path, files)

    def read_file(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8", errors="replace")
