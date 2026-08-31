import requests
from bs4 import BeautifulSoup
import psycopg2

URL = "https://blog.python.org/"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

blogs = []

for article in soup.find_all("h3"):
    title = article.get_text(strip=True)

    parent_link = article.find_parent("a")

    if parent_link:
        url = parent_link.get("href", "")
        blogs.append((title, url))

print(f"Found {len(blogs)} blogs")

conn = psycopg2.connect(
    host="psql-db",
    port=5432,
    database="LipSumGenerator",
    user="postgres",
    password="admin"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS python_blogs (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT
    )
""")

for title, url in blogs:
    cursor.execute(
        "INSERT INTO python_blogs (title, url) VALUES (%s, %s)",
        (title, url)
    )

conn.commit()

cursor.close()
conn.close()

print("Blog data saved to PostgreSQL successfully!")