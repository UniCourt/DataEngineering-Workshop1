import requests
from bs4 import BeautifulSoup
import psycopg2


# PostgreSQL connection
conn = psycopg2.connect(
    host="postgres_service",
    database="postgres",
    user="postgres",
    password="admin"
)

cursor = conn.cursor()


# Python Blog URL
url = "https://blog.python.org/"

response = requests.get(url)

if response.status_code == 200:
    print("Website scraped successfully!")
else:
    print("Failed to access website. Status:", response.status_code)
    exit()


soup = BeautifulSoup(response.content, "html5lib")


# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        title TEXT,
        date TEXT
    )
""")

conn.commit()


# Find blog posts
posts = soup.find_all("article")


for post in posts:
    title_tag = post.find(["h2", "h3"])

    if title_tag:
        title = title_tag.get_text(strip=True)

        date_tag = post.find("time")

        if date_tag:
            date = date_tag.get_text(strip=True)
        else:
            date = "N/A"

        print("Title:", title)
        print("Date:", date)
        print("-" * 60)

        cursor.execute(
            """
            INSERT INTO blog_posts (title, date)
            VALUES (%s, %s)
            """,
            (title, date)
        )


conn.commit()

print("Blog data successfully stored in PostgreSQL.")


cursor.close()
conn.close()
