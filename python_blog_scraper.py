import time
from datetime import datetime

import requests
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://blog.python.org"
BLOG_URL = f"{BASE_URL}/blog/"

DB_CONFIG = {
    "host": "psql-db",
    "port": 5432,
    "database": "postgres",
    "user": "postgres",
    "password": "123456",
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blog_posts (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                published_date DATE,
                url TEXT UNIQUE NOT NULL,
                summary TEXT
            );
        """)

    conn.commit()


def scrape_page(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = []

    for article in soup.find_all("article"):
        title_element = article.find(["h2", "h3"])
        link_element = article.find("a", href=True)

        if not title_element or not link_element:
            continue

        title = title_element.get_text(" ", strip=True)
        post_url = urljoin(BASE_URL, link_element["href"])

        posts.append({
            "title": title,
            "url": post_url,
        })

    return posts


def get_post_details(url):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Get title
    title_element = soup.find("h1")

    if title_element:
        title = title_element.get_text(" ", strip=True)
    else:
        title = None

    author = None
    published_date = None

    # The Python Blog displays the author and date as:
    # Author / Month Day, Year
    #
    # Example:
    # Hugo van Kemenade / September 1, 2026

    metadata = soup.find(
        string=lambda text: text and " / " in text
    )

    if metadata:
        metadata_text = metadata.strip()

        parts = metadata_text.split(" / ", 1)

        if len(parts) == 2:
            possible_author = parts[0].strip()
            possible_date = parts[1].strip()

            try:
                published_date = datetime.strptime(
                    possible_date,
                    "%B %d, %Y"
                ).date()

                author = possible_author

            except ValueError:
                pass

    # Get summary
    summary = None

    article = soup.find("article")

    if article:
        paragraphs = article.find_all("p")

        if paragraphs:
            summary = paragraphs[0].get_text(
                " ",
                strip=True
            )

    return title, author, published_date, summary


def save_post(conn, post):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO blog_posts
                (title, author, published_date, url, summary)
            VALUES
                (%s, %s, %s, %s, %s)
            ON CONFLICT (url)
            DO UPDATE SET
                title = EXCLUDED.title,
                author = EXCLUDED.author,
                published_date = EXCLUDED.published_date,
                summary = EXCLUDED.summary;
            """,
            (
                post["title"],
                post["author"],
                post["published_date"],
                post["url"],
                post["summary"],
            ),
        )

    conn.commit()


def main():
    print("Connecting to PostgreSQL...")

    conn = get_db_connection()

    try:
        print("Creating table if it does not exist...")

        create_table(conn)

        print("Scraping Python Blog...")

        posts = scrape_page(BLOG_URL)

        print(f"Found {len(posts)} posts")

        for post in posts:
            try:
                (
                    title,
                    author,
                    published_date,
                    summary,
                ) = get_post_details(post["url"])

                post["title"] = title or post["title"]
                post["author"] = author
                post["published_date"] = published_date
                post["summary"] = summary

                save_post(conn, post)

                print(
                    f"Saved: {post['title']} "
                    f"({post['published_date']})"
                )

                time.sleep(0.2)

            except requests.RequestException as error:
                print(
                    f"Failed to scrape {post['url']}: {error}"
                )

            except psycopg2.Error as error:
                print(
                    f"Failed to save {post['url']}: {error}"
                )
                conn.rollback()

    finally:
        conn.close()

    print("Scraping completed.")


if __name__ == "__main__":
    main()