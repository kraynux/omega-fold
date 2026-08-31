from omega_fold.core.enums import ConfidenceLevel, LinkStatus, LinkType
from omega_fold.domain.links.models import LinkEntry


def test_link_entry_defaults() -> None:
    link = LinkEntry(url="/about.html", link_type=LinkType.ABSOLUTE, source_file="/site/index.html", attribute="href")
    assert link.status == LinkStatus.UNCHECKED
    assert link.status_code is None
    assert link.error_message is None
    assert link.confidence == ConfidenceLevel.UNKNOWN
    assert link.target_exists is None


def test_link_entry_verified_broken() -> None:
    link = LinkEntry(
        url="https://example.org/missing",
        link_type=LinkType.EXTERNAL,
        source_file="/site/index.html",
        attribute="href",
        status=LinkStatus.BROKEN,
        status_code=404,
        confidence=ConfidenceLevel.VERIFIED,
        target_exists=False,
    )
    assert link.status_code == 404
    assert link.target_exists is False
