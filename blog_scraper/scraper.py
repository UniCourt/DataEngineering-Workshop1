import requests
from bs4 import BeautifulSoup
import psycopg2
import time

URL = "https://blog.python.org/"

DB_HOST = "postgres"
DB_NAME = "blogdb"
DB_USER = "postgres"
DB_PASSWORD = "postgres"


def scrape_blogs():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    blogs = []

    for post in soup.find_all("h3", class_="post-title"):
        link = post.find("a")

        if link:
            title = link.get_text(strip=True)
            blog_url = link.get("href")

            blogs.append({
                "title": title,
                "url": blog_url
            })

    return blogs


def connect_database():
    for attempt in range(10):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )

            print("Connected to PostgreSQL")
            return connection

        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(3)

    raise Exception("Could not connect to PostgreSQL")


def save_to_database(blogs):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL
        )
    """)

    for blog in blogs:
        cursor.execute("""
            INSERT INTO blog_posts (title, url)
            VALUES (%s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (blog["title"], blog["url"]))

    connection.commit()

    cursor.close()
    connection.close()

    print("Blog data saved successfully")


if __name__ == "__main__":
    print("Scraping Python Blog...")

    blogs = scrape_blogs()

    print("Number of blogs found:", len(blogs))

    for blog in blogs:
        print(blog)

    save_to_database(blogs)
