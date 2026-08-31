from omega_fold.core.enums import LinkType
from omega_fold.domain.links.service import verify_internal_link

_KNOWN = frozenset(
    {
        "/site/index.html",
        "/site/about.html",
        "/site/img/logo.png",
        "/site/img/icons/star.svg",
    }
)


def test_absolute_link_found() -> None:
    assert verify_internal_link(LinkType.ABSOLUTE, "/about.html", "/site/index.html", "/site", _KNOWN) is True


def test_absolute_link_not_found() -> None:
    assert verify_internal_link(LinkType.ABSOLUTE, "/missing.html", "/site/index.html", "/site", _KNOWN) is False


def test_relative_link_with_separator_resolved_against_source_dir() -> None:
    # source_file est /site/index.html -> son dossier est /site
    assert verify_internal_link(LinkType.RELATIVE, "img/logo.png", "/site/index.html", "/site", _KNOWN) is True


def test_relative_link_with_parent_segment() -> None:
    # source_file est /site/img/gallery.html -> ../about.html -> /site/about.html
    assert verify_internal_link(LinkType.RELATIVE, "../about.html", "/site/img/gallery.html", "/site", _KNOWN) is True


def test_relative_link_bare_filename_searches_whole_tree() -> None:
    assert verify_internal_link(LinkType.RELATIVE, "star.svg", "/site/index.html", "/site", _KNOWN) is True


def test_relative_link_bare_filename_not_found() -> None:
    assert verify_internal_link(LinkType.RELATIVE, "missing.svg", "/site/index.html", "/site", _KNOWN) is False


def test_non_internal_link_types_always_false() -> None:
    for link_type in (LinkType.EXTERNAL, LinkType.ANCHOR, LinkType.MAILTO, LinkType.TEL, LinkType.JAVASCRIPT, LinkType.DATA, LinkType.EMPTY):
        assert verify_internal_link(link_type, "/about.html", "/site/index.html", "/site", _KNOWN) is False
