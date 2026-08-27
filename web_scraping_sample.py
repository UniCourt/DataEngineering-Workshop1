import logging
import os
from datetime import datetime
from urllib.parse import urljoin

import psycopg2
import requests
from bs4 import BeautifulSoup


BLOG_URL = os.getenv("BLOG_URL", "https://blog.python.org/blog")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "20"))
MAX_PAGES = int(os.getenv("MAX_PAGES", "100"))


def fetch_page(session, url):
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def parse_posts(html, page_url):
    soup = BeautifulSoup(html, "html5lib")
    posts = []

    for card in soup.select("article.post-card"):
        link = card.select_one("a[href]")
        title_element = card.select_one("h3")
        date_element = card.select_one("time[datetime]")
        if link is None or title_element is None:
            continue

        published_at = None
        if date_element is not None:
            try:
                published_at = datetime.fromisoformat(
                    date_element["datetime"].replace("Z", "+00:00")
                )
            except ValueError:
                logging.warning("Ignoring invalid publication date for %s", link["href"])

        posts.append(
            {
                "title": title_element.get_text(" ", strip=True),
                "url": urljoin(page_url, link["href"]),
                "published_at": published_at,
            }
        )

    next_link = soup.select_one('a[rel="next"]')
    if next_link is None:
        next_link = next(
            (
                link
                for link in soup.find_all("a", href=True)
                if link.get_text(" ", strip=True).lower().startswith(("next", "older posts"))
            ),
            None,
        )

    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return posts, next_url


def scrape_posts(start_url):
    posts = []
    visited_urls = set()
    next_url = start_url

    with requests.Session() as session:
        for _ in range(MAX_PAGES):
            if not next_url or next_url in visited_urls:
                break
            visited_urls.add(next_url)

            try:
                html = fetch_page(session, next_url)
            except requests.RequestException:
                logging.exception("Could not fetch blog page: %s", next_url)
                if not posts:
                    raise
                break

            page_posts, next_url = parse_posts(html, next_url)
            posts.extend(page_posts)

    unique_posts = {post["url"]: post for post in posts}
    return list(unique_posts.values())


def database_config():
    return {
        "host": os.environ["POSTGRES_HOST"],
        "port": os.environ.get("POSTGRES_PORT", "5432"),
        "dbname": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }


def save_posts(posts):
    connection = None
    try:
        connection = psycopg2.connect(**database_config())
        with connection:
            with connection.cursor() as cursor:
                with open("schema.sql", encoding="utf-8") as schema_file:
                    cursor.execute(schema_file.read())
                cursor.executemany(
                    """
                    INSERT INTO blog_posts (title, url, published_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (url) DO NOTHING
                    """,
                    [
                        (post["title"], post["url"], post["published_at"])
                        for post in posts
                    ],
                )
    except (OSError, psycopg2.Error):
        logging.exception("Could not save blog posts to PostgreSQL")
        raise
    finally:
        if connection is not None:
            connection.close()


def main():
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    posts = scrape_posts(BLOG_URL)
    save_posts(posts)
    logging.info("Saved %d blog posts", len(posts))


if __name__ == "__main__":
    main()

