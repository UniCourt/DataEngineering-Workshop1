import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import os
import re

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "blogdb")
DB_USER = os.getenv("DB_USER", "bloguser")
DB_PASS = os.getenv("DB_PASS", "blogpass")

URL = "https://blog.python.org/"
POST_LINK_PATTERN = re.compile(r"^/\d{4}/\d{2}/")


def get_connection():
    for i in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
            )
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(3)
    raise Exception("Could not connect to database")


def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT,
            link TEXT UNIQUE,
            summary TEXT
        )
    """)
    conn.commit()
    cur.close()


def scrape_and_save(conn):
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")

    cur = conn.cursor()
    count = 0
    seen_links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not POST_LINK_PATTERN.match(href):
            continue

        title = a.get_text(strip=True)
        if not title or href in seen_links:
            continue
        seen_links.add(href)

        link = "https://blog.python.org" + href

        parent = a.find_parent(["article", "li", "section", "div"]) or a.parent
        summary = parent.get_text(" ", strip=True)[:300]

        cur.execute(
            "INSERT INTO posts (title, link, summary) VALUES (%s, %s, %s) ON CONFLICT (link) DO NOTHING",
            (title, link, summary),
        )
        count += 1

    conn.commit()
    cur.close()
    print(f"Saved {count} posts to the database.")


if __name__ == "__main__":
    conn = get_connection()
    create_table(conn)
    scrape_and_save(conn)
    conn.close()



#docker compose up scraper --build