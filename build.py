#!/usr/bin/env python3
"""Static site builder for IUG conference notes."""

import argparse
import http.server
import json
import re
import shutil
import threading
from pathlib import Path

import frontmatter
import mistune
import yaml
from jinja2 import Environment, FileSystemLoader

# Directories (defaults, overridable for testing)
ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content"
TEMPLATE_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "docs"
PHOTOS_DIR = ROOT / "photos"
TRANSCRIPTS_DIR = ROOT / "transcripts"


def load_config(data_dir=None):
    """Load site.yaml and speakers.json. Returns (site_dict, speakers_by_id)."""
    data_dir = data_dir or DATA_DIR
    with open(data_dir / "site.yaml") as f:
        site = yaml.safe_load(f)
    with open(data_dir / "speakers.json") as f:
        speakers_list = json.load(f)
    speakers = {s["id"]: s for s in speakers_list}
    return site, speakers


def discover_content(content_dir=None):
    """Find all .md files in content/ and parse frontmatter + body."""
    content_dir = content_dir or CONTENT_DIR
    pages = []
    for md_file in sorted(content_dir.glob("*.md")):
        post = frontmatter.load(md_file)
        url = md_file.stem + ".html"
        page = dict(post.metadata)
        page["url"] = url
        page["_body"] = post.content
        page["_source"] = md_file.name
        pages.append(page)
    return pages


def render_markdown(text):
    """Convert markdown text to HTML.

    Preprocesses to:
    1. Strip leading whitespace from HTML lines (prevents code block treatment)
    2. Bridge blank lines inside nested HTML (prevents block splitting)
    """
    BLOCK_TAGS = (
        r"(?:div|ul|ol|table|section|article|nav|aside|header|footer"
        r"|main|details|figure|blockquote|form|fieldset|dl|pre)"
    )

    lines = text.split("\n")
    processed = []
    depth = 0

    for line in lines:
        stripped = line.lstrip()

        # Strip indentation from HTML lines
        if stripped.startswith("<") or stripped.startswith("</"):
            line = stripped

        # Track block-level HTML depth
        opens = len(re.findall(rf"<{BLOCK_TAGS}\b", line, re.I))
        closes = len(re.findall(rf"</{BLOCK_TAGS}\b", line, re.I))
        depth = max(0, depth + opens - closes)

        # Bridge blank lines inside nested HTML blocks to prevent
        # mistune from ending the HTML block prematurely
        if stripped == "" and depth > 0:
            processed.append("<!-- -->")
        else:
            processed.append(line)

    return mistune.html("\n".join(processed))


def get_rarity(session_count):
    """Compute speaker rarity tier from session count."""
    if session_count >= 8:
        return {"tier": "legendary", "label": "Legendary"}
    if session_count >= 5:
        return {"tier": "rare", "label": "Rare"}
    if session_count >= 3:
        return {"tier": "uncommon", "label": "Uncommon"}
    return {"tier": "common", "label": "Common"}


def enrich_speakers(speakers):
    """Add computed fields (rarity, unique years, unique tracks) to each speaker."""
    for sid, speaker in speakers.items():
        sessions = speaker.get("sessions", [])
        speaker["rarity"] = get_rarity(len(sessions))
        speaker["unique_years"] = sorted(set(s["year"] for s in sessions), reverse=True)
        speaker["unique_tracks"] = sorted(set(s.get("track", "general") for s in sessions))
        speaker["sessions_sorted"] = sorted(sessions, key=lambda s: s["year"], reverse=True)
        speaker["session_count"] = len(sessions)
        speaker["year_count"] = len(speaker["unique_years"])
        speaker["track_count"] = len(speaker["unique_tracks"])
    return speakers


def get_sessions_for_day(pages, day):
    """Return all session pages for a given day, sorted by time."""
    return [p for p in pages if p.get("day") == day and p.get("template") == "session"]


def generate_llms_txt(site, pages, output_dir=None):
    """Generate llms.txt and llms-full.txt for AI agent navigation."""
    output_dir = output_dir or OUTPUT_DIR

    # Categorize pages
    sessions = [p for p in pages if p.get("template") == "session"]
    day_pages = [p for p in pages if p.get("template") == "day"]
    guides = [p for p in pages if p.get("template") == "page"]
    special = [p for p in pages if p.get("template") in ("index", "speakers")]

    lines = []
    lines.append(f"# {site['title']}")
    lines.append(f"> {site.get('url', '')}")
    lines.append("")
    lines.append("Conference knowledge base with session notes, technical guides, and speaker data.")
    lines.append("")

    if special:
        lines.append("## Pages")
        for p in special:
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    if day_pages:
        lines.append("## Day Overviews")
        for p in sorted(day_pages, key=lambda p: p.get("date", "")):
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    if sessions:
        lines.append("## Sessions")
        for p in sorted(sessions, key=lambda p: (p.get("day", ""), p.get("title", ""))):
            day = p.get("day", "")
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')} [{day}]")
        lines.append("")

    if guides:
        lines.append("## Guides")
        for p in guides:
            lines.append(f"- [{p['title']}]({p['url']}): {p.get('description', '')}")
        lines.append("")

    lines.append("## Structured Data")
    lines.append("- [speakers.json](speakers-data.json): Full speaker database with session history")
    lines.append("")

    repo = site.get("repo", "")
    lines.append("## Corrections & Contributions")
    lines.append("")
    lines.append("Found an error or want to suggest a correction?")
    lines.append("")
    lines.append(f"- **File an issue:** {repo}/issues/new?title=Correction&body=Page:%20(which%20page)%0A%0ACorrection:%20(describe%20the%20issue)")
    lines.append(f"- **Browse open issues:** {repo}/issues")
    lines.append(f"- **Submit a pull request:** Fork {repo}, edit the relevant markdown file in `content/`, and open a PR.")
    lines.append("")
    lines.append("Content source files are markdown with YAML frontmatter in the `content/` directory.")
    lines.append("")

    (output_dir / "llms.txt").write_text("\n".join(lines))

    # llms-full.txt: include rendered content
    full_lines = list(lines)
    full_lines.append("---")
    full_lines.append("")
    for p in pages:
        full_lines.append(f"# {p['title']}")
        full_lines.append(f"URL: {p['url']}")
        if p.get("description"):
            full_lines.append(f"Description: {p['description']}")
        full_lines.append("")
        body = p.get("_body", "")
        if body.strip():
            full_lines.append(body.strip())
        else:
            full_lines.append("(Template-driven page — see structured data)")
        full_lines.append("")
        full_lines.append("---")
        full_lines.append("")

    (output_dir / "llms-full.txt").write_text("\n".join(full_lines))
    print("  Generated llms.txt and llms-full.txt")


def build_site():
    """Run the full build pipeline."""
    print("Building site...")
    site, speakers = load_config()
    speakers = enrich_speakers(speakers)
    pages = discover_content()

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    for page in pages:
        template_name = page.get("template", "page") + ".html"
        template = env.get_template(template_name)

        content_html = render_markdown(page["_body"])

        # Compute nav_active: for sessions, highlight the parent day
        if page.get("day"):
            nav_active = page["day"] + ".html"
        else:
            nav_active = page["url"]

        html = template.render(
            site=site,
            page=page,
            content=content_html,
            speakers=speakers,
            pages=pages,
            nav_active=nav_active,
            get_sessions_for_day=get_sessions_for_day,
        )

        out_path = OUTPUT_DIR / page["url"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html)
        print(f"  {page['url']}")

    # Generate agent navigation files
    generate_llms_txt(site, pages)

    # Copy static assets
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
        print(f"  Copied static/")

    # Copy photos
    if PHOTOS_DIR.exists():
        shutil.copytree(PHOTOS_DIR, OUTPUT_DIR / "photos", dirs_exist_ok=True)
        print(f"  Copied photos/")

    # Copy transcripts
    if TRANSCRIPTS_DIR.exists():
        shutil.copytree(TRANSCRIPTS_DIR, OUTPUT_DIR / "transcripts", dirs_exist_ok=True)
        print(f"  Copied transcripts/")

    print(f"Built {len(pages)} pages -> {OUTPUT_DIR}/")


def clean():
    """Remove the output directory."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
        print(f"Cleaned {OUTPUT_DIR}/")


def serve_and_watch(port):
    """Start HTTP server and file watcher. Blocks until Ctrl+C."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)

        def log_message(self, format, *args):
            # Suppress per-request logs to keep rebuild output visible
            pass

    server = http.server.HTTPServer(("0.0.0.0", port), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    print(f"Serving on http://0.0.0.0:{port}")

    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer

        class RebuildHandler(FileSystemEventHandler):
            def __init__(self):
                self._timer = None

            def on_any_event(self, event):
                if event.src_path.startswith(str(OUTPUT_DIR)):
                    return
                if self._timer:
                    self._timer.cancel()
                self._timer = threading.Timer(0.3, self._rebuild)
                self._timer.start()

            def _rebuild(self):
                print("\nChange detected, rebuilding...")
                try:
                    build_site()
                    print("Ready.")
                except Exception as e:
                    print(f"Build error: {e}")

        observer = Observer()
        handler = RebuildHandler()
        for watch_dir in [CONTENT_DIR, TEMPLATE_DIR, STATIC_DIR, DATA_DIR]:
            if watch_dir.exists():
                observer.schedule(handler, str(watch_dir), recursive=True)
        observer.start()
        print("Watching for changes... (Ctrl+C to stop)")

        server_thread.join()
    except KeyboardInterrupt:
        print("\nStopping...")
        observer.stop()
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Build the IUG conference site")
    parser.add_argument("--clean", action="store_true", help="Clean output before building")
    parser.add_argument("--dev", action="store_true", help="Build, serve, and watch")
    parser.add_argument("--port", type=int, default=8000, help="Dev server port")
    args = parser.parse_args()

    if args.clean:
        clean()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    build_site()

    if args.dev:
        serve_and_watch(args.port)


if __name__ == "__main__":
    main()
