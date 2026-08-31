# Copyright (c) 2026 kraynux - Licence MIT
"""Calcul pur des statistiques d'un scan (OMEGA-FOLD_SPECIFICATIONS.md
§2.6-§2.9) a partir de listes deja construites (`FileEntry`/`LinkEntry`) —
aucune E/S, testable avec des jeux de donnees synthetiques."""
from __future__ import annotations

from collections import Counter
from urllib.parse import urlparse

from omega_fold.core.enums import LinkType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.stats.models import ExtensionStats, ExternalDomainStats, FamilyStats, TopFile
from omega_fold.domain.stats.policies import classify_family
from omega_fold.domain.tree.models import FileEntry


def compute_extension_stats(files: list[FileEntry]) -> list[ExtensionStats]:
    total_size = sum(f.size for f in files) or 1  # evite une division par zero, voir note ci-dessous
    counts: Counter[str] = Counter()
    sizes: Counter[str] = Counter()
    for file in files:
        counts[file.extension] += 1
        sizes[file.extension] += file.size

    return [
        ExtensionStats(
            extension=extension,
            files_count=counts[extension],
            total_size=sizes[extension],
            percentage_of_total=round(sizes[extension] / total_size * 100, 2),
        )
        for extension in sorted(counts, key=lambda ext: sizes[ext], reverse=True)
    ]


def compute_family_stats(files: list[FileEntry]) -> list[FamilyStats]:
    """`percentage_of_total` reste 0.0 si `files` est vide — pas de
    division par zero deguisee en resultat trompeur (100% de rien n'a
    pas de sens), voir compute_extension_stats pour la meme regle."""
    total_size = sum(f.size for f in files) or 1
    files_by_family: dict[str, list[FileEntry]] = {}
    for file in files:
        family = file.family or classify_family(file.extension)
        files_by_family.setdefault(family, []).append(file)

    stats: list[FamilyStats] = []
    for family, family_files in sorted(files_by_family.items(), key=lambda item: sum(f.size for f in item[1]), reverse=True):
        family_size = sum(f.size for f in family_files)
        stats.append(
            FamilyStats(
                family=family,
                files_count=len(family_files),
                total_size=family_size,
                percentage_of_total=round(family_size / total_size * 100, 2),
                extensions=compute_extension_stats(family_files),
            )
        )
    return stats


def compute_top_files_by_size(files: list[FileEntry], limit: int = 20) -> list[TopFile]:
    ranked = sorted(files, key=lambda f: f.size, reverse=True)[:limit]
    return [TopFile(path=f.path, size=f.size, extension=f.extension) for f in ranked]


def compute_top_files_by_links(files: list[FileEntry], links: list[LinkEntry]) -> list[TopFile]:
    """`links_count` : nombre de liens dont `source_file` est ce fichier
    (liens sortants trouves DANS ce fichier, pas les liens qui y menent)."""
    outgoing: Counter[str] = Counter(link.source_file for link in links)
    ranked = sorted(files, key=lambda f: outgoing[f.path], reverse=True)
    top = [f for f in ranked if outgoing[f.path] > 0][:20]
    return [TopFile(path=f.path, size=f.size, extension=f.extension, links_count=outgoing[f.path]) for f in top]


def compute_external_domain_stats(links: list[LinkEntry]) -> list[ExternalDomainStats]:
    domains: Counter[str] = Counter(
        urlparse(link.url).netloc for link in links if link.link_type == LinkType.EXTERNAL
    )
    domains.pop("", None)  # netloc vide : URL externe malformee, pas exploitable comme domaine
    return [
        ExternalDomainStats(domain=domain, links_count=count)
        for domain, count in sorted(domains.items(), key=lambda item: item[1], reverse=True)
    ]
