# Copyright (c) 2026 kraynux - Licence MIT
"""Implementation reelle du port LinkChecker pour un lien EXTERNE
(OMEGA-FOLD_SPECIFICATIONS.md §5.3) : HEAD d'abord, GET si HEAD echoue ou
n'est pas supporte (405/501). `httpx` (sync) plutot que `aiohttp` : le
port `LinkChecker.check` est synchrone par contrat (voir ports/
link_checker.py) — appele depuis un contexte async via
`asyncio.to_thread` si besoin (voir application/commands/run_scan.py::
run_scan_distant), pas de bridge async/sync a construire ici."""
from __future__ import annotations

import httpx

from omega_fold.core.enums import LinkStatus

_METHOD_NOT_ALLOWED = 405
_NOT_IMPLEMENTED = 501


class HttpLinkChecker:
    """Implemente ports/link_checker.py::LinkChecker."""

    def check(self, url: str, *, timeout: float) -> tuple[LinkStatus, int | None, str | None]:
        try:
            with httpx.Client(follow_redirects=False, timeout=timeout) as client:
                response = client.head(url)
                if response.status_code in (_METHOD_NOT_ALLOWED, _NOT_IMPLEMENTED):
                    response = client.get(url)
        except httpx.TimeoutException:
            return LinkStatus.TIMEOUT, None, "delai depasse"
        except httpx.HTTPError as exc:
            return LinkStatus.ERROR, None, str(exc)
        except httpx.InvalidURL as exc:
            # PAS une sous-classe de httpx.HTTPError (bug reel signale par
            # l'utilisateur : "INVALID non-printable ASCII character in url"
            # — un href extrait d'un HTML casse/dynamique, ex. un template
            # JS mal interprete comme lien, faisait planter tout le scan
            # sans etre rattrape par le except ci-dessus). Un lien mal
            # forme n'est ni EXISTS ni BROKEN, juste jamais verifiable.
            return LinkStatus.ERROR, None, str(exc)

        return self._status_from_code(response.status_code), response.status_code, None

    @staticmethod
    def _status_from_code(status_code: int) -> LinkStatus:
        if 200 <= status_code < 300:
            return LinkStatus.EXISTS
        if 300 <= status_code < 400:
            return LinkStatus.REDIRECT
        return LinkStatus.BROKEN
