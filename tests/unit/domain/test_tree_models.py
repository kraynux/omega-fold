from omega_fold.domain.tree.models import DirEntry, FileEntry


def test_file_entry_construction() -> None:
    entry = FileEntry(
        path="/site/index.html",
        name="index.html",
        extension=".html",
        size=2048,
        depth=1,
        family="code",
    )
    assert entry.mime_type is None
    assert entry.is_binary is False


def test_dir_entry_defaults() -> None:
    entry = DirEntry(path="/site", name="site", depth=0)
    assert entry.files_count == 0
    assert entry.dirs_count == 0
    assert entry.total_size == 0
    assert entry.children == []
    assert entry.files == []


def test_dir_entry_with_nested_children() -> None:
    child_file = FileEntry(path="/site/img/logo.png", name="logo.png", extension=".png", size=1024, depth=2, family="images")
    child_dir = DirEntry(path="/site/img", name="img", depth=1, files_count=1, total_size=1024, files=[child_file])
    root = DirEntry(path="/site", name="site", depth=0, dirs_count=1, total_size=1024, children=[child_dir])

    assert root.children[0] is child_dir
    assert root.children[0].files[0] is child_file
    assert root.children[0].files[0].family == "images"
