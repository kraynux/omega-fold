# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation reelle du port HtmlLinkExtractor (BeautifulSoup4 + lxml).

Note de mutualisation (D-002) : DEEP resout un besoin voisin dans
`infrastructure/discovery/html_link_extractor.py` (uniquement `<a href>`,
pour la decouverte de cibles) — cette implementation couvre davantage de
balises/attributs (besoin different : cartographier TOUTES les
ressources d'une page, pas juste des candidats de cible), pas fusionnee
pour l'instant (voir DECISIONS_ARCHITECTURE.md D-002, "a trancher")."""
from __future__ import annotations

from bs4 import BeautifulSoup

_TAG_ATTRIBUTES: tuple[tuple[str, str], ...] = (
    ("a", "href"),
    ("img", "src"),
    ("script", "src"),
    ("link", "href"),
    ("form", "action"),
)


class Bs4LinkExtractor:
    """Implemente ports/html_link_extractor.py::HtmlLinkExtractor."""

    def extract(self, html_body: str) -> list[tuple[str, str]]:
        soup = BeautifulSoup(html_body, "lxml")
        found: list[tuple[str, str]] = []
        for tag_name, attribute in _TAG_ATTRIBUTES:
            for tag in soup.find_all(tag_name):
                value = tag.get(attribute)
                if value:
                    found.append((str(value), attribute))
        return found
