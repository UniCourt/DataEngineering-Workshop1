import requests
import psycopg2
from bs4 import BeautifulSoup


conn = psycopg2.connect(
    host="psql-db",
    database="workshop",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

url = "https://blog.python.org/"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

posts = soup.find_all("article")

for post in posts:
    title = post.h3.text.strip()
    link = "https://blog.python.org" + post.a["href"]
    author = post.find("span").text.strip()
    date = post.time.text.strip()

    print("Title:", title)
    print("URL:", link)
    print("Author:", author)
    print("Date:", date)
    print()

   
    cursor.execute(
        "SELECT id FROM blogs WHERE url = %s",
        (link,)
    )

    existing_blog = cursor.fetchone()

    if existing_blog is None:
        cursor.execute(
            """
            INSERT INTO blogs (title, url, author, published_date)
            VALUES (%s, %s, %s, %s)
            """,
            (title, link, author, date)
        )

conn.commit()

cursor.close()
conn.close()

print("Scraping and database insertion completed.")