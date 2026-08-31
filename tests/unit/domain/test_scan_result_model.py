from omega_fold.core.enums import LinkStatus, LinkType, ScanTargetType
from omega_fold.domain.links.models import LinkEntry
from omega_fold.domain.reports.models import ScanResult
from omega_fold.domain.scans.models import Scan
from omega_fold.domain.stats.models import FamilyStats
from omega_fold.domain.tree.models import DirEntry


def test_scan_result_defaults() -> None:
    result = ScanResult(scan=Scan())
    assert result.root_dir is None
    assert result.links == []
    assert result.extension_stats == []
    assert result.family_stats == []
    assert result.top_files_by_size == []
    assert result.top_files_by_links == []
    assert result.external_domains == []
    assert result.broken_links == []


def test_scan_result_full_assembly() -> None:
    scan = Scan(id="abc", target="/site", target_type=ScanTargetType.LOCAL)
    root = DirEntry(path="/site", name="site", depth=0)
    broken = LinkEntry(
        url="/missing.html", link_type=LinkType.ABSOLUTE, source_file="/site/index.html",
        attribute="href", status=LinkStatus.BROKEN,
    )
    result = ScanResult(
        scan=scan,
        root_dir=root,
        links=[broken],
        family_stats=[FamilyStats(family="code", files_count=1)],
        broken_links=[broken],
    )
    assert result.scan.id == "abc"
    assert result.root_dir is root
    assert result.broken_links[0] is broken
    assert result.family_stats[0].family == "code"
