import time

from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Request, Response

from omega_fold.infrastructure.network.aiohttp_crawler import AiohttpCrawler

_UA = "omega-fold-test/1.0"


async def test_fetch_html_page(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/").respond_with_data(
        "<html><body>hello</body></html>", content_type="text/html"
    )
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/"), timeout=2.0, user_agent=_UA, respect_robots=False)

    assert page.status_code == 200
    assert page.content_type is not None and page.content_type.startswith("text/html")
    assert page.html_body == "<html><body>hello</body></html>"
    assert page.allowed_by_robots is True


async def test_fetch_non_html_page_has_no_body(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/logo.png").respond_with_data(b"\x89PNG", content_type="image/png")
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/logo.png"), timeout=2.0, user_agent=_UA, respect_robots=False)

    assert page.html_body is None


async def test_fetch_sends_configured_user_agent(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/").respond_with_data("ok")
    crawler = AiohttpCrawler()

    await crawler.fetch(httpserver.url_for("/"), timeout=2.0, user_agent=_UA, respect_robots=False)

    request = httpserver.log[0][0]
    assert request.headers.get("User-Agent") == _UA


async def test_respects_robots_txt_disallow(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/robots.txt").respond_with_data(
        "User-agent: *\nDisallow: /private\n", content_type="text/plain"
    )
    httpserver.expect_request("/private").respond_with_data("secret")
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/private"), timeout=2.0, user_agent=_UA, respect_robots=True)

    assert page.allowed_by_robots is False
    assert page.html_body is None


async def test_respects_robots_txt_allow(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/robots.txt").respond_with_data(
        "User-agent: *\nDisallow: /private\n", content_type="text/plain"
    )
    httpserver.expect_request("/public").respond_with_data("<html></html>", content_type="text/html")
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/public"), timeout=2.0, user_agent=_UA, respect_robots=True)

    assert page.allowed_by_robots is True
    assert page.html_body == "<html></html>"


async def test_ignores_robots_txt_when_disabled(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/robots.txt").respond_with_data(
        "User-agent: *\nDisallow: /private\n", content_type="text/plain"
    )
    httpserver.expect_request("/private").respond_with_data("secret", content_type="text/plain")
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/private"), timeout=2.0, user_agent=_UA, respect_robots=False)

    assert page.allowed_by_robots is True
    assert page.status_code == 200


async def test_fetch_timeout_returns_soft_failure_instead_of_raising(httpserver: HTTPServer) -> None:
    """Regression : une seule page lente/injoignable (timeout) faisait
    lever une exception non rattrapee dans fetch(), qui remontait jusqu'a
    interrompre tout le crawl (bug reel signale par l'utilisateur : un
    scan sur 127.0.0.1 qui ne se termine jamais, `TimeoutError`)."""

    def _slow_handler(request: Request) -> Response:
        time.sleep(0.5)
        return Response("trop lent", content_type="text/plain")

    httpserver.expect_request("/slow").respond_with_handler(_slow_handler)
    crawler = AiohttpCrawler()

    page = await crawler.fetch(httpserver.url_for("/slow"), timeout=0.1, user_agent=_UA, respect_robots=False)

    assert page.fetch_error is not None
    assert page.status_code == 0
    assert page.html_body is None


async def test_fetch_connection_refused_returns_soft_failure_instead_of_raising() -> None:
    """Meme regression que ci-dessus, pour une connexion refusee (aucun
    serveur sur ce port) plutot qu'un timeout — deux exceptions bien
    distinctes (`TimeoutError` vs `aiohttp.ClientConnectorError`), toutes
    deux capturees par le meme garde-fou."""
    crawler = AiohttpCrawler()

    page = await crawler.fetch(
        "http://127.0.0.1:1", timeout=2.0, user_agent=_UA, respect_robots=False
    )

    assert page.fetch_error is not None
    assert page.status_code == 0
