import requests
from bs4 import BeautifulSoup
import psycopg2

BASE_URL = "https://blog.python.org"

# PostgreSQL connection
conn = psycopg2.connect(
    host="psql-db",
    port=5432,
    database="python_blogs",
    user="postgres",
    password="123456"
)

cursor = conn.cursor()

session = requests.Session()

# Get Python Insider homepage
response = session.get(BASE_URL + "/", timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

posts = []
seen_urls = set()

# Find blog post links
for a in soup.find_all("a", href=True):

    href = a["href"]

    if not href.startswith("/2026/"):
        continue

    url = BASE_URL + href

    if url in seen_urls:
        continue

    seen_urls.add(url)

    posts.append({
        "url": url
    })

print("Number of posts found:", len(posts))


# Scrape each blog post
for post in posts:

    response = session.get(post["url"], timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    # Title
    title_tag = soup.find("h1")

    if title_tag:
        title = title_tag.get_text(" ", strip=True)
    else:
        title = "Unknown"

    # Published date
    date_tag = soup.find("time")

    if date_tag:
        published_date = (
            date_tag.get("datetime")
            or date_tag.get_text(" ", strip=True)
        )
    else:
        published_date = None

    # Content
    article = soup.find("article")

    if article:

        for element in article.find_all(
            ["script", "style", "nav"]
        ):
            element.decompose()

        content = article.get_text(
            " ",
            strip=True
        )

    else:
        content = ""

    # Author skipped
    author = None

    # Insert into PostgreSQL
    cursor.execute(
        """
        INSERT INTO blogs
        (title, author, published_date, url, content)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            title,
            author,
            published_date,
            post["url"],
            content
        )
    )

    print("Inserted:", title)
    print("Published:", published_date)
    print("URL:", post["url"])
    print("-" * 70)


# Commit changes
conn.commit()

cursor.close()
conn.close()

print("\nAll blog posts inserted into PostgreSQL.")
