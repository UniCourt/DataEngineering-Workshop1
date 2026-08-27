import time
import requests
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://blog.python.org/"

# PostgreSQL connection details
DB_HOST = "postgres"
DB_NAME = "unicourt_db"
DB_USER = "unicourt_user"
DB_PASSWORD = "unicourt_password"


def get_database_connection():
    while True:
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Connected to PostgreSQL.")
            return connection
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)


def scrape_blogs():
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    blogs = []

    for post in soup.find_all("article"):
        title_tag = post.find("h3")
        link_tag = post.find("a")
        author_tag = post.find("span")
        date_tag = post.find("time")

        if title_tag and link_tag:
            title = title_tag.get_text(strip=True)
            url = urljoin(BASE_URL, link_tag.get("href"))
            author = author_tag.get_text(strip=True) if author_tag else "Unknown"
            published_date = (
                date_tag.get_text(strip=True)
                if date_tag
                else "Unknown"
            )

            blogs.append((title, author, published_date, url))

    return blogs


def save_to_database(connection, blogs):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blog_posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            published_date TEXT,
            url TEXT UNIQUE
        )
    """)

    for title, author, published_date, url in blogs:
        cursor.execute("""
            INSERT INTO blog_posts
                (title, author, published_date, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
        """, (title, author, published_date, url))

    connection.commit()
    cursor.close()

    print(f"Saved {len(blogs)} blog posts to PostgreSQL.")


def main():
    blogs = scrape_blogs()

    print(f"Scraped {len(blogs)} blog posts.")

    connection = get_database_connection()

    save_to_database(connection, blogs)

    connection.close()
    print("Database connection closed.")


if __name__ == "__main__":
    main()
