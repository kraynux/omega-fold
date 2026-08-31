from omega_fold.infrastructure.network.bs4_link_extractor import Bs4LinkExtractor

_HTML = """
<html>
<head><link rel="stylesheet" href="/style.css"></head>
<body>
  <a href="/about.html">About</a>
  <a href="https://example.org">External</a>
  <img src="img/logo.png">
  <script src="/app.js"></script>
  <form action="/submit"></form>
</body>
</html>
"""


def test_extract_finds_all_tag_attribute_pairs() -> None:
    extractor = Bs4LinkExtractor()
    found = extractor.extract(_HTML)

    assert ("/style.css", "href") in found
    assert ("/about.html", "href") in found
    assert ("https://example.org", "href") in found
    assert ("img/logo.png", "src") in found
    assert ("/app.js", "src") in found
    assert ("/submit", "action") in found
    assert len(found) == 6


def test_extract_ignores_tags_without_the_attribute() -> None:
    extractor = Bs4LinkExtractor()
    found = extractor.extract("<a name='no-href-here'>anchor</a>")
    assert found == []
