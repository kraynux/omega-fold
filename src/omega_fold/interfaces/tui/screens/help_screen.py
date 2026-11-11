# Copyright (c) 2026 kraynux - Licence MIT
"""Ecran Aide : reference statique des raccourcis et fonctions de
l'application. Adapte du patron screens/help_screen.py de CHECK/DEEP
(D-007/D-008) — le tableau des profils systeme (sans equivalent FOLD)
est remplace par le catalogue des familles de fichiers
(`domain/stats/families.py::FAMILIES`)."""
from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, DataTable, Footer, Header, Static

from omega_fold.domain.stats.families import FAMILIES
from omega_fold.interfaces.tui.screens._base import OmegaScreen
from omega_fold.interfaces.tui.screens.contact_support import contact_support_screen
from omega_fold.shared.i18n import _

_SHORTCUTS = (
    (_("Haut / Bas"), _("Naviguer entre les éléments d'un écran")),
    (_("Tab / Maj+Tab"), _("Naviguer entre les champs d'un formulaire")),
    (_("Échap"), _("Retour à l'écran précédent (confirmation de sortie sur l'accueil)")),
    ("t", _("Thème suivant (appliqué immédiatement, sans confirmation)")),
    ("r", _("Rafraîchir la détection du terminal")),
    ("a", _("Cette aide")),
    ("q", _("Quitter (avec confirmation)")),
)

_SECTIONS = (
    (
        _("Scanner"),
        (
            _("Saisir une cible (répertoire local ou URL), le type (local/distant), le mode "
              "(statique ou dynamique) et, pour un scan distant, les garde-fous de crawl "
              "(profondeur max, nombre de pages, délai entre requêtes, User-Agent, respect de "
              "robots.txt).")
        ),
    ),
    (
        _("Historique"),
        (
            _("Liste tous les scans passés : détail complet (arborescence, familles, liens "
              "cassés), ou rejouer un scan sur la même cible (un scan distant rejoué utilise "
              "les garde-fous par défaut, pas ceux du scan original — non persistés).")
        ),
    ),
    (
        _("Export"),
        (
            _("Depuis le détail d'un scan : JSON (structure complète), texte (rapport compact) "
              "ou HTML (rapport visuel avec histogramme par famille, thème d'export "
              "indépendant du thème de l'interface).")
        ),
    ),
)

_SCOPE_NOTICE = (
    _("Omega-fold analyse un répertoire local ou crawle un site distant sous des garde-fous "
      "toujours actifs (profondeur, nombre de pages, délai, même domaine) : un lien externe "
      "n'est vérifié par HTTP qu'en mode dynamique, un lien interne est toujours vérifié "
      "contre les fichiers/pages réellement trouvés, jamais par supposition.")
)


class HelpScreen(OmegaScreen):
    """Reference statique, accessible depuis n'importe quel ecran (touche `a`)."""

    def __init__(self, *, container: object | None = None) -> None:
        super().__init__()
        # Aide -> Contact et support (D-016, 2026-11-09) : services prepares par le conteneur de
        # l'outil (app/) ; absents (bouton masque) si l'aide est ouverte sans conteneur.
        self._contact_support = getattr(container, "contact_support", None)

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(classes="omega-panel"):
            yield Static(_("AIDE"), classes="omega-title")
            yield Static(_("Raccourcis clavier"), classes="omega-subtitle")
            for key, description in _SHORTCUTS:
                yield Static(_("{key:<14} {description}").format(key=key, description=description))
            yield Static("")
            yield Static(_("Fonctions"), classes="omega-subtitle")
            for title, description in _SECTIONS:
                yield Static(f"[b]{title}[/b]\n{description}\n")
            yield Static("")
            yield Static(_("Familles de fichiers"), classes="omega-subtitle")
            yield DataTable(id="family-table")
            yield Static("")
            yield Static(_SCOPE_NOTICE, classes="omega-subtitle")
            with Horizontal(classes="omega-actions"):
                if self._contact_support is not None:
                    with Container(classes="omega-btn-frame"):
                        yield Button(_("Contact et support"), id="contact-support", variant="primary")
                with Container(classes="omega-btn-frame"):
                    yield Button(_("Retour"), id="back")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#family-table", DataTable)
        table.add_columns(_("Famille"), _("Extensions"))
        for family, extensions in FAMILIES.items():
            table.add_row(family, ", ".join(extensions) if extensions else _("(le reste)"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.dismiss()
        elif event.button.id == "contact-support" and self._contact_support is not None:
            self.app.push_screen(contact_support_screen(self._contact_support))
