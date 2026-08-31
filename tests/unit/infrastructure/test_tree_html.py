from omega_fold.domain.tree.models import DirEntry, FileEntry
from omega_fold.infrastructure.exporters.tree_html import render_tree_html


def _tree() -> DirEntry:
    grandchild = DirEntry(
        path="/site/a/b", name="b", depth=2, files_count=1, dirs_count=0, total_size=5,
        files=[FileEntry(path="/site/a/b/deep.txt", name="deep.txt", extension=".txt", size=5, depth=2, family="text")],
    )
    child = DirEntry(
        path="/site/a", name="a", depth=1, files_count=0, dirs_count=1, total_size=5, children=[grandchild],
    )
    return DirEntry(
        path="/site", name="site", depth=0, files_count=1, dirs_count=1, total_size=15, children=[child],
        files=[FileEntry(path="/site/index.html", name="index.html", extension=".html", size=10, depth=0, family="code")],
    )


def test_root_is_open_but_children_are_closed() -> None:
    html = render_tree_html(_tree())
    assert html.startswith('<details class="tree-folder" open>')
    # Le premier <details> APRES la racine (celui du sous-repertoire "a") n'a pas "open".
    after_root_summary = html.index("</summary>")
    assert '<details class="tree-folder">' in html[after_root_summary:]
    assert '<details class="tree-folder" open>' not in html[after_root_summary:]


def test_all_levels_present() -> None:
    html = render_tree_html(_tree())
    assert "index.html" in html
    assert ">a/<" in html or "📁 a/" in html
    assert ">b/<" in html or "📁 b/" in html
    assert "deep.txt" in html


def test_escapes_dangerous_names() -> None:
    tree = DirEntry(
        path="/site", name="site", depth=0, files_count=1, dirs_count=0, total_size=1,
        files=[FileEntry(path="/site/<script>.html", name="<script>.html", extension=".html", size=1, depth=0, family="code")],
    )
    html = render_tree_html(tree)
    assert "<script>.html" not in html
    assert "&lt;script&gt;.html" in html


def test_tags_are_balanced() -> None:
    html = render_tree_html(_tree())
    assert html.count("<details") == html.count("</details>")
