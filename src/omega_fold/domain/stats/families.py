# Copyright (c) 2026 kraynux - Licence MIT
"""Definition des familles de fichiers (OMEGA-FOLD_SPECIFICATIONS.md
§3.1) — verbatim depuis le spec, deplacable telle quelle vers omega_lib
en Phase Suite si un autre outil en a besoin (aucun a ce jour)."""
from __future__ import annotations

FAMILIES: dict[str, list[str]] = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".bmp", ".tiff", ".avif"],
    "documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp"],
    "code": [
        ".html", ".php", ".js", ".ts", ".py", ".rb", ".java", ".cpp", ".c", ".h",
        ".css", ".scss", ".less", ".vue", ".jsx", ".tsx",
    ],
    "data": [".json", ".xml", ".yaml", ".yml", ".csv", ".sql", ".db", ".sqlite", ".ini", ".conf", ".cfg"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"],
    "fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "video": [".mp4", ".webm", ".avi", ".mov", ".mkv", ".flv"],
    "audio": [".mp3", ".wav", ".ogg", ".flac", ".aac"],
    "text": [".txt", ".md", ".rst", ".log"],
    "other": [],  # tout ce qui n'est pas dans les autres familles
}
