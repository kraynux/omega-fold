import time
from datetime import UTC, datetime

from pytest_httpserver import HTTPServer
from werkzeug.wrappers import Request, Response

from omega_fold.application.commands.run_scan import run_scan_distant
from omega_fold.core.enums import LinkStatus, LinkType, ScanMode
from omega_fold.infrastructure.network.aiohttp_crawler import AiohttpCrawler
from omega_fold.infrastructure.network.bs4_link_extractor import Bs4LinkExtractor
from omega_fold.infrastructure.network.http_link_checker import HttpLinkChecker


def _setup_site(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/").respond_with_data(
        """
        <html><body>
          <a href="/about">About</a>
          <a href="/missing">Missing</a>
          <a href="https://example.invalid/">External</a>
        </body></html>
        """,
        content_type="text/html",
    )
    httpserver.expect_request("/about").respond_with_data(
        '<html><body><a href="/">Home</a></body></html>', content_type="text/html"
    )
    httpserver.expect_request("/missing").respond_with_data("not found", status=404)


async def test_run_scan_distant_end_to_end_static(httpserver: HTTPServer) -> None:
    _setup_site(httpserver)
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.STATIC,
        max_depth=3,
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    scan = result.scan
    assert scan.id == "distant-scan-id"
    assert scan.status == "completed"
    assert scan.total_files == 3  # /, /about, /missing (toutes visitees malgre le 404)

    about_link = next(link for link in result.links if link.url == "/about")
    assert about_link.link_type == LinkType.ABSOLUTE
    assert about_link.status == LinkStatus.EXISTS
    assert about_link.status_code == 200

    missing_link = next(link for link in result.links if link.url == "/missing")
    assert missing_link.status == LinkStatus.BROKEN
    assert missing_link.status_code == 404

    external_link = next(link for link in result.links if link.link_type == LinkType.EXTERNAL)
    assert external_link.status == LinkStatus.UNCHECKED  # mode STATIC : jamais verifie

    assert len(result.broken_links) == 1
    assert result.external_domains[0].domain == "example.invalid"


async def test_run_scan_distant_dynamic_mode_checks_external_links(httpserver: HTTPServer) -> None:
    _setup_site(httpserver)
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.DYNAMIC,
        max_depth=3,
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    external_link = next(link for link in result.links if link.link_type == LinkType.EXTERNAL)
    assert external_link.status != LinkStatus.UNCHECKED  # mode DYNAMIC : verifie (ERROR attendu, domaine invalide)


async def test_run_scan_distant_respects_max_depth(httpserver: HTTPServer) -> None:
    _setup_site(httpserver)
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.STATIC,
        max_depth=0,  # ne suit meme pas les liens de la page racine
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    assert result.scan.total_files == 1  # uniquement la racine
    about_link = next(link for link in result.links if link.url == "/about")
    assert about_link.status == LinkStatus.UNCHECKED  # jamais visitee (hors profondeur)


async def test_run_scan_distant_ignores_permalink_redirecting_to_external_site(httpserver: HTTPServer) -> None:
    """Regression : un lien au CHEMIN interne (`/public/distrosea/`, style
    permalien/raccourci) qui redirige en realite vers un domaine externe
    ne doit jamais etre traite comme une page du site scanne — sinon le
    crawl continue sur le site externe en le croyant interne (cas reel
    signale par l'utilisateur : `kraynux.snake-mackarel.ts.net/public/
    Distros/distrosea/` redirige vers le vrai site "distrosea")."""
    external = HTTPServer()
    external.start()
    try:
        external.expect_request("/").respond_with_data(
            '<html><body><a href="/deeper">Deeper</a></body></html>', content_type="text/html"
        )
        external_url = external.url_for("/")

        httpserver.expect_request("/").respond_with_data(
            '<html><body><a href="/public/distrosea/">Distrosea</a></body></html>',
            content_type="text/html",
        )
        # Le chemin ressemble a un dossier interne ; le serveur redirige en
        # realite vers `external_url` (domaine different).
        httpserver.expect_request("/public/distrosea/").respond_with_data(
            "", status=302, headers={"Location": external_url}
        )
        base_url = httpserver.url_for("/")

        result = await run_scan_distant(
            base_url=base_url,
            scan_mode=ScanMode.STATIC,
            max_depth=3,
            max_pages=10,
            delay_ms=0,
            user_agent="omega-fold-test/1.0",
            respect_robots=False,
            distant_crawler=AiohttpCrawler(),
            html_link_extractor=Bs4LinkExtractor(),
            link_checker=HttpLinkChecker(),
            id_factory=lambda: "distant-scan-id",
            now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
            timeout=2.0,
        )

        # La page externe (et son lien "/deeper") n'a jamais ete traitee
        # comme une page du site scanne.
        assert result.scan.total_files == 1  # uniquement la racine
        redirect_link = next(link for link in result.links if link.url == "/public/distrosea/")
        assert redirect_link.status == LinkStatus.UNCHECKED  # ni EXISTS ni BROKEN par supposition
        assert all("/deeper" not in link.url for link in result.links)  # jamais extrait du site externe
    finally:
        external.stop()


async def test_run_scan_distant_classifies_non_html_resources_by_extension(httpserver: HTTPServer) -> None:
    """Regression : les ressources non-HTML (CSS/images/...) d'un scan
    distant recevaient toutes `extension=""`/`family="other"`, quel que
    soit leur type reel (seule la difference "HTML ou pas" etait faite) —
    signale par l'utilisateur avec un scan reel ou 600 fichiers non-HTML
    finissaient tous en "(sans extension)"."""
    httpserver.expect_request("/").respond_with_data(
        '<html><body><link href="/style.css"><img src="/logo.png"></body></html>',
        content_type="text/html",
    )
    httpserver.expect_request("/style.css").respond_with_data("body{}", content_type="text/css")
    httpserver.expect_request("/logo.png").respond_with_data(b"\x89PNG", content_type="image/png")
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.STATIC,
        max_depth=3,
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    assert result.root_dir is not None
    files_by_name = {f.name: f for f in result.root_dir.files}
    assert files_by_name["style.css"].extension == ".css"
    assert files_by_name["style.css"].family == "code"
    assert files_by_name["logo.png"].extension == ".png"
    assert files_by_name["logo.png"].family == "images"
    assert files_by_name["index.html"].extension == ".html"
    assert files_by_name["index.html"].family == "code"


async def test_run_scan_distant_survives_a_page_that_times_out() -> None:
    """Regression : une seule page qui timeout au milieu du crawl ne doit
    pas faire echouer le scan entier — le crawl doit continuer sur les
    pages restantes et se terminer normalement (bug reel signale par
    l'utilisateur : scan qui ne se termine jamais, `TimeoutError`).
    Instance `HTTPServer` dediee (`threaded=True`, pas la fixture
    partagee) : le serveur doit pouvoir traiter `/fast` PENDANT que
    `/slow` dort encore, sinon le test mesurerait un blocage cote serveur
    de test, pas le comportement reel du crawler."""

    def _slow_handler(request: Request) -> Response:
        time.sleep(0.5)
        return Response("trop lent", content_type="text/html")

    server = HTTPServer(threaded=True)
    server.start()
    try:
        server.expect_request("/").respond_with_data(
            '<html><body><a href="/slow">Slow</a><a href="/fast">Fast</a></body></html>',
            content_type="text/html",
        )
        server.expect_request("/slow").respond_with_handler(_slow_handler)
        server.expect_request("/fast").respond_with_data("<html><body>ok</body></html>", content_type="text/html")
        base_url = server.url_for("/")

        result = await run_scan_distant(
            base_url=base_url,
            scan_mode=ScanMode.STATIC,
            max_depth=3,
            max_pages=10,
            delay_ms=0,
            user_agent="omega-fold-test/1.0",
            respect_robots=False,
            distant_crawler=AiohttpCrawler(),
            html_link_extractor=Bs4LinkExtractor(),
            link_checker=HttpLinkChecker(),
            id_factory=lambda: "distant-scan-id",
            now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
            timeout=0.2,
        )

        assert result.scan.status == "completed"
        visited_paths = {f.path for f in result.root_dir.files} if result.root_dir else set()
        assert "/fast" in visited_paths  # la page rapide est quand meme visitee
        assert "/slow" not in visited_paths  # jamais visitee (timeout), pas dans l'arborescence
        slow_link = next(link for link in result.links if link.url == "/slow")
        assert slow_link.status == LinkStatus.UNCHECKED  # ni EXISTS ni BROKEN par supposition
    finally:
        server.stop()


async def test_run_scan_distant_marks_status_truncated_when_max_pages_hit(httpserver: HTTPServer) -> None:
    """Regression : "1000 fichiers trouves" ne disait pas si c'etait la
    taille REELLE du site ou juste la limite --max-pages atteinte (doute
    de fiabilite signale par l'utilisateur) — un site plus grand que
    `max_pages` doit produire un statut distinct, explicite."""
    httpserver.expect_request("/").respond_with_data(
        '<html><body><a href="/a">a</a><a href="/b">b</a><a href="/c">c</a></body></html>',
        content_type="text/html",
    )
    for name in ("a", "b", "c"):
        httpserver.expect_request(f"/{name}").respond_with_data(
            "<html><body>ok</body></html>", content_type="text/html"
        )
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.STATIC,
        max_depth=3,
        max_pages=2,  # le site en a au moins 4 (racine + a/b/c)
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    assert result.scan.status == "completed_truncated"
    assert result.scan.total_files == 2


async def test_run_scan_distant_max_depth_alone_is_not_marked_truncated(httpserver: HTTPServer) -> None:
    """Contrepreuve : atteindre `max_depth` borne intentionnellement la
    portee (demande explicite de l'utilisateur), ce n'est PAS une
    troncature au sens de `completed_truncated` — seul `max_pages`,
    atteint alors qu'il restait des pages en file, l'est."""
    _setup_site(httpserver)
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.STATIC,
        max_depth=0,
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    assert result.scan.status == "completed"


async def test_run_scan_distant_survives_a_malformed_external_link_in_dynamic_mode(
    httpserver: HTTPServer,
) -> None:
    """Regression : un href malforme (caractere non imprimable, ex. un
    template JS mal interprete comme lien) verifie en mode DYNAMIC levait
    `httpx.InvalidURL`, non rattrapee — faisait planter tout le scan (bug
    reel signale par l'utilisateur, message exact : "INVALID
    non-printable ASCII character in url"). Le lien malforme doit rester
    ERROR, le reste du scan doit continuer normalement."""
    httpserver.expect_request("/").respond_with_data(
        '<html><body><a href="/about">About</a><a href="\n{bad}">Bad</a></body></html>',
        content_type="text/html",
    )
    httpserver.expect_request("/about").respond_with_data("<html><body>ok</body></html>", content_type="text/html")
    base_url = httpserver.url_for("/")

    result = await run_scan_distant(
        base_url=base_url,
        scan_mode=ScanMode.DYNAMIC,
        max_depth=3,
        max_pages=10,
        delay_ms=0,
        user_agent="omega-fold-test/1.0",
        respect_robots=False,
        distant_crawler=AiohttpCrawler(),
        html_link_extractor=Bs4LinkExtractor(),
        link_checker=HttpLinkChecker(),
        id_factory=lambda: "distant-scan-id",
        now=lambda: datetime(2026, 8, 31, tzinfo=UTC),
        timeout=2.0,
    )

    assert result.scan.status == "completed"
    about_link = next(link for link in result.links if link.url == "/about")
    assert about_link.status == LinkStatus.EXISTS
