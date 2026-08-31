# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de parcours d'un repertoire local
(OMEGA-FOLD_SPECIFICATIONS.md §4.1). Implementation (Phase 2) : parcours
recursif reel, calcul de profondeur/taille."""
from __future__ import annotations

from typing import Protocol

from omega_fold.domain.tree.models import DirEntry


class LocalFsReader(Protocol):
    """Implemente par infrastructure/filesystem/local_fs_walker.py."""

    def read_tree(self, root_path: str) -> DirEntry:
        """Parcourt `root_path` recursivement et retourne l'arborescence
        complete (fichiers + sous-repertoires), profondeur/taille
        calculees. Leve une erreur d'infrastructure si `root_path`
        n'existe pas ou n'est pas lisible — aucune tentative de
        traitement silencieux ici."""
        ...

    def read_file(self, path: str) -> str:
        """Contenu texte d'UN fichier (ex. une page HTML deja localisee
        par `read_tree`, pour en extraire les liens — voir
        application/commands/run_scan.py::run_scan_local). Ajoute apres
        coup (Phase 2) : lire le contenu d'un fichier est de la meme
        nature d'E/S que le parcourir, ca n'a pas sa place dans
        application/ non plus."""
        ...
