from omega_fold.domain.stats.models import ExtensionStats, ExternalDomainStats, FamilyStats, TopFile


def test_extension_stats_defaults() -> None:
    stats = ExtensionStats(extension=".png")
    assert stats.files_count == 0
    assert stats.total_size == 0
    assert stats.percentage_of_total == 0.0


def test_family_stats_holds_extensions() -> None:
    ext = ExtensionStats(extension=".png", files_count=3, total_size=3072, percentage_of_total=12.5)
    family = FamilyStats(family="images", files_count=3, total_size=3072, percentage_of_total=12.5, extensions=[ext])
    assert family.extensions[0] is ext


def test_top_file_defaults() -> None:
    top = TopFile(path="/site/video.mp4", size=104857600, extension=".mp4")
    assert top.links_count == 0


def test_external_domain_stats_defaults() -> None:
    stats = ExternalDomainStats(domain="example.org")
    assert stats.links_count == 0
