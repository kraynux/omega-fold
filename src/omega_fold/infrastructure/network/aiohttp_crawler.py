# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation reelle du port DistantCrawler (aiohttp asynchrone).

robots.txt est recupere et parse ICI (pas dans domain/application) :
c'est de la meme nature d'E/S que recuperer la page elle-meme. Mis en
cache par domaine sur l'instance (une seule instance de `AiohttpCrawler`
est reutilisee pour tout un crawl, voir application/commands/
run_scan.py::run_scan_distant) — evite de re-telecharger robots.txt a
chaque page."""
from __future__ import annotations

from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import aiohttp

from omega_fold.ports.distant_crawler import CrawledPage

_HTML_CONTENT_TYPE_PREFIX = "text/html"


class AiohttpCrawler:
    """Implemente ports/distant_crawler.py::DistantCrawler."""

    def __init__(self) -> None:
        self._robots_cache: dict[str, RobotFileParser | None] = {}

    async def fetch(self, url: str, *, timeout: float, user_agent: str, respect_robots: bool) -> CrawledPage:
        if respect_robots:
            parser = await self._get_robots_parser(url, timeout=timeout, user_agent=user_agent)
            if parser is not None and not parser.can_fetch(user_agent, url):
                return CrawledPage(
                    url=url, status_code=0, content_type=None, content_length=None,
                    html_body=None, final_url=url, allowed_by_robots=False,
                )

        try:
            async with aiohttp.ClientSession() as session, session.get(
                url, headers={"User-Agent": user_agent}, timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                content_type = response.headers.get("Content-Type")
                content_length_header = response.headers.get("Content-Length")
                content_length = int(content_length_header) if content_length_header else None

                html_body: str | None = None
                if content_type and content_type.split(";")[0].strip() == _HTML_CONTENT_TYPE_PREFIX:
                    html_body = await response.text(errors="replace")

                return CrawledPage(
                    url=url,
                    status_code=response.status,
                    content_type=content_type,
                    content_length=content_length,
                    html_body=html_body,
                    final_url=str(response.url),
                )
        except (TimeoutError, aiohttp.ClientError, OSError, ValueError) as exc:
            # Une seule ressource injoignable/lente/mal formee (timeout,
            # connexion refusee, reset, DNS, URL invalide...) ne doit jamais
            # interrompre tout le crawl (bug reel trouve en usage : une
            # seule TimeoutError sur une page faisait echouer le scan
            # entier). `TimeoutError` n'est PAS une sous-classe de
            # `aiohttp.ClientError` (asyncio.TimeoutError y est aliase
            # depuis Python 3.11) — capturee separement. `ValueError` :
            # yarl (aiohttp) leve parfois cette exception pour une URL
            # syntaxiquement invalide (ex. caractere de controle non
            # imprimable dans un href extrait d'un HTML casse/dynamique) —
            # meme classe de bug que httpx.InvalidURL cote
            # infrastructure/network/http_link_checker.py.
            return CrawledPage(
                url=url, status_code=0, content_type=None, content_length=None,
                html_body=None, final_url=url, fetch_error=str(exc) or type(exc).__name__,
            )

    async def _get_robots_parser(self, url: str, *, timeout: float, user_agent: str) -> RobotFileParser | None:
        parsed = urlparse(url)
        domain_key = f"{parsed.scheme}://{parsed.netloc}"
        if domain_key in self._robots_cache:
            return self._robots_cache[domain_key]

        robots_url = urljoin(domain_key, "/robots.txt")
        parser = RobotFileParser()
        try:
            async with aiohttp.ClientSession() as session, session.get(
                robots_url, headers={"User-Agent": user_agent}, timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                if response.status >= 400:
                    self._robots_cache[domain_key] = None
                    return None
                text = await response.text(errors="replace")
        except (TimeoutError, aiohttp.ClientError):
            # meme raisonnement que fetch() ci-dessus : un robots.txt lent/
            # injoignable n'est pas une erreur fatale, juste indetermine
            # (repli implicite sur "autorise", meme comportement qu'un 4xx/5xx).
            self._robots_cache[domain_key] = None
            return None

        parser.parse(text.splitlines())
        self._robots_cache[domain_key] = parser
        return parser
