"""
scraper.py
----------
Scrapes blog posts from https://blog.python.org/ (Python Insider, the
official CPython blog) and saves them into PostgreSQL.

SITE STRUCTURE (verified by inspecting the live site):
  - Listing pages: https://blog.python.org/blog  (page 1)
                    https://blog.python.org/blog/2, /blog/3, ... (page N)
  - Each post link on a listing page is a relative URL shaped like
        /2026/08/riscv-now-officially-supported
    i.e. /YYYY/MM/slug — this pattern is what we use to reliably pick out
    post links from navigation/author/tag links on the page.
  - Each individual post page has:
        <h1>                      -> the title
        an <a href="/authors/..."> -> the author name + link
        a meta description tag    -> short summary
        the main body text inside <article> (falls back to <main>)
"""

import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from database import init_db, get_session, BlogPost

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
SITE_ROOT = "https://blog.python.org"
LISTING_URL = f"{SITE_ROOT}/blog"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
REQUEST_DELAY_SECONDS = 1.5   # be polite — don't hammer the server
MAX_LISTING_PAGES = 3         # how many listing pages to crawl (each has ~20 posts)
MAX_POSTS = 30                # overall cap on how many individual posts to save

# A post URL always looks like /YYYY/MM/slug  (with an optional trailing slash)
POST_PATH_RE = re.compile(r"^/\d{4}/\d{2}/[\w\-]+/?$")


def fetch_page(url: str) -> BeautifulSoup:
    """Download a page and return a parsed BeautifulSoup object."""
    logger.info(f"Fetching: {url}")
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def listing_page_url(page_number: int) -> str:
    """Page 1 is /blog itself; pages 2+ are /blog/2, /blog/3, ..."""
    if page_number == 1:
        return LISTING_URL
    return f"{LISTING_URL}/{page_number}"


def parse_listing_page(soup: BeautifulSoup) -> list[dict]:
    """
    Find every post link on a listing page by matching the /YYYY/MM/slug
    URL pattern — this avoids relying on fragile CSS class names, which
    Astro-generated sites often don't have in a stable, guessable form.
    """
    posts = []
    seen_urls = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        # Normalize to a path-only check (strip domain if present)
        path = href
        if href.startswith(SITE_ROOT):
            path = href[len(SITE_ROOT):]

        if not POST_PATH_RE.match(path):
            continue

        full_url = urljoin(SITE_ROOT, href).rstrip("/")
        if full_url in seen_urls:
            continue

        title = a_tag.get_text(strip=True)
        if not title:
            continue

        seen_urls.add(full_url)
        posts.append({"title": title, "url": full_url})

    logger.info(f"Found {len(posts)} posts on listing page")
    return posts


def parse_post_detail(soup: BeautifulSoup) -> dict:
    """Visit an individual post page and extract author, date, summary, content."""

    # --- Title (fallback only; we already have it from the listing page) ---
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else None

    # --- Author: the first link pointing to /authors/... ---
    author_tag = soup.select_one("a[href*='/authors/']")
    author = author_tag.get_text(strip=True) if author_tag else None

    # --- Date: sits next to the author link, e.g. "Stan Ulbrych / August 24, 2026" ---
    published_date = None
    if author_tag and author_tag.parent:
        parent_text = author_tag.parent.get_text(" ", strip=True)
        # Take whatever follows the author's name and a separator like "/"
        match = re.search(r"/\s*(.+)$", parent_text)
        if match:
            published_date = match.group(1).strip()

    # --- Summary: meta description tag ---
    summary = None
    meta_desc = soup.select_one("meta[name='description']") or soup.select_one("meta[property='og:description']")
    if meta_desc and meta_desc.has_attr("content"):
        summary = meta_desc["content"].strip()

    # --- Full content: prefer <article>, fall back to <main> ---
    content_container = soup.find("article") or soup.find("main")
    content = None
    if content_container:
        parts = content_container.find_all(["p", "h2", "h3", "li"])
        content = "\n\n".join(p.get_text(strip=True) for p in parts if p.get_text(strip=True))

    return {
        "title": title,
        "author": author,
        "published_date": published_date,
        "summary": summary,
        "content": content,
    }


def save_post(session, post_data: dict):
    """Insert a post into the DB, skipping it if the URL already exists."""
    existing = session.query(BlogPost).filter_by(url=post_data["url"]).first()
    if existing:
        logger.info(f"Skipping duplicate: {post_data['title']}")
        return

    blog_post = BlogPost(
        title=post_data["title"],
        url=post_data["url"],
        author=post_data.get("author"),
        published_date=post_data.get("published_date"),
        summary=post_data.get("summary"),
        content=post_data.get("content"),
    )
    session.add(blog_post)
    session.commit()
    logger.info(f"Saved: {post_data['title']}")


def run_scraper():
    """Main entry point: crawl listing pages, then each post's detail page."""
    init_db()
    session = get_session()

    all_posts = []
    try:
        for page_number in range(1, MAX_LISTING_PAGES + 1):
            if len(all_posts) >= MAX_POSTS:
                break
            url = listing_page_url(page_number)
            listing_soup = fetch_page(url)
            page_posts = parse_listing_page(listing_soup)
            if not page_posts:
                logger.info("No more posts found — stopping pagination.")
                break
            all_posts.extend(page_posts)
            time.sleep(REQUEST_DELAY_SECONDS)

        all_posts = all_posts[:MAX_POSTS]

        for post in all_posts:
            try:
                time.sleep(REQUEST_DELAY_SECONDS)
                detail_soup = fetch_page(post["url"])
                details = parse_post_detail(detail_soup)
                # Keep the listing-page title as a reliable fallback
                details["title"] = details.get("title") or post["title"]
                post.update(details)
                save_post(session, post)
            except Exception as e:
                logger.error(f"Failed to process {post['url']}: {e}")

    finally:
        session.close()

    logger.info("Scraping complete.")


if __name__ == "__main__":
    run_scraper()