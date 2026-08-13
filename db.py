import os
import time
import psycopg2
from psycopg2.extras import execute_values

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "workshop_db")
DB_USER = os.getenv("DB_USER", "workshop_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "workshop_pass")


def get_connection(retries=10, delay=3):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                user=DB_USER, password=DB_PASSWORD,
            )
            print(f"[db] Connected to Postgres on attempt {attempt}")
            return conn
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"[db] Attempt {attempt}/{retries} failed: {e}")
            time.sleep(delay)
    raise last_error


def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS blog_posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                url VARCHAR(500) NOT NULL UNIQUE,
                author VARCHAR(255),
                author_url VARCHAR(500),
                published_date DATE,
                summary TEXT,
                tags TEXT[],
                scraped_at TIMESTAMP DEFAULT NOW()
            );
        """)
    conn.commit()
    print("[db] Table 'blog_posts' is ready")


def insert_posts(conn, posts):
    if not posts:
        print("[db] No posts to insert")
        return

    rows = [
        (
            p["title"], p["url"], p["author"], p["author_url"],
            p["published_date"], p["summary"], p["tags"],
        )
        for p in posts
    ]

    query = """
        INSERT INTO blog_posts (title, url, author, author_url, published_date, summary, tags)
        VALUES %s
        ON CONFLICT (url) DO UPDATE
        SET title = EXCLUDED.title,
            author = EXCLUDED.author,
            author_url = EXCLUDED.author_url,
            published_date = EXCLUDED.published_date,
            summary = EXCLUDED.summary,
            tags = EXCLUDED.tags,
            scraped_at = NOW();
    """
    with conn.cursor() as cur:
        execute_values(cur, query, rows)
    conn.commit()
    print(f"[db] Inserted/updated {len(rows)} rows")