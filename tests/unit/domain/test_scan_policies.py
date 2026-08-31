import pytest

from omega_fold.domain.scans.policies import (
    is_depth_allowed,
    is_page_count_allowed,
    is_same_domain,
    normalize_distant_target,
)


@pytest.mark.parametrize(
    ("current_depth", "max_depth", "expected"),
    [(0, 3, True), (2, 3, True), (3, 3, False), (4, 3, False)],
)
def test_is_depth_allowed(current_depth: int, max_depth: int, expected: bool) -> None:
    assert is_depth_allowed(current_depth, max_depth) is expected


@pytest.mark.parametrize(
    ("current_count", "max_pages", "expected"),
    [(0, 10, True), (9, 10, True), (10, 10, False), (11, 10, False)],
)
def test_is_page_count_allowed(current_count: int, max_pages: int, expected: bool) -> None:
    assert is_page_count_allowed(current_count, max_pages) is expected


@pytest.mark.parametrize(
    ("url", "base_domain", "expected"),
    [
        ("https://example.org/page", "example.org", True),
        ("http://example.org/page", "example.org", True),
        ("https://EXAMPLE.org/page", "example.org", True),
        ("https://other.org/page", "example.org", False),
        ("/relative/path.html", "example.org", True),
        ("page.html", "example.org", True),
    ],
)
def test_is_same_domain(url: str, base_domain: str, expected: bool) -> None:
    assert is_same_domain(url, base_domain) is expected


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("example.org", "https://example.org"),
        ("  example.org  ", "https://example.org"),
        ("http://example.org", "http://example.org"),
        ("https://example.org", "https://example.org"),
        ("HTTPS://example.org", "HTTPS://example.org"),
    ],
)
def test_normalize_distant_target(target: str, expected: str) -> None:
    assert normalize_distant_target(target) == expected
