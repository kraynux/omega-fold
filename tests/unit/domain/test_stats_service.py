from omega_fold.core.enums import LinkType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.stats.service import (
    compute_extension_stats,
    compute_external_domain_stats,
    compute_family_stats,
    compute_top_files_by_links,
    compute_top_files_by_size,
)
from omega_fold.domain.tree.models import FileEntry


def _file(path: str, extension: str, size: int, family: str) -> FileEntry:
    return FileEntry(path=path, name=path.rsplit("/", 1)[-1], extension=extension, size=size, depth=1, family=family)


_FILES = [
    _file("/site/index.html", ".html", 300, "code"),
    _file("/site/about.html", ".html", 100, "code"),
    _file("/site/logo.png", ".png", 400, "images"),
    _file("/site/photo.png", ".png", 200, "images"),
]


def test_compute_extension_stats_sorted_by_size_desc() -> None:
    stats = compute_extension_stats(_FILES)
    assert [s.extension for s in stats] == [".png", ".html"]
    png = stats[0]
    assert png.files_count == 2
    assert png.total_size == 600
    assert png.percentage_of_total == 60.0


def test_compute_extension_stats_empty_list_no_division_error() -> None:
    assert compute_extension_stats([]) == []


def test_compute_family_stats_nests_extension_stats() -> None:
    stats = compute_family_stats(_FILES)
    assert [s.family for s in stats] == ["images", "code"]
    images = stats[0]
    assert images.files_count == 2
    assert images.total_size == 600
    assert images.extensions[0].extension == ".png"


def test_compute_top_files_by_size() -> None:
    top = compute_top_files_by_size(_FILES, limit=2)
    assert [t.path for t in top] == ["/site/logo.png", "/site/index.html"]


def test_compute_top_files_by_links_only_files_with_outgoing_links() -> None:
    links = [
        LinkEntry(url="/about.html", link_type=LinkType.ABSOLUTE, source_file="/site/index.html", attribute="href"),
        LinkEntry(url="/logo.png", link_type=LinkType.ABSOLUTE, source_file="/site/index.html", attribute="src"),
    ]
    top = compute_top_files_by_links(_FILES, links)
    assert len(top) == 1
    assert top[0].path == "/site/index.html"
    assert top[0].links_count == 2


def test_compute_external_domain_stats() -> None:
    links = [
        LinkEntry(url="https://example.org/a", link_type=LinkType.EXTERNAL, source_file="x", attribute="href"),
        LinkEntry(url="https://example.org/b", link_type=LinkType.EXTERNAL, source_file="x", attribute="href"),
        LinkEntry(url="https://other.org/c", link_type=LinkType.EXTERNAL, source_file="x", attribute="href"),
        LinkEntry(url="/internal.html", link_type=LinkType.ABSOLUTE, source_file="x", attribute="href"),
    ]
    stats = compute_external_domain_stats(links)
    assert stats[0].domain == "example.org"
    assert stats[0].links_count == 2
    assert stats[1].domain == "other.org"
    assert stats[1].links_count == 1
