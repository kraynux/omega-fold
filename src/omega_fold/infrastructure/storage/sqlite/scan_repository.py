# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation SQLite du port ScanRepository (ports/scan_repository.py).

Schema simplifie (voir schema.py) : `save_result`/`get_result` ne
persistent QUE `files`+`links` (delete-then-insert par `scan_id`, meme
raisonnement que `save_hosts` de omega-deep — pas de `ON DELETE CASCADE`
fiable sur sqlite3 par defaut). `DirEntry` (arbre imbrique) et toutes les
statistiques (`extension_stats`/`family_stats`/`top_files_*`/
`external_domains`) sont RECALCULEES a la lecture via les fonctions pures
deja ecrites en Phase 2 (`domain/tree/service.py::build_tree`,
`domain/stats/service.py::compute_*`) plutot que stockees telles quelles :
`get_result` reconstruit donc un `ScanResult` complet et coherent, jamais
desynchronise de `files`/`links`.

Le `root_path` passe a `build_tree` differe selon `target_type` : pour un
scan LOCAL, c'est `scan.target` (le chemin racine reel, voir
run_scan.py::run_scan_local qui pose `target=root_dir.path`) ; pour un
scan DISTANT, c'est toujours `"/"` (voir run_scan.py::run_scan_distant qui
appelle `build_tree("/", files)` — les chemins des `FileEntry` distants
sont des chemins virtuels poses par `_page_url_to_path`, racine `/`)."""
from __future__ import annotations

import sqlite3

from omega_lib.shared.ids import new_id

from omega_fold.core.enums import ConfidenceLevel, LinkStatus, LinkType, ScanMode, ScanTargetType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.models import Scan
from omega_fold.domain.stats.service import (
    compute_extension_stats,
    compute_external_domain_stats,
    compute_family_stats,
    compute_top_files_by_links,
    compute_top_files_by_size,
)
from omega_fold.domain.tree.models import FileEntry
from omega_fold.domain.tree.service import build_tree, flatten_files
from omega_fold.infrastructure.exceptions import StorageError


class SqliteScanRepository:
    """Implemente ports/scan_repository.py::ScanRepository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    # --- scans --------------------------------------------------------

    def save(self, scan: Scan) -> None:
        try:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO scans
                    (id, created_at, tool, target, target_type, scan_mode,
                     status, total_files, total_dirs, total_size, max_depth,
                     total_links, internal_links, external_links, broken_links)
                VALUES (?, ?, 'fold', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    scan.id,
                    scan.created_at,
                    scan.target,
                    scan.target_type.value,
                    scan.scan_mode.value,
                    scan.status,
                    scan.total_files,
                    scan.total_dirs,
                    scan.total_size,
                    scan.max_depth,
                    scan.total_links,
                    scan.internal_links,
                    scan.external_links,
                    scan.broken_links,
                ),
            )
            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(f"echec de sauvegarde du scan {scan.id!r}") from exc

    def get(self, scan_id: str) -> Scan | None:
        row = self._connection.execute("SELECT * FROM scans WHERE id = ?", (scan_id,)).fetchone()
        return self._row_to_scan(row) if row is not None else None

    def list_history(self, *, target: str | None = None, limit: int = 50) -> tuple[Scan, ...]:
        if target is not None:
            rows = self._connection.execute(
                "SELECT * FROM scans WHERE target = ? ORDER BY created_at DESC LIMIT ?", (target, limit)
            ).fetchall()
        else:
            rows = self._connection.execute(
                "SELECT * FROM scans ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return tuple(self._row_to_scan(row) for row in rows)

    def clear(self) -> None:
        self._connection.execute("DELETE FROM links")
        self._connection.execute("DELETE FROM files")
        self._connection.execute("DELETE FROM scans")
        self._connection.commit()

    @staticmethod
    def _row_to_scan(row: sqlite3.Row) -> Scan:
        return Scan(
            id=row["id"],
            created_at=row["created_at"],
            target=row["target"],
            target_type=ScanTargetType(row["target_type"]),
            scan_mode=ScanMode(row["scan_mode"]),
            status=row["status"],
            total_files=row["total_files"],
            total_dirs=row["total_dirs"],
            total_size=row["total_size"],
            max_depth=row["max_depth"],
            total_links=row["total_links"],
            internal_links=row["internal_links"],
            external_links=row["external_links"],
            broken_links=row["broken_links"],
        )

    # --- resultat complet (files/links) --------------------------------

    def save_result(self, scan_id: str, result: ScanResult) -> None:
        try:
            cursor = self._connection.cursor()
            # ON DELETE CASCADE n'est pas active par defaut sur sqlite3, nettoyage manuel.
            cursor.execute("DELETE FROM links WHERE scan_id = ?", (scan_id,))
            cursor.execute("DELETE FROM files WHERE scan_id = ?", (scan_id,))

            files = flatten_files(result.root_dir) if result.root_dir is not None else []
            for file in files:
                self._insert_file(cursor, scan_id, file)
            for link in result.links:
                self._insert_link(cursor, scan_id, link)

            self._connection.commit()
        except sqlite3.Error as exc:
            raise StorageError(f"echec de sauvegarde du resultat pour le scan {scan_id!r}") from exc

    @staticmethod
    def _insert_file(cursor: sqlite3.Cursor, scan_id: str, file: FileEntry) -> None:
        cursor.execute(
            """
            INSERT INTO files (id, scan_id, path, name, extension, size, depth, family, mime_type, is_binary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id(),
                scan_id,
                file.path,
                file.name,
                file.extension,
                file.size,
                file.depth,
                file.family,
                file.mime_type,
                file.is_binary,
            ),
        )

    @staticmethod
    def _insert_link(cursor: sqlite3.Cursor, scan_id: str, link: LinkEntry) -> None:
        cursor.execute(
            """
            INSERT INTO links
                (id, scan_id, url, link_type, source_file, attribute, status,
                 status_code, error_message, confidence, target_exists)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                new_id(),
                scan_id,
                link.url,
                link.link_type.value,
                link.source_file,
                link.attribute,
                link.status.value,
                link.status_code,
                link.error_message,
                link.confidence.value,
                link.target_exists,
            ),
        )

    def get_result(self, scan_id: str) -> ScanResult | None:
        scan = self.get(scan_id)
        if scan is None:
            return None

        file_rows = self._connection.execute("SELECT * FROM files WHERE scan_id = ?", (scan_id,)).fetchall()
        link_rows = self._connection.execute("SELECT * FROM links WHERE scan_id = ?", (scan_id,)).fetchall()
        files = [self._row_to_file(row) for row in file_rows]
        links = [self._row_to_link(row) for row in link_rows]

        root_path = scan.target if scan.target_type == ScanTargetType.LOCAL else "/"
        root_dir = build_tree(root_path, files)
        broken_links = [link for link in links if link.status == LinkStatus.BROKEN]

        return ScanResult(
            scan=scan,
            root_dir=root_dir,
            links=links,
            extension_stats=compute_extension_stats(files),
            family_stats=compute_family_stats(files),
            top_files_by_size=compute_top_files_by_size(files),
            top_files_by_links=compute_top_files_by_links(files, links),
            external_domains=compute_external_domain_stats(links),
            broken_links=broken_links,
        )

    @staticmethod
    def _row_to_file(row: sqlite3.Row) -> FileEntry:
        return FileEntry(
            path=row["path"],
            name=row["name"],
            extension=row["extension"],
            size=row["size"],
            depth=row["depth"],
            family=row["family"],
            mime_type=row["mime_type"],
            is_binary=bool(row["is_binary"]),
        )

    @staticmethod
    def _row_to_link(row: sqlite3.Row) -> LinkEntry:
        return LinkEntry(
            url=row["url"],
            link_type=LinkType(row["link_type"]),
            source_file=row["source_file"],
            attribute=row["attribute"],
            status=LinkStatus(row["status"]),
            status_code=row["status_code"],
            error_message=row["error_message"],
            confidence=ConfidenceLevel(row["confidence"]),
            target_exists=(bool(row["target_exists"]) if row["target_exists"] is not None else None),
        )
