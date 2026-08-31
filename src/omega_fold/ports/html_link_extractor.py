# Copyright (c) 2026 kraynux - Licence MIT
"""Contrat d'extraction des liens bruts d'une page HTML
(OMEGA-FOLD_SPECIFICATIONS.md §4.1/§4.2 — `<a href>`, `<img src>`,
`<script src>`, etc.). Implementation (Phase 2/3) : BeautifulSoup4.

Note de mutualisation (D-002, ~/DEV/SUITE/DECISIONS_ARCHITECTURE.md) :
DEEP resout un besoin voisin dans
`infrastructure/discovery/html_link_extractor.py` (extraction de liens
pour la decouverte de cibles) de facon independante — a reevaluer une
fois l'implementation FOLD ecrite (Phase 2/3), pas tranche a ce stade."""
from __future__ import annotations

from typing import Protocol


class HtmlLinkExtractor(Protocol):
    """Implemente par infrastructure/network/bs4_link_extractor.py."""

    def extract(self, html_body: str) -> list[tuple[str, str]]:
        """Retourne une liste de `(url, attribute)` — `attribute` etant
        `"href"`, `"src"` ou `"action"` selon la balise/l'attribut
        d'origine. Ne classifie rien (voir domain/links/policies.py::
        classify_link_type, applique separement par l'appelant) et ne
        verifie aucune existence — extraction pure du HTML brut."""
        ...
