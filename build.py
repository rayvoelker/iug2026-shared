#!/usr/bin/env python3
"""Static site builder for IUG conference notes."""

import argparse
import http.server
import json
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
    """Convert markdown text to HTML."""
    return mistune.html(text)


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
