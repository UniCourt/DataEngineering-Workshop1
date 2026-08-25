import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import psycopg2

url = "https://blog.python.org/"

response = requests.get(url)

print("Status:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="postgres",
    port=5432,
    database="workshop_db",
    user="workshop",
    password="workshop"
)

cursor = connection.cursor()

print("\nBLOG POSTS:")

posts = soup.find_all("a", class_="group block")

for post in posts:

    post_url = urljoin(url, post.get("href"))

    title = post.find(["h1", "h2", "h3"])
    title = title.get_text(" ", strip=True) if title else ""

    author = post.find("span", class_="font-medium")
    author = author.get_text(" ", strip=True) if author else ""

    date = post.find("time")
    date = date.get_text(" ", strip=True) if date else ""

    summary = post.find("p")
    summary = summary.get_text(" ", strip=True) if summary else ""

    print("\n------------------------------")
    print("Title:", title)
    print("Author:", author)
    print("Date:", date)
    print("URL:", post_url)
    print("Summary:", summary)

    # Insert into PostgreSQL
    cursor.execute(
        """
        INSERT INTO blogs (title, author, date, url, summary)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (url) DO NOTHING
        """,
        (title, author, date, post_url, summary)
    )

connection.commit()

cursor.close()
connection.close()

print("\nData saved to PostgreSQL.")
