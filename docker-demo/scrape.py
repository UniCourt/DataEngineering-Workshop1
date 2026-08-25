import requests
from bs4 import BeautifulSoup
import psycopg2
import time

time.sleep(10)

conn = psycopg2.connect(
    host="db",
    database="blogdb",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS blogs(
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE
)
""")

conn.commit()

print("Connected to PostgreSQL")

url = "https://python.org/blogs/"
response = requests.get(url)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# Latest news links on the page
posts = soup.select(".list-recent-posts li a")

count = 0

for post in posts:
    title = post.get_text(strip=True)
    link = post.get("href")

    if not link.startswith("http"):
        link = "https://python.org" + link

    cur.execute("""
        INSERT INTO blogs(title, link)
        VALUES(%s,%s)
        ON CONFLICT(link) DO NOTHING
    """, (title, link))

    count += 1

conn.commit()

print(f"{count} blog posts saved successfully!")

cur.close()
conn.close()
