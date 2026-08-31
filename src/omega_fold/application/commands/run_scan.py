# Copyright (c) 2026 kraynux - Licence MIT
"""Use case : lancer un scan local (OMEGA-FOLD_SPECIFICATIONS.md §6.1) —
parcours + extraction/classification/verification des liens + calcul des
statistiques + assemblage du `ScanResult`. La verification HTTP des liens
externes (mode DYNAMIC) est traitee separement par
`run_scan_distant`/`infrastructure/network/http_link_checker.py` (Phase
3) : un scan local en mode DYNAMIC verifie ses liens INTERNES comme en
mode STATIC (verification filesystem, pas HTTP — ce n'est pas plus lent
en dynamique) et laisse ses liens EXTERNES `UNCHECKED` pour l'instant
(brancher `HttpLinkChecker` ici est une extension triviale, pas faite
faute de demande explicite — eviter la sur-ingenierie)."""
from __future__ import annotations

import asyncio
import logging
import posixpath
from collections.abc import Callable
from datetime import datetime
from urllib.parse import urldefrag, urljoin, urlparse

from omega_lib.shared.typing import IdFactory

from omega_fold.core.enums import LinkStatus, LinkType, ScanMode, ScanTargetType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.links.policies import classify_link_type, is_internal
from omega_fold.domain.links.service import verify_internal_link
from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.models import Scan
from omega_fold.domain.scans.policies import (
    is_depth_allowed,
    is_page_count_allowed,
    is_same_domain,
    normalize_distant_target,
)
from omega_fold.domain.stats.policies import classify_family, is_binary_mime
from omega_fold.domain.stats.service import (
    compute_extension_stats,
    compute_external_domain_stats,
    compute_family_stats,
    compute_top_files_by_links,
    compute_top_files_by_size,
)
from omega_fold.domain.tree.models import FileEntry
from omega_fold.domain.tree.service import build_tree, count_all_dirs, flatten_files
from omega_fold.domain.tree.service import max_depth as tree_max_depth
from omega_fold.ports.distant_crawler import DistantCrawler
from omega_fold.ports.html_link_extractor import HtmlLinkExtractor
from omega_fold.ports.link_checker import LinkChecker
from omega_fold.ports.local_fs_reader import LocalFsReader
from omega_fold.ports.scan_repository import ScanRepository

_HTML_EXTENSION = ".html"
_DEFAULT_TIMEOUT_SECONDS = 8.0
_logger = logging.getLogger("omega_fold.scan")


def run_scan_local(
    *,
    root_path: str,
    scan_mode: ScanMode,
    local_fs_reader: LocalFsReader,
    html_link_extractor: HtmlLinkExtractor,
    id_factory: IdFactory,
    now: Callable[[], datetime],
    scan_repository: ScanRepository | None = None,
) -> ScanResult:
    _logger.info(f"Parcours de {root_path}...")
    root_dir = local_fs_reader.read_tree(root_path)
    files = flatten_files(root_dir)
    known_paths = frozenset(f.path for f in files)
    _logger.info(f"{len(files)} fichier(s) trouve(s), extraction des liens...")

    links: list[LinkEntry] = []
    for file in files:
        if file.family != "code" or file.extension != _HTML_EXTENSION:
            continue
        html_body = local_fs_reader.read_file(file.path)
        for url, attribute in html_link_extractor.extract(html_body):
            link_type = classify_link_type(url)
            entry = LinkEntry(url=url, link_type=link_type, source_file=file.path, attribute=attribute)
            if is_internal(link_type):
                exists = verify_internal_link(link_type, url, file.path, root_dir.path, known_paths)
                entry.target_exists = exists
                entry.status = LinkStatus.EXISTS if exists else LinkStatus.BROKEN
            links.append(entry)

    broken_links = [link for link in links if link.status == LinkStatus.BROKEN]

    scan = Scan(
        id=id_factory(),
        created_at=now().isoformat(),
        target=root_dir.path,
        target_type=ScanTargetType.LOCAL,
        scan_mode=scan_mode,
        status="completed",
        total_files=len(files),
        total_dirs=count_all_dirs(root_dir),
        total_size=root_dir.total_size,
        max_depth=tree_max_depth(root_dir),
        total_links=len(links),
        internal_links=sum(1 for link in links if is_internal(link.link_type)),
        external_links=sum(1 for link in links if link.link_type == LinkType.EXTERNAL),
        broken_links=len(broken_links),
    )

    result = ScanResult(
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
    if scan_repository is not None:
        assert scan.id is not None  # toujours fixe par id_factory() ci-dessus
        scan_repository.save(scan)
        scan_repository.save_result(scan.id, result)
    _logger.info(f"Scan termine : {len(files)} fichier(s), {len(links)} lien(s).")
    return result


def _page_url_to_path(url: str) -> str:
    """URL -> chemin virtuel posix (pour reutiliser domain/tree/service.py
    ::build_tree tel quel) : le chemin de l'URL, racine "/" -> "/index.html"
    (une page vide de chemin n'est pas distinguable du repertoire racine
    lui-meme dans une arborescence posix)."""
    path = urlparse(url).path
    if not path or path == "/":
        return "/index.html"
    return path


async def run_scan_distant(
    *,
    base_url: str,
    scan_mode: ScanMode,
    max_depth: int,
    max_pages: int,
    delay_ms: int,
    user_agent: str,
    respect_robots: bool,
    distant_crawler: DistantCrawler,
    html_link_extractor: HtmlLinkExtractor,
    link_checker: LinkChecker,
    id_factory: IdFactory,
    now: Callable[[], datetime],
    timeout: float = _DEFAULT_TIMEOUT_SECONDS,
    scan_repository: ScanRepository | None = None,
) -> ScanResult:
    """Crawl BFS borne par `max_depth`/`max_pages`, un `asyncio.sleep`
    entre chaque requete (`delay_ms`). Un lien EXTERNE n'est verifie par
    HTTP qu'en mode DYNAMIC (spec §1.2) ; un lien INTERNE est verifie
    apres coup (une fois le crawl termine) contre l'ensemble des pages
    reellement visitees avec succes — une page hors des garde-fous ou
    bloquee par robots.txt reste `UNCHECKED`, jamais `BROKEN` par
    supposition (le lien n'a pas ete tente, ce n'est pas la meme chose
    qu'un lien confirme casse)."""
    base_url = normalize_distant_target(base_url)
    _logger.info(f"Crawl de {base_url}...")
    base_domain = urlparse(base_url).netloc

    visited_status: dict[str, int] = {}  # url (sans fragment) -> status_code
    files: list[FileEntry] = []
    links: list[LinkEntry] = []
    queue: list[tuple[str, int]] = [(base_url, 0)]
    queued: set[str] = {base_url}
    deepest_depth = 0
    truncated = False

    while queue:
        if not is_page_count_allowed(len(visited_status), max_pages):
            # Des pages restaient en file : le crawl s'est arrete a cause de
            # `--max-pages`, pas parce que le site a ete entierement couvert
            # (contrairement a `max_depth`, qui borne intentionnellement la
            # portee — atteindre la profondeur demandee n'est pas une
            # troncature). Doute de fiabilite signale par l'utilisateur :
            # "1000 fichiers trouves" ne disait pas si c'etait la TAILLE
            # REELLE du site ou juste la limite par defaut atteinte.
            truncated = True
            _logger.info(f"Limite de {max_pages} page(s) atteinte, crawl arrete (site probablement plus grand).")
            break
        url, depth = queue.pop(0)
        if url in visited_status:
            continue

        await asyncio.sleep(delay_ms / 1000)
        page = await distant_crawler.fetch(url, timeout=timeout, user_agent=user_agent, respect_robots=respect_robots)
        if page.fetch_error is not None:
            # Une seule page injoignable/lente (timeout, connexion refusee,
            # DNS...) ne doit jamais interrompre tout le crawl — deja perdu
            # sinon toute la progression accumulee (bug reel signale par
            # l'utilisateur). Reste UNCHECKED, meme principe que robots.txt.
            _logger.info(f"Echec de recuperation, page ignoree : {url} ({page.fetch_error})")
            continue
        if not page.allowed_by_robots:
            _logger.info(f"Bloque par robots.txt : {url}")
            continue  # jamais visite : reste UNCHECKED pour les liens qui y menent

        if not is_same_domain(page.final_url, base_domain):
            # Permalien/redirection courte (ex. /go/xyz, /out/...) dont le
            # CHEMIN ressemble a un lien interne mais dont le serveur
            # redirige en realite vers un domaine externe : le contenu
            # recupere est celui du site EXTERNE, jamais traite comme une
            # page du site scanne (ni arborescence, ni liens suivis) — sans
            # cela le crawl continuerait sur le site externe. Reste
            # UNCHECKED cote verification de lien interne (voir robots.txt
            # ci-dessus, meme principe).
            _logger.info(f"Redirection hors domaine ignoree : {url} -> {page.final_url}")
            continue

        _logger.info(f"Page visitee : {url} ({page.status_code})")
        visited_status[url] = page.status_code
        deepest_depth = max(deepest_depth, depth)
        virtual_path = _page_url_to_path(url)
        virtual_name = virtual_path.rsplit("/", 1)[-1]
        extension = posixpath.splitext(virtual_name)[1].lower()
        if not extension and page.html_body is not None:
            extension = _HTML_EXTENSION  # route "propre" sans extension (ex. /about) mais contenu HTML confirme
        files.append(
            FileEntry(
                path=virtual_path,
                name=virtual_name,
                extension=extension,
                size=page.content_length or (len(page.html_body) if page.html_body else 0),
                depth=depth,
                family=classify_family(extension) if extension else "other",
                mime_type=page.content_type,
                is_binary=is_binary_mime(page.content_type) if page.content_type else page.html_body is None,
            )
        )

        if page.html_body is None:
            continue

        # Les liens de CETTE page sont toujours extraits/rapportes (utile
        # pour les stats/le rapport), meme si `max_depth` interdit de les
        # suivre plus loin — is_depth_allowed borne uniquement la mise en
        # FILE, pas la visibilite des liens de la page elle-meme.
        can_follow = is_depth_allowed(depth, max_depth)
        for raw_url, attribute in html_link_extractor.extract(page.html_body):
            link_type = classify_link_type(raw_url)
            entry = LinkEntry(url=raw_url, link_type=link_type, source_file=url, attribute=attribute)

            if link_type == LinkType.EXTERNAL:
                if scan_mode == ScanMode.DYNAMIC:
                    status, code, error = await asyncio.to_thread(link_checker.check, raw_url, timeout=timeout)
                    entry.status = status
                    entry.status_code = code
                    entry.error_message = error
                links.append(entry)
                continue

            if is_internal(link_type):
                if can_follow:
                    resolved, _ = urldefrag(urljoin(url, raw_url))
                    if is_same_domain(resolved, base_domain) and resolved not in queued:
                        queued.add(resolved)
                        queue.append((resolved, depth + 1))
                links.append(entry)
                continue

            links.append(entry)  # ancre/mailto/tel/javascript/data/vide : jamais verifie

    # Deuxieme passe : les liens internes ne peuvent etre juges qu'une
    # fois toutes les pages atteignables reellement visitees.
    for link in links:
        if not is_internal(link.link_type):
            continue
        resolved, _ = urldefrag(urljoin(link.source_file, link.url))
        status_code = visited_status.get(resolved)
        if status_code is None:
            continue  # jamais visitee (hors garde-fous/robots.txt) : reste UNCHECKED
        link.status_code = status_code
        link.target_exists = 200 <= status_code < 400
        link.status = LinkStatus.EXISTS if link.target_exists else LinkStatus.BROKEN

    broken_links = [link for link in links if link.status == LinkStatus.BROKEN]
    root_dir = build_tree("/", files)

    scan = Scan(
        id=id_factory(),
        created_at=now().isoformat(),
        target=base_url,
        target_type=ScanTargetType.DISTANT,
        scan_mode=scan_mode,
        status="completed_truncated" if truncated else "completed",
        total_files=len(files),
        total_dirs=count_all_dirs(root_dir),
        total_size=root_dir.total_size,
        max_depth=deepest_depth,
        total_links=len(links),
        internal_links=sum(1 for link in links if is_internal(link.link_type)),
        external_links=sum(1 for link in links if link.link_type == LinkType.EXTERNAL),
        broken_links=len(broken_links),
    )

    result = ScanResult(
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
    if scan_repository is not None:
        assert scan.id is not None  # toujours fixe par id_factory() ci-dessus
        scan_repository.save(scan)
        scan_repository.save_result(scan.id, result)
    _logger.info(f"Crawl termine : {len(files)} page(s), {len(links)} lien(s).")
    return result


async def run_scan(
    *,
    target: str,
    target_type: ScanTargetType,
    scan_mode: ScanMode,
    id_factory: IdFactory,
    now: Callable[[], datetime],
    html_link_extractor: HtmlLinkExtractor,
    local_fs_reader: LocalFsReader | None = None,
    distant_crawler: DistantCrawler | None = None,
    link_checker: LinkChecker | None = None,
    max_depth: int = 5,
    max_pages: int = 1000,
    delay_ms: int = 100,
    user_agent: str = "omega-fold/0.1",
    respect_robots: bool = False,
    scan_repository: ScanRepository | None = None,
) -> ScanResult:
    """Dispatcher (OMEGA-FOLD_SPECIFICATIONS.md §6.1) : delegue a
    `run_scan_local` ou `run_scan_distant` selon `target_type`. Async
    dans les deux cas (meme si `run_scan_local` lui-meme est sync) —
    l'appelant (CLI/TUI, Phase 4) n'a qu'une seule fonction a `await`."""
    if target_type == ScanTargetType.LOCAL:
        if local_fs_reader is None:
            raise ValueError("local_fs_reader est requis pour un scan LOCAL")
        return run_scan_local(
            root_path=target,
            scan_mode=scan_mode,
            local_fs_reader=local_fs_reader,
            html_link_extractor=html_link_extractor,
            id_factory=id_factory,
            now=now,
            scan_repository=scan_repository,
        )

    if distant_crawler is None or link_checker is None:
        raise ValueError("distant_crawler et link_checker sont requis pour un scan DISTANT")
    return await run_scan_distant(
        base_url=target,
        scan_mode=scan_mode,
        max_depth=max_depth,
        max_pages=max_pages,
        delay_ms=delay_ms,
        user_agent=user_agent,
        respect_robots=respect_robots,
        scan_repository=scan_repository,
        distant_crawler=distant_crawler,
        html_link_extractor=html_link_extractor,
        link_checker=link_checker,
        id_factory=id_factory,
        now=now,
    )
