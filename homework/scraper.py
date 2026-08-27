import re
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from database import save_blogs, wait_for_database


BASE_URL = "https://blog.python.org"
BLOG_URL = "https://blog.python.org/blog/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


def fetch_page(url):
    """
    Download an HTML page.
    """
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.text


def parse_date(date_text):
    """
    Convert a date such as:
        August 24, 2026

    into a Python date object:
        2026-08-24
    """
    date_text = date_text.strip()

    try:
        return datetime.strptime(
            date_text,
            "%B %d, %Y",
        ).date()
    except ValueError:
        return None


def clean_text(text):
    """
    Remove unnecessary whitespace.
    """
    return re.sub(r"\s+", " ", text).strip()


def scrape_blogs(url=BLOG_URL):
    """
    Scrape blog posts from the Python Insider listing page.
    """

    print(f"Scraping: {url}")

    html = fetch_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    blogs = []
    seen_urls = set()

    # Find all links on the page.
    post_links = soup.select("a[href]")

    for link in post_links:
        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(
            BASE_URL,
            href,
        )

        # Python Insider article URLs currently follow:
        # /YYYY/MM/article-name
        if not re.match(
            r"^https://blog\.python\.org/\d{4}/\d{2}/.+",
            full_url,
        ):
            continue

        # Avoid duplicate URLs.
        if full_url in seen_urls:
            continue

        title = clean_text(
            link.get_text(
                " ",
                strip=True,
            )
        )

        # Ignore empty links.
        if not title:
            continue

        # Ignore very short navigation links.
        if len(title) < 5:
            continue

        seen_urls.add(full_url)

        # Find the surrounding article/list container.
        container = (
            link.find_parent("article")
            or link.find_parent("li")
            or link.parent
        )

        if container is None:
            continue

        container_text = clean_text(
            container.get_text(
                " ",
                strip=True,
            )
        )

        author = None
        published_date = None
        description = None

        # --------------------------------------------
        # Extract author
        # --------------------------------------------

        author_element = container.select_one(
            'a[href^="/authors/"]'
        )

        if author_element:
            author = clean_text(
                author_element.get_text(
                    " ",
                    strip=True,
                )
            )

        # --------------------------------------------
        # Extract published date
        # --------------------------------------------

        date_match = re.search(
            r"""
            (
                January|February|March|April|May|June|
                July|August|September|October|November|December
            )
            \s+
            \d{1,2},
            \s+
            \d{4}
            """,
            container_text,
            re.VERBOSE,
        )

        if date_match:
            published_date = parse_date(
                date_match.group(0)
            )

        # --------------------------------------------
        # Extract description
        # --------------------------------------------

        paragraphs = container.find_all("p")

        for paragraph in paragraphs:
            paragraph_text = clean_text(
                paragraph.get_text(
                    " ",
                    strip=True,
                )
            )

            if paragraph_text:
                description = paragraph_text
                break

        blogs.append(
            {
                "title": title,
                "author": author,
                "published_date": published_date,
                "description": description,
                "url": full_url,
            }
        )

    return blogs


def main():
    print("Starting Python blog scraper...")

    # Wait until PostgreSQL is ready.
    wait_for_database()

    # Scrape blog posts.
    blogs = scrape_blogs()

    print(f"Found {len(blogs)} blog posts.")

    if blogs:
        print("\nFirst 5 blog posts:")

        for blog in blogs[:5]:
            print(
                f"- {blog['title']} "
                f"({blog['published_date']})"
            )

        print("\nSaving blogs to PostgreSQL...")

        save_blogs(blogs)

    print("\nScraping completed.")


if __name__ == "__main__":
    main()