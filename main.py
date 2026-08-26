import time
import requests
from bs4 import BeautifulSoup
import psycopg2

res = requests.get('https://blog.python.org/')
res.raise_for_status()
soup = BeautifulSoup(res.content, 'html5lib')

blogs = []
for article in soup.find_all('article', class_='post-card'):
    title_el = article.find('h3')
    author_el = article.find('a', class_=lambda c: c and 'font-medium' in c)
    time_el = article.find('time')
    title = title_el.text.strip() if title_el else 'N/A'
    author = author_el.text.strip() if author_el else 'N/A'
    time_text = time_el.get_text(strip=True) if time_el else 'N/A'
    blogs.append((title, author, time_text))

conn = None
for attempt in range(5):
    try:
        conn = psycopg2.connect(
            host='psql-db',
            user='postgres',
            password='123456',
            dbname='postgres'
        )
        break
    except psycopg2.OperationalError:
        print(f"Database not ready, retrying in 2s... (attempt {attempt + 1}/5)")
        time.sleep(2)

if conn is None:
    raise Exception("Could not connect to database after 5 attempts")

cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        id SERIAL PRIMARY KEY,
        title TEXT,
        author TEXT,
        published_date TEXT
    )
""")

for title, author, time_text in blogs:
    cur.execute(
        "INSERT INTO blogs (title, author, published_date) VALUES (%s, %s, %s)",
        (title, author, time_text)
    )

conn.commit()
print(f"Inserted {len(blogs)} blog posts into the database.")

cur.close()
conn.close()
