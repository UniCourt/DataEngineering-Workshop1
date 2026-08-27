import os
import time
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET
 
import psycopg2
import requests
 
RSS_URL = "https://blog.python.org/rss.xml"
NAMESPACES = {"dc": "http://purl.org/dc/elements/1.1/"}
 
 
def get_db_connection():
    """Retry connecting until the DB container is ready."""
    while True:
        try:
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "psql-db"),
                dbname=os.getenv("DB_NAME", "blogs_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "123456"),
                port=os.getenv("DB_PORT", "5432"),
            )
            return conn
        except psycopg2.OperationalError:
            print("Database not ready, retrying in 2 seconds...")
            time.sleep(2)
 
 
def create_table(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS blogs (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                author TEXT,
                published_at TIMESTAMPTZ,
                description TEXT
            );
            """
        )
    conn.commit()
 
 
def scrape_blogs():
    """Fetch and parse the Python Insider RSS feed."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; PythonBlogScraper/1.0)"}
 
    print(f"Fetching {RSS_URL} ...")
    response = requests.get(RSS_URL, headers=headers, timeout=15)
    response.raise_for_status()
    print(f"HTTP status: {response.status_code}")
 
    root = ET.fromstring(response.content)
 
    blogs = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        description = (item.findtext("description") or "").strip()
        author = (item.findtext("dc:creator", namespaces=NAMESPACES) or "").strip()
        pub_date_raw = (item.findtext("pubDate") or "").strip()
 
        published_at = None
        if pub_date_raw:
            try:
                published_at = parsedate_to_datetime(pub_date_raw)
            except (TypeError, ValueError):
                published_at = None
 
        if title and link:
            blogs.append((title, link, author, published_at, description))
 
    return blogs
 
 
def save_to_db(conn, blogs):
    with conn.cursor() as cur:
        for title, link, author, published_at, description in blogs:
            cur.execute(
                """
                INSERT INTO blogs (title, url, author, published_at, description)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    title = EXCLUDED.title,
                    author = EXCLUDED.author,
                    published_at = EXCLUDED.published_at,
                    description = EXCLUDED.description;
                """,
                (title, link, author, published_at, description),
            )
    conn.commit()
 
 
if __name__ == "__main__":
    print("Connecting to database...")
    connection = get_db_connection()
    create_table(connection)
 
    print("Scraping Python Insider blog (via RSS)...")
    blog_data = scrape_blogs()
 
    print(f"Saving {len(blog_data)} records to database...")
    save_to_db(connection, blog_data)
 
    connection.close()
    print("Done!")
