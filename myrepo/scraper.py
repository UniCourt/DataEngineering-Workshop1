import requests
from bs4 import BeautifulSoup
import psycopg2
from urllib.parse import urljoin


BLOG_URL = "https://blog.python.org/blog/"

DB_CONFIG = {
    "host": "psql-db",
    "port": 5432,
    "database": "blogdb",
    "user": "postgres",
    "password": "123456",
}


def scrape_blogs():
    response = requests.get(BLOG_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = []

    for article in soup.find_all("article"):
        title_tag = article.find("h3")

        if not title_tag:
            continue

        link_tag = title_tag.find_parent("a")
        author_tag = article.find("a", href=lambda href: href and "/authors/" in href)
        date_tag = article.find("time")
        description_tag = article.find("p")

        title = title_tag.get_text(strip=True)

        url = ""
        if link_tag and link_tag.get("href"):
            url = urljoin(BLOG_URL, link_tag["href"])

        author = ""
        if author_tag:
            author = author_tag.get_text(strip=True)

        published_date = None
        if date_tag and date_tag.get("datetime"):
            published_date = date_tag["datetime"]

        description = ""
        if description_tag:
            description = description_tag.get_text(" ", strip=True)

        posts.append(
            (title, author, published_date, url, description)
        )

    return posts


def save_to_database(posts):
    import time

    for attempt in range(10):
        try:
            connection = psycopg2.connect(**DB_CONFIG)
            break
        except psycopg2.OperationalError:
            if attempt == 9:
                raise
            print("PostgreSQL is not ready. Retrying...")
            time.sleep(3)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            published_date TIMESTAMP,
            url TEXT UNIQUE,
            description TEXT
        );
    """)

    connection.commit()

    insert_query = """
        INSERT INTO blog_posts
        (title, author, published_date, url, description)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING;
    """

    for post in posts:
        cursor.execute(insert_query, post)

    connection.commit()

    cursor.close()
    connection.close()

if __name__ == "__main__":
    posts = scrape_blogs()

    print(f"Scraped {len(posts)} blog posts.")

    save_to_database(posts)

    print("Blog data saved to PostgreSQL.")
