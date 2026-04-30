"""Tests for the IUG 2026 conference site build."""

import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "docs"


@pytest.fixture(scope="session", autouse=True)
def build_site():
    """Run the build once before all tests."""
    result = subprocess.run(
        ["uv", "run", "python", "build.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Build failed:\n{result.stderr}"


def get_html_files():
    """Return all built HTML files."""
    return sorted(OUTPUT_DIR.glob("*.html"))


class TestBuildCompleteness:
    def test_expected_pages_built(self):
        """All expected pages should be present in docs/."""
        html_files = {f.name for f in get_html_files()}
        expected = {
            "index.html",
            "sunday.html", "monday.html", "tuesday.html", "wednesday.html",
            "speakers.html",
            "sierra-roadmap.html", "hackathon-awards.html", "amazon-business.html",
            "ai-the-right-way.html", "ai-the-right-way-ray-notes.html",
            "vega-reports.html", "resource-sharing.html",
            "sierra-year-in-review.html", "floating-collections-bof.html", "meep.html",
            "executive-panel.html", "cataloging-without-oclc.html",
            "sierra-sso.html", "sierra-sys-admin-forum.html",
            "cloudflare-sierra-guide.html", "sierra-sso-guide.html",
            "suggest-a-purchase.html",
            "about.html",
        }
        missing = expected - html_files
        assert not missing, f"Missing pages: {missing}"


class TestContentIntegrity:
    def test_no_escaped_html_in_output(self):
        """No page should contain HTML that mistune escaped into code blocks."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            if "<pre><code>&lt;div" in content or "<pre><code>&lt;p" in content:
                failures.append(html_file.name)
        assert not failures, f"Pages with escaped HTML: {failures}"

    def test_no_duplicate_dates_in_subtitles(self):
        """Session subtitles should not repeat the date."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            match = re.search(
                r'class="page-subtitle">(.*?)</p>', content, re.DOTALL
            )
            if match:
                subtitle = match.group(1)
                dates = re.findall(r"(?:Monday|Tuesday|Wednesday|Sunday),\s+April\s+\d+", subtitle)
                if len(dates) != len(set(dates)):
                    failures.append(f"{html_file.name}: {subtitle.strip()}")
        assert not failures, f"Duplicate dates in subtitles:\n" + "\n".join(failures)

    def test_internal_links_resolve(self):
        """All internal .html links should point to files that exist."""
        failures = []
        for html_file in get_html_files():
            content = html_file.read_text()
            for href in re.findall(r'href="([^"#][^"]*?\.html)', content):
                if href.startswith("http"):
                    continue
                target = OUTPUT_DIR / href
                if not target.exists():
                    failures.append(f"{html_file.name} -> {href}")
        assert not failures, f"Broken internal links:\n" + "\n".join(failures)

    def test_speaker_anchor_links_resolve(self):
        """Speaker anchor links should reference IDs in speakers.html."""
        speakers_html = (OUTPUT_DIR / "speakers.html").read_text()
        speaker_ids = set(re.findall(r'id="([^"]+)"', speakers_html))
        failures = []
        for html_file in get_html_files():
            if html_file.name == "speakers.html":
                continue
            content = html_file.read_text()
            for anchor in re.findall(r'href="speakers\.html#([^"]+)"', content):
                if anchor not in speaker_ids:
                    failures.append(f"{html_file.name} -> speakers.html#{anchor}")
        assert not failures, f"Broken speaker links:\n" + "\n".join(failures)
