import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://blog.python.org"
LISTING_URL = BASE_URL + "/blog"

# Matches post links like /2026/08/python-31214-31116-31021
POST_LINK_RE = re.compile(r"^/\d{4}/\d{2}/[\w-]+/?$")
# Matches pagination links like /blog/2, /blog/17
PAGE_LINK_RE = re.compile(r"^/blog/(\d+)/?$")

HEADERS = {"User-Agent": "Mozilla/5.0 (workshop-scraper; +https://github.com/mskandashyambhat)"}


def fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.text


def get_total_pages(soup):
    page_numbers = [1]
    for a in soup.find_all("a", href=True):
        m = PAGE_LINK_RE.match(a["href"])
        if m:
            page_numbers.append(int(m.group(1)))
    return max(page_numbers)


def normalize_date(raw):
    """Try to turn whatever date text/attribute we found into a real date."""
    if not raw:
        return None
    raw = raw.strip()
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def parse_listing_page(html):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    seen_links = set()

    for link_tag in soup.find_all("a", href=True):
        href = link_tag["href"]
        if not POST_LINK_RE.match(href):
            continue
        if href in seen_links:
            continue
        title = link_tag.get_text(strip=True)
        if not title:
            continue
        seen_links.add(href)

        # Nearest ancestor block that also holds author/date/summary/tags
        container = link_tag.find_parent(["article", "section", "div", "li"]) or link_tag.parent

        author, author_url = None, None
        author_tag = container.find("a", href=re.compile(r"^/authors/"))
        if author_tag:
            author = author_tag.get_text(strip=True)
            author_url = BASE_URL + author_tag["href"]

        published_date_raw = None
        time_tag = container.find("time")
        if time_tag:
            published_date_raw = time_tag.get("datetime") or time_tag.get_text(strip=True)
        else:
            text = container.get_text(" ", strip=True)
            m = re.search(r"([A-Z][a-z]+ \d{1,2}, \d{4})", text)
            if m:
                published_date_raw = m.group(1)

        tags = [t.get_text(strip=True) for t in container.find_all("a", href=re.compile(r"^/tags/"))]

        summary = None
        p_tag = container.find("p")
        if p_tag:
            summary = p_tag.get_text(strip=True)

        full_url = href if href.startswith("http") else BASE_URL + href

        posts.append({
            "title": title,
            "url": full_url,
            "author": author,
            "author_url": author_url,
            "published_date": normalize_date(published_date_raw),
            "summary": summary,
            "tags": tags,
        })

    return posts


def scrape(max_pages=None, delay=1.0):
    """Scrape all (or up to max_pages) listing pages of blog.python.org/blog"""
    html = fetch(LISTING_URL)
    soup = BeautifulSoup(html, "html.parser")
    total_pages = get_total_pages(soup)
    if max_pages:
        total_pages = min(total_pages, max_pages)

    print(f"[scraper] Found {total_pages} listing page(s) to scrape")

    all_posts = parse_listing_page(html)

    for page_num in range(2, total_pages + 1):
        url = f"{BASE_URL}/blog/{page_num}"
        print(f"[scraper] Fetching {url}")
        page_html = fetch(url)
        all_posts.extend(parse_listing_page(page_html))
        time.sleep(delay)  # be polite to the server

    print(f"[scraper] Scraped {len(all_posts)} posts total")
    return all_posts