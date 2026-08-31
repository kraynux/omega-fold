# Copyright (c) 2026 kraynux - Licence MIT
"""Verification programmatique du balisage genere par
widgets/splash_hero.py — assertions auto-contenues (pas de dependance a
~/DEV/FOLD/ascii.txt, fichier hors du paquet/repo, absent sur toute autre
machine/CI) : la transcription elle-meme a ete verifiee ligne par ligne
contre la source au moment de l'ecriture, ce test couvre la coherence
structurelle du balisage Rich genere (pas de regression future)."""
from __future__ import annotations

from omega_fold.interfaces.tui.widgets.splash_hero import _MARKUP, _RAW_LINES


def test_raw_lines_have_expected_line_count() -> None:
    assert len(_RAW_LINES) == 21


def test_markup_contains_expected_accent_regions() -> None:
    assert "[$accent]LINUX FOLDER ANALYSE[/]" in _MARKUP
    assert "[$accent]|[/]" in _MARKUP


def test_markup_contains_wordmark_and_tagline_text() -> None:
    assert "V1.00" in _MARKUP
    assert "SCAN" in _MARKUP and "FOLDER" in _MARKUP and "EXPORT" in _MARKUP


def test_markup_is_balanced() -> None:
    open_tags = sum(
        _MARKUP.count(f"[{token}]")
        for token in ("$accent", "$foreground", "$secondary", "dim $foreground", "dim $secondary")
    )
    assert open_tags == _MARKUP.count("[/]")
    assert open_tags > 0
