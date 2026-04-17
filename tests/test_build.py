"""Tests for the core build pipeline functions."""

import json
import tempfile
from pathlib import Path

import frontmatter
import yaml

from build import load_config, discover_content, render_markdown, get_rarity


def test_load_config(tmp_path):
    """load_config reads site.yaml and speakers.json correctly."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    site_yaml = {"title": "Test Site", "url": "https://example.com"}
    (data_dir / "site.yaml").write_text(yaml.dump(site_yaml))

    speakers = [{"id": "alice", "name": "Alice", "sessions": []}]
    (data_dir / "speakers.json").write_text(json.dumps(speakers))

    site, spk = load_config(data_dir)
    assert site["title"] == "Test Site"
    assert "alice" in spk
    assert spk["alice"]["name"] == "Alice"


def test_discover_content(tmp_path):
    """discover_content finds .md files and parses frontmatter."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()

    md = "---\ntitle: Test Page\ntemplate: page\n---\n\n# Hello\n\nWorld"
    (content_dir / "test.md").write_text(md)

    pages = discover_content(content_dir)
    assert len(pages) == 1
    assert pages[0]["title"] == "Test Page"
    assert pages[0]["template"] == "page"
    assert pages[0]["url"] == "test.html"
    assert "# Hello" in pages[0]["_body"]


def test_render_markdown():
    """render_markdown converts markdown to HTML."""
    html = render_markdown("# Title\n\nA paragraph with **bold**.")
    assert "<h1>" in html
    assert "<strong>bold</strong>" in html


def test_get_rarity():
    """get_rarity returns correct tier labels."""
    assert get_rarity(1)["tier"] == "common"
    assert get_rarity(3)["tier"] == "uncommon"
    assert get_rarity(5)["tier"] == "rare"
    assert get_rarity(8)["tier"] == "legendary"


def test_generate_llms_txt(tmp_path):
    """generate_llms_txt creates llms.txt from page metadata."""
    site = {"title": "Test Site", "url": "https://example.com"}
    pages = [
        {"title": "Home", "url": "index.html", "template": "index", "description": "Home page"},
        {"title": "Session A", "url": "session-a.html", "template": "session", "description": "A session", "day": "monday"},
    ]
    output_dir = tmp_path / "docs"
    output_dir.mkdir()

    from build import generate_llms_txt
    generate_llms_txt(site, pages, output_dir)

    llms = (output_dir / "llms.txt").read_text()
    assert "Test Site" in llms
    assert "session-a.html" in llms
    assert "Session A" in llms

    llms_full = (output_dir / "llms-full.txt").read_text()
    assert "Test Site" in llms_full
    assert "session-a.html" in llms_full
