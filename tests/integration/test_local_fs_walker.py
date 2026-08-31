from pathlib import Path

from omega_fold.infrastructure.filesystem.local_fs_walker import LocalFsWalker


def test_read_tree_real_directory(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text("<html></html>", encoding="utf-8")
    img_dir = tmp_path / "img"
    img_dir.mkdir()
    (img_dir / "logo.png").write_bytes(b"\x89PNG" + b"0" * 96)

    walker = LocalFsWalker()
    root = walker.read_tree(str(tmp_path))

    assert root.files_count == 1
    assert root.dirs_count == 1
    assert root.total_size == len("<html></html>") + 100

    img = root.children[0]
    assert img.name == "img"
    assert img.files[0].name == "logo.png"
    assert img.files[0].family == "images"
    assert img.files[0].extension == ".png"


def test_read_tree_html_file_gets_code_family(tmp_path: Path) -> None:
    (tmp_path / "page.html").write_text("<html></html>", encoding="utf-8")
    walker = LocalFsWalker()
    root = walker.read_tree(str(tmp_path))
    assert root.files[0].family == "code"
    assert root.files[0].mime_type == "text/html"
    assert root.files[0].is_binary is False


def test_read_tree_missing_directory_raises() -> None:
    walker = LocalFsWalker()
    try:
        walker.read_tree("/this/path/does/not/exist")
    except NotADirectoryError:
        pass
    else:
        raise AssertionError("expected NotADirectoryError")
