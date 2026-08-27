import requests
from bs4 import BeautifulSoup
import psycopg2

conn = psycopg2.connect(
    host="db",
    database="blogdb",
    user="postgres",
    password="password",
    port=5432
)

cursor = conn.cursor()

print("Connected to PostgreSQL!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogs (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
)
""")

url = "https://blog.python.org/blog/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

posts = soup.select("article")

print("Posts found:", len(posts))

for post in posts:
    title = post.get_text(" ", strip=True)

    cursor.execute(
        "INSERT INTO blogs (title) VALUES (%s)",
        (title,)
    )

conn.commit()

cursor.close()
conn.close()

print("Data saved to PostgreSQL!")
