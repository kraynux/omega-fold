import pytest

from omega_fold.domain.stats.policies import classify_family


@pytest.mark.parametrize(
    ("extension", "expected"),
    [
        (".png", "images"),
        (".JPG", "images"),  # normalisation en minuscules
        (".pdf", "documents"),
        (".py", "code"),
        (".json", "data"),
        (".zip", "archives"),
        (".woff2", "fonts"),
        (".mp4", "video"),
        (".mp3", "audio"),
        (".md", "text"),
        (".unknownext", "other"),
        ("", "other"),
    ],
)
def test_classify_family(extension: str, expected: str) -> None:
    assert classify_family(extension) == expected


def test_classify_family_priority_first_match_wins() -> None:
    """Si une extension apparaissait dans plusieurs familles, la premiere
    trouvee dans l'ordre d'iteration de FAMILIES l'emporte (spec §3.2) —
    verifie le mecanisme de priorite lui-meme, independamment du fait
    qu'aucun chevauchement reel n'existe dans FAMILIES aujourd'hui."""
    from omega_fold.domain.stats import families

    original = dict(families.FAMILIES)
    try:
        families.FAMILIES.clear()
        families.FAMILIES.update({"first": [".dup"], "second": [".dup"], "other": []})
        assert classify_family(".dup") == "first"
    finally:
        families.FAMILIES.clear()
        families.FAMILIES.update(original)
