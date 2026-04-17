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
            "ai-the-right-way.html", "vega-reports.html", "resource-sharing.html",
            "sierra-year-in-review.html", "floating-collections-bof.html", "meep.html",
            "executive-panel.html", "cataloging-without-oclc.html",
            "sierra-sso.html", "sierra-sys-admin-forum.html",
            "cloudflare-sierra-guide.html", "sierra-sso-guide.html",
            "suggest-a-purchase.html",
        }
        missing = expected - html_files
        assert not missing, f"Missing pages: {missing}"
