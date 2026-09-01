import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import os
from urllib.parse import urljoin

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', '123456')

def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
            print("✅ Connected to the database successfully!")
            return conn
        except psycopg2.OperationalError:
            print(f"⏳ Database not ready yet. Retrying in 5 seconds... ({i+1}/10)")
            time.sleep(5)
    raise Exception("❌ Could not connect to the database.")

def setup_database(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS python_blogs (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    print("✅ Database table created/verified.")

def scrape_blogs():
    url = 'https://www.scrapethissite.com/'
    print(f"🕷️  Scraping data from {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to download page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    posts = []

    for title_elem in soup.find_all('h3'):
        content_elem = title_elem.find_next('p')

        if title_elem and content_elem:
            title = title_elem.get_text(strip=True)
            content = content_elem.get_text(strip=True, separator='\n')

            link_tag = title_elem.find('a')
            post_url = urljoin(url, link_tag['href']) if link_tag and link_tag.has_attr('href') else url

            posts.append({'title': title, 'content': content, 'url': post_url})

    print(f"📄 Found {len(posts)} blog posts.")
    return posts

def insert_data(conn, posts):
    cur = conn.cursor()
    for post in posts:
        cur.execute('''
            INSERT INTO python_blogs (title, content, url)
            VALUES (%s, %s, %s)
        ''', (post['title'], post['content'], post['url']))
    conn.commit()
    cur.close()
    print("💾 Data successfully inserted into the database!")

if __name__ == '__main__':
    conn = get_db_connection()
    setup_database(conn)
    scraped_posts = scrape_blogs()

    if scraped_posts:
        insert_data(conn, scraped_posts)
    else:
        print("⚠️ No posts found to insert.")

    conn.close()
    print("✅ Process complete!")
