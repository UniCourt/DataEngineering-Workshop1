import requests

import os
from bs4 import BeautifulSoup
import psycopg

RSS_URL = "https://blog.python.org/rss.xml"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("Fetching Python Blog RSS feed...")

response = requests.get(
    RSS_URL,
    headers=headers,
    timeout=15
)

print("Status:", response.status_code)

if response.status_code != 200:
    print("Failed to fetch Python Blog RSS feed")
    exit(1)

soup = BeautifulSoup(
    response.content,
    "xml"
)

blogs = []

for item in soup.find_all("item"):

    title_tag = item.find("title")
    link_tag = item.find("link")

    if not title_tag or not link_tag:
        continue

    title = title_tag.get_text(strip=True)
    url = link_tag.get_text(strip=True)

    blogs.append({
        "title": title,
        "url": url
    })

print("\nTotal blogs found:", len(blogs))

for blog in blogs:
    print("\n-------------------")
    print("Title:", blog["title"])
    print("URL:", blog["url"])


print("\nConnecting to PostgreSQL...")

conn = psycopg.connect(
    host="psql-db",
    port=5432,
    dbname="demo",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT UNIQUE NOT NULL
    )
""")

for blog in blogs:

    cursor.execute("""
        INSERT INTO blog_posts
        (title, url)
        VALUES (%s, %s)
        ON CONFLICT (url) DO NOTHING
    """, (
        blog["title"],
        blog["url"]
    ))

conn.commit()

cursor.execute(
    "SELECT COUNT(*) FROM blog_posts"
)

count = cursor.fetchone()[0]

print("\nBlogs saved to PostgreSQL")
print("Total blogs in PostgreSQL:", count)

cursor.close()
conn.close()

print("\nScraper completed successfully.")
