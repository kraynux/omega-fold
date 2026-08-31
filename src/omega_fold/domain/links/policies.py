# Copyright (c) 2026 kraynux - Licence MIT
"""Classification pure d'un lien brut (OMEGA-FOLD_SPECIFICATIONS.md §5.1).
Aucune E/S : opere sur la chaine d'URL/chemin deja extraite, testable sans
filesystem ni reseau.

`LinkType` melange en un seul enum deux axes que le spec decrit separement
(interne/externe, puis absolu/relatif pour un lien interne) : un lien
EXTERNAL n'est jamais raffine en ABSOLUTE/RELATIVE (une URL complete n'a
pas cette distinction), et INTERNAL elle-meme n'est jamais retournee par
`classify_link_type` — tout lien interne est soit ABSOLUTE soit RELATIVE
(les deux regles du spec sont chacune l'exact complement de l'autre, pas
de cas residuel). `is_internal()` ci-dessous retrouve la categorie large
"interne" a partir d'un resultat ABSOLUTE/RELATIVE, pour le code qui a
besoin de cette distinction plus grossiere (stats, filtrage)."""
from __future__ import annotations

from omega_fold.core.enums import LinkType

_SPECIAL_SCHEMES: tuple[tuple[str, LinkType], ...] = (
    ("mailto:", LinkType.MAILTO),
    ("tel:", LinkType.TEL),
    ("javascript:", LinkType.JAVASCRIPT),
    ("data:", LinkType.DATA),
)

_EXTERNAL_PREFIXES = ("http://", "https://", "//")


def classify_link_type(url: str) -> LinkType:
    """Ordre de priorite (le plus specifique d'abord) :
    vide > schema special (mailto/tel/javascript/data) > ancre pure
    (commence par '#') > externe (http(s):// ou // protocol-relative) >
    absolu (commence par '/') > relatif (tout le reste).

    Une ancre n'est reconnue que si l'URL commence directement par '#'
    (fragment pur, meme page) — un lien comme 'page.html#section' garde
    sa classification absolue/relative habituelle, le fragment de fin
    n'en fait pas une simple ancre au sens de ce spec (il navigue bien
    vers une autre ressource)."""
    stripped = url.strip()

    if not stripped:
        return LinkType.EMPTY

    for scheme, link_type in _SPECIAL_SCHEMES:
        if stripped.lower().startswith(scheme):
            return link_type

    if stripped.startswith("#"):
        return LinkType.ANCHOR

    if stripped.startswith(_EXTERNAL_PREFIXES):
        return LinkType.EXTERNAL

    if stripped.startswith("/"):
        return LinkType.ABSOLUTE

    return LinkType.RELATIVE


def is_internal(link_type: LinkType) -> bool:
    """Categorie large "interne" (spec §5.1) : tout lien qui n'est ni
    externe ni un schema/ancre special."""
    return link_type in (LinkType.ABSOLUTE, LinkType.RELATIVE)
