from omega_fold.domain.tree.models import FileEntry
from omega_fold.domain.tree.service import build_tree


def _file(path: str, size: int, depth: int) -> FileEntry:
    return FileEntry(path=path, name=path.rsplit("/", 1)[-1], extension=".txt", size=size, depth=depth, family="text")


def test_build_tree_root_only_files() -> None:
    files = [_file("/site/a.txt", 100, 1), _file("/site/b.txt", 200, 1)]
    root = build_tree("/site", files)

    assert root.path == "/site"
    assert root.depth == 0
    assert root.files_count == 2
    assert root.dirs_count == 0
    assert root.total_size == 300


def test_build_tree_nested_directories_aggregate_size_only() -> None:
    files = [
        _file("/site/index.html", 100, 1),
        _file("/site/img/logo.png", 50, 2),
        _file("/site/img/icons/star.svg", 25, 3),
    ]
    root = build_tree("/site", files)

    assert root.files_count == 1  # direct seulement
    assert root.dirs_count == 1  # 'img' direct seulement
    assert root.total_size == 175  # recursif : 100 + 50 + 25

    img = root.children[0]
    assert img.path == "/site/img"
    assert img.depth == 1
    assert img.files_count == 1
    assert img.dirs_count == 1
    assert img.total_size == 75  # 50 + 25

    icons = img.children[0]
    assert icons.path == "/site/img/icons"
    assert icons.depth == 2
    assert icons.files_count == 1
    assert icons.total_size == 25


def test_build_tree_empty_intermediate_directory_is_created() -> None:
    """Un repertoire uniquement traverse (aucun fichier direct, un seul
    sous-repertoire) doit quand meme exister dans l'arbre."""
    files = [_file("/site/a/b/c/deep.txt", 10, 3)]
    root = build_tree("/site", files)

    a = root.children[0]
    assert a.path == "/site/a"
    assert a.files_count == 0
    assert a.dirs_count == 1

    b = a.children[0]
    assert b.path == "/site/a/b"
    assert b.files_count == 0

    c = b.children[0]
    assert c.path == "/site/a/b/c"
    assert c.files_count == 1
    assert c.total_size == 10


def test_build_tree_no_files() -> None:
    root = build_tree("/empty", [])
    assert root.files_count == 0
    assert root.dirs_count == 0
    assert root.total_size == 0
    assert root.children == []
