# Copyright (c) 2026 kraynux - Licence MIT
"""Definition DDL des tables SQLite — schema volontairement simplifie par
rapport a OMEGA-FOLD_SPECIFICATIONS.md §7.1 : seulement `scans`/`files`/
`links` (pas de tables separees pour `dirs`/`extension_stats`/
`family_stats`/`top_files`/`external_domains`). `DirEntry` (arbre imbrique)
et toutes les statistiques sont entierement reconstructibles a partir de
`files`+`links` deja stockes, via les fonctions pures deja ecrites en
Phase 2 (`domain/tree/service.py::build_tree`,
`domain/stats/service.py::compute_*`) — les recalculer a la lecture evite
une duplication qui pourrait diverger (voir DECISIONS_ARCHITECTURE.md).

`id` en UUID (pas autoincrement), `created_at` en ISO8601 UTC — memes
principes que omega-check/omega-deep (D-006)."""
from __future__ import annotations

SCHEMA_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS scans (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        tool TEXT NOT NULL DEFAULT 'fold',
        target TEXT NOT NULL,
        target_type TEXT NOT NULL,
        scan_mode TEXT NOT NULL,
        status TEXT NOT NULL,
        total_files INTEGER NOT NULL DEFAULT 0,
        total_dirs INTEGER NOT NULL DEFAULT 0,
        total_size INTEGER NOT NULL DEFAULT 0,
        max_depth INTEGER NOT NULL DEFAULT 0,
        total_links INTEGER NOT NULL DEFAULT 0,
        internal_links INTEGER NOT NULL DEFAULT 0,
        external_links INTEGER NOT NULL DEFAULT 0,
        broken_links INTEGER NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_scans_target ON scans (target)
    """,
    """
    CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        scan_id TEXT NOT NULL REFERENCES scans (id),
        path TEXT NOT NULL,
        name TEXT NOT NULL,
        extension TEXT NOT NULL,
        size INTEGER NOT NULL,
        depth INTEGER NOT NULL,
        family TEXT NOT NULL,
        mime_type TEXT,
        is_binary INTEGER NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_files_scan_id ON files (scan_id)
    """,
    """
    CREATE TABLE IF NOT EXISTS links (
        id TEXT PRIMARY KEY,
        scan_id TEXT NOT NULL REFERENCES scans (id),
        url TEXT NOT NULL,
        link_type TEXT NOT NULL,
        source_file TEXT NOT NULL,
        attribute TEXT NOT NULL,
        status TEXT NOT NULL,
        status_code INTEGER,
        error_message TEXT,
        confidence TEXT NOT NULL,
        target_exists INTEGER
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_links_scan_id ON links (scan_id)
    """,
)
