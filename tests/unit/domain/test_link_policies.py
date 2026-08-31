import pytest

from omega_fold.core.enums import LinkType
from omega_fold.domain.links.policies import classify_link_type, is_internal


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("", LinkType.EMPTY),
        ("   ", LinkType.EMPTY),
        ("mailto:contact@example.org", LinkType.MAILTO),
        ("MAILTO:contact@example.org", LinkType.MAILTO),
        ("tel:+33123456789", LinkType.TEL),
        ("javascript:void(0)", LinkType.JAVASCRIPT),
        ("data:image/png;base64,iVBORw0KGgo=", LinkType.DATA),
        ("#section-2", LinkType.ANCHOR),
        ("http://example.org", LinkType.EXTERNAL),
        ("https://example.org/path", LinkType.EXTERNAL),
        ("//cdn.example.org/lib.js", LinkType.EXTERNAL),
        ("/about.html", LinkType.ABSOLUTE),
        ("/assets/img/logo.png", LinkType.ABSOLUTE),
        ("about.html", LinkType.RELATIVE),
        ("../img/logo.png", LinkType.RELATIVE),
        ("page.html#section", LinkType.RELATIVE),  # fragment de fin, pas une ancre pure (voir docstring)
    ],
)
def test_classify_link_type(url: str, expected: LinkType) -> None:
    assert classify_link_type(url) == expected


@pytest.mark.parametrize(
    ("link_type", "expected"),
    [
        (LinkType.ABSOLUTE, True),
        (LinkType.RELATIVE, True),
        (LinkType.EXTERNAL, False),
        (LinkType.ANCHOR, False),
        (LinkType.MAILTO, False),
        (LinkType.TEL, False),
        (LinkType.JAVASCRIPT, False),
        (LinkType.DATA, False),
        (LinkType.EMPTY, False),
    ],
)
def test_is_internal(link_type: LinkType, expected: bool) -> None:
    assert is_internal(link_type) is expected
