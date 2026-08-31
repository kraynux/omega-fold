from omega_fold.core.enums import ScanMode, ScanTargetType
from omega_fold.domain.scans.models import Scan


def test_scan_defaults() -> None:
    scan = Scan()
    assert scan.id is None
    assert scan.target_type == ScanTargetType.LOCAL
    assert scan.scan_mode == ScanMode.STATIC
    assert scan.status == "running"
    assert scan.total_files == 0
    assert scan.total_dirs == 0
    assert scan.total_size == 0
    assert scan.max_depth == 0
    assert scan.total_links == 0
    assert scan.internal_links == 0
    assert scan.external_links == 0
    assert scan.broken_links == 0


def test_scan_construction_with_values() -> None:
    scan = Scan(
        id="abc123",
        created_at="2026-08-31T00:00:00+00:00",
        target="https://example.org",
        target_type=ScanTargetType.DISTANT,
        scan_mode=ScanMode.DYNAMIC,
        status="completed",
        total_files=42,
        total_dirs=5,
        total_size=123456,
        max_depth=3,
        total_links=10,
        internal_links=7,
        external_links=3,
        broken_links=1,
    )
    assert scan.id == "abc123"
    assert scan.target_type == ScanTargetType.DISTANT
    assert scan.scan_mode == ScanMode.DYNAMIC
    assert scan.status == "completed"
    assert scan.total_files == 42
    assert scan.broken_links == 1
