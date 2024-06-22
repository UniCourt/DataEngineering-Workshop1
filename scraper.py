import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import time

def scrape_blog():
    base_url = "https://blog.python.org/"
    current_url = base_url
    all_posts = []

    while True:
        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break

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
                print("Skipping incomplete post")
                continue
            author = author_tag.get_text(strip=True) if author_tag else 'Unknown'
            all_posts.append({
                'title': title,
                'date': date,
                'author': author,
                'content': content
            })
        older_posts_link = soup.find('a', {'class': 'blog-pager-older-link'})
        if older_posts_link:
            current_url = older_posts_link['href']
        else:
            break
    return all_posts

def save_to_postgres(blog_posts):
    # PostgreSQL connection details
    DB_NAME = os.getenv("DB_NAME", "blogdata")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_PORT = os.getenv("DB_PORT", "5432")

    time.sleep(10)  

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

   
    cur = conn.cursor()

   
    cur.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        date TEXT,
        title TEXT,
        author TEXT,
        content TEXT
    );
    """)


    for post in blog_posts:
        cur.execute(
            "INSERT INTO blog_posts (date, title, author, content) VALUES (%s, %s, %s, %s)",
            (post['date'], post['title'], post['author'], post['content'])
        )


    conn.commit()
    cur.close()
    conn.close()
    print("Data has been successfully written to the PostgreSQL database")

def main():
    blog_posts = scrape_blog()
    save_to_postgres(blog_posts)

if __name__ == "__main__":
    main()
