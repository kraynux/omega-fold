import pytest

from omega_fold.domain.stats.formatting import format_size


@pytest.mark.parametrize(
    ("size_bytes", "expected"),
    [
        (0, "0 o"),
        (823, "823 o"),
        (1024, "1.0 Ko"),
        (1536, "1.5 Ko"),
        (1_900_000_000, "1.8 Go"),
        (1024**4, "1.0 To"),
    ],
)
def test_format_size(size_bytes: int, expected: str) -> None:
    assert format_size(size_bytes) == expected
