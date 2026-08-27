import os
import time

import psycopg2
import requests
from bs4 import BeautifulSoup

URL = 'https://blog.python.org/'

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123456')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')

RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '5'))
RETRY_DELAY = float(os.getenv('RETRY_DELAY', '2'))


def fetch_blogs():
    res = requests.get(URL, timeout=30)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'html5lib')

    blogs = []
    for article in soup.find_all('article', class_='post-card'):
        title_el = article.find('h3')
        author_el = article.find(class_=lambda c: c and 'font-medium' in c)
        time_el = article.find('time')
        title = title_el.text.strip() if title_el else 'N/A'
        author = author_el.text.strip() if author_el else 'N/A'
        time_text = time_el.get_text(strip=True) if time_el else 'N/A'
        blogs.append((title, author, time_text))
    return blogs


def connect_with_retry():
    last_error = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname=DB_NAME,
            )
        except psycopg2.OperationalError as exc:
            last_error = exc
            print(
                f"Database not ready, retrying in {RETRY_DELAY}s... "
                f"(attempt {attempt + 1}/{RETRY_ATTEMPTS})"
            )
            time.sleep(RETRY_DELAY)
    raise ConnectionError(
        f"Could not connect to database after {RETRY_ATTEMPTS} attempts: {last_error}"
    ) from last_error


def main():
    blogs = fetch_blogs()
    if not blogs:
        print("No blog posts found on the page.")
        return

    conn = connect_with_retry()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS blogs (
                    id SERIAL PRIMARY KEY,
                    title TEXT UNIQUE,
                    author TEXT,
                    published_date TEXT
                )
            """)

            for title, author, time_text in blogs:
                cur.execute(
                    "INSERT INTO blogs (title, author, published_date) "
                    "VALUES (%s, %s, %s) ON CONFLICT (title) DO NOTHING",
                    (title, author, time_text),
                )

        conn.commit()
        print(f"Inserted {len(blogs)} blog posts into the database.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
