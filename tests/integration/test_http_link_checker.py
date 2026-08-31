from pytest_httpserver import HTTPServer

from omega_fold.core.enums import LinkStatus
from omega_fold.infrastructure.network.http_link_checker import HttpLinkChecker


def test_check_2xx_is_exists(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/ok", method="HEAD").respond_with_data("", status=200)
    status, code, error = HttpLinkChecker().check(httpserver.url_for("/ok"), timeout=2.0)
    assert status == LinkStatus.EXISTS
    assert code == 200
    assert error is None


def test_check_falls_back_to_get_when_head_not_allowed(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/get-only", method="HEAD").respond_with_data("", status=405)
    httpserver.expect_request("/get-only", method="GET").respond_with_data("ok", status=200)
    status, code, _ = HttpLinkChecker().check(httpserver.url_for("/get-only"), timeout=2.0)
    assert status == LinkStatus.EXISTS
    assert code == 200


def test_check_3xx_is_redirect(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/moved", method="HEAD").respond_with_data(
        "", status=301, headers={"Location": "/new"}
    )
    status, code, _ = HttpLinkChecker().check(httpserver.url_for("/moved"), timeout=2.0)
    assert status == LinkStatus.REDIRECT
    assert code == 301


def test_check_404_is_broken(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/missing", method="HEAD").respond_with_data("", status=404)
    status, code, _ = HttpLinkChecker().check(httpserver.url_for("/missing"), timeout=2.0)
    assert status == LinkStatus.BROKEN
    assert code == 404


def test_check_500_is_broken(httpserver: HTTPServer) -> None:
    httpserver.expect_request("/error", method="HEAD").respond_with_data("", status=500)
    status, code, _ = HttpLinkChecker().check(httpserver.url_for("/error"), timeout=2.0)
    assert status == LinkStatus.BROKEN
    assert code == 500


def test_check_connection_error_is_error_status() -> None:
    status, code, error = HttpLinkChecker().check("http://127.0.0.1:1/", timeout=0.5)
    assert status == LinkStatus.ERROR
    assert code is None
    assert error is not None


def test_check_malformed_url_is_error_status_not_raised() -> None:
    """Regression : un href extrait d'un HTML casse/dynamique peut
    contenir un caractere non imprimable (ex. un template JS mal
    interprete comme lien) — `httpx.InvalidURL` n'est PAS une sous-classe
    de `httpx.HTTPError`, donc pas rattrapee par le except existant :
    faisait planter tout le scan (bug reel signale par l'utilisateur,
    message exact : "INVALID non-printable ASCII character in url")."""
    status, code, error = HttpLinkChecker().check("http://example.org/\n{bad}", timeout=2.0)
    assert status == LinkStatus.ERROR
    assert code is None
    assert error is not None
