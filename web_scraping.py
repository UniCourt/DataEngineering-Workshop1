import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_blog_posts(base_url="https://blog.python.org/"):
    all_posts = []

    try:
        while base_url:
            response = requests.get(base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            posts = soup.find_all('div', class_='date-outer')

            for post in posts:
                title_tag = post.find('h3', class_='post-title')
                date_tag = post.find('h2', class_='date-header')
                content_tag = post.find('div', class_='post-body')
                author_tag = post.find('span', class_='fn')

                if title_tag and date_tag and content_tag:
                    title = title_tag.get_text(strip=True)
                    date = date_tag.get_text(strip=True)
                    content = content_tag.get_text(strip=True)
                else:
                    logging.warning("Skipping incomplete post")
                    continue

                author = author_tag.get_text(strip=True) if author_tag else 'Unknown'
                all_posts.append({
                    'title': title,
                    'date': date,
                    'author': author,
                    'content': content
                })

            older_posts_link = soup.find('a', {'class': 'blog-pager-older-link'})
            base_url = older_posts_link['href'] if older_posts_link else None

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve page {base_url}. Error: {str(e)}")

    return all_posts

def save_posts_to_db(posts):
    # PostgreSQL connection details
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS scrapped_contents (
                id SERIAL PRIMARY KEY,
                date TEXT,
                title TEXT,
                author TEXT,
                content TEXT
            );
            """)

            for post in posts:
                cur.execute(
                    "INSERT INTO scrapped_contents  (date, title, author, content) VALUES (%s, %s, %s, %s)",
                    (post['date'], post['title'], post['author'], post['content'])
                )

        conn.commit()
        logging.info("Data has been successfully written to the PostgreSQL database")

    except psycopg2.Error as e:
        logging.error(f"Error inserting data into PostgreSQL: {e}")

    finally:
        if conn:
            conn.close()

def main():
    blog_posts = fetch_blog_posts()
    if blog_posts:
        save_posts_to_db(blog_posts)

if __name__ == "__main__":
    main()
