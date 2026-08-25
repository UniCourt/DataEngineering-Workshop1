import requests
from bs4 import BeautifulSoup
import psycopg2
from urllib.parse import urljoin


URL = "https://blog.python.org/blog/"


# Connect to PostgreSQL
connection = psycopg2.connect(
    host="psql-db-homework",
    port=5432,
    database="demo",
    user="postgres",
    password="123456"
)

cursor = connection.cursor()


# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        id SERIAL PRIMARY KEY,
        title TEXT,
        url TEXT UNIQUE,
        description TEXT
    )
""")

connection.commit()


# Get blog listing page
response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


count = 0

# Find every link on the page
for link in soup.find_all("a", href=True):

    href = link["href"]

    # Actual blog posts have URLs like /2026/08/...
    if not href.startswith("/2026/"):
        continue

    title = link.get_text(" ", strip=True)

    if not title:
        continue

    blog_url = urljoin(URL, href)

    # Visit the individual blog page
    blog_response = requests.get(
        blog_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    if blog_response.status_code != 200:
        print("Could not access:", blog_url)
        continue

    blog_soup = BeautifulSoup(blog_response.text, "html.parser")

    # Get the main article content
    article = blog_soup.find("article")

    if article:
        description = article.get_text(" ", strip=True)
    else:
        # Fallback: get paragraphs from the page
        paragraphs = blog_soup.find_all("p")
        description = " ".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

    # Store data in PostgreSQL
    cursor.execute("""
        INSERT INTO blogs (title, url, description)
        VALUES (%s, %s, %s)
        ON CONFLICT (url)
        DO UPDATE SET
            title = EXCLUDED.title,
            description = EXCLUDED.description
    """, (
        title,
        blog_url,
        description
    ))

    count += 1

    print("Title:", title)
    print("URL:", blog_url)
    print("Description:", description[:200], "...")
    print("-" * 70)

    if count >= 10:
        break


connection.commit()

cursor.close()
connection.close()

print()
print("Total blogs stored:", count)
print("Scraping completed successfully!")
