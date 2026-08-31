# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat de crawl HTTP limite d'un site distant
(OMEGA-FOLD_SPECIFICATIONS.md §4.2). Implementation (Phase 3) :
aiohttp asynchrone — garde-fous profondeur/nombre de pages/delai
appliques par l'appelant (`domain/scans/policies.py`, voir
DECISIONS_ARCHITECTURE.md pour la deviation vs `OMEGA-FOLD_ARBORESCENCE.md`
§2 qui suggerait `application/pipeline/guards/`) ; robots.txt est verifie
DANS l'adaptateur (`infrastructure/network/aiohttp_crawler.py`), seule
exception a "l'appelant orchestre tout" — recuperer et parser robots.txt
est de la meme nature d'E/S que recuperer la page elle-meme, ca n'a pas
sa place dans application/."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class CrawledPage:
    """Une page recuperee : assez d'information pour que l'appelant en
    tire un FileEntry/DirEntry virtuel et en extraie les liens.

    `final_url` : l'URL reellement chargee APRES toute redirection HTTP
    suivie par l'implementation — distincte de `url` (l'URL demandee).
    Necessaire pour detecter un "permalien" dont le chemin ressemble a
    un lien interne (`/go/xyz`, `/out/...`) mais qui redirige en realite
    vers un domaine externe : sans ce champ, l'appelant traiterait le
    contenu recupere (celui du site EXTERNE) comme une page interne et
    continuerait a en suivre les liens (bug reel trouve en usage)."""

    url: str
    status_code: int
    content_type: str | None
    content_length: int | None  # depuis l'en-tete Content-Length, si present
    html_body: str | None  # None si le contenu n'est pas du HTML
    final_url: str = ""  # URL apres redirection(s) ; egale a `url` si aucune
    allowed_by_robots: bool = True  # False si robots.txt interdit cette URL (fetch non tente)
    fetch_error: str | None = None
    """Non-None si la requete a echoue (timeout/connexion refusee/DNS/...)
    — jamais leve comme exception (voir docstring de `fetch` ci-dessous) :
    une seule page en echec (serveur lent, ressource qui ne repond jamais)
    ne doit jamais interrompre tout le crawl (bug reel trouve en usage —
    `TimeoutError` sur une seule requete faisait echouer le scan entier,
    perdant toute la progression deja accumulee)."""


class DistantCrawler(Protocol):
    """Implemente par infrastructure/network/aiohttp_crawler.py. `fetch`
    est asynchrone (`aiohttp` est fondamentalement async) — revision du
    contrat pose en Phase 1 (qui l'avait laisse synchrone par erreur),
    meme genre de revision transparente que `save_host` -> `save_hosts`
    chez omega-deep."""

    async def fetch(self, url: str, *, timeout: float, user_agent: str, respect_robots: bool) -> CrawledPage:
        """Une seule page, une seule requete. L'appelant orchestre la
        boucle de crawl (profondeur, nombre de pages, delai entre
        requetes) — jamais cette fonction elle-meme. Si
        `respect_robots=True` et que robots.txt interdit `url`, retourne
        un `CrawledPage` avec `allowed_by_robots=False` et
        `status_code=0` plutot que de lever — un refus de robots.txt
        n'est pas une erreur reseau. Meme principe pour un ECHEC RESEAU
        (timeout, connexion refusee, DNS, etc.) : retourne un
        `CrawledPage` avec `fetch_error` renseigne (`status_code=0`),
        NE LEVE JAMAIS — une seule ressource injoignable ne doit pas
        interrompre tout le crawl, l'appelant decide comment reagir
        (ignorer cette page et continuer)."""
        ...
