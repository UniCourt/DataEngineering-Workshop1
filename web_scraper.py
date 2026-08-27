import requests
from bs4 import BeautifulSoup
import psycopg2

# Connect to PostgreSQL
connection = psycopg2.connect(
    host="postgres",
    port=5432,
    database="blogs",
    user="postgres",
    password="postgres"
)

cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS blog_posts (
        id SERIAL PRIMARY KEY,
        heading TEXT,
        author TEXT,
        date TEXT
    )
""")

connection.commit()

# Scrape Python Blogs
blogs = []

for page in range(1, 18):

    if page == 1:
        url = "https://blog.python.org/blog/"
    else:
        url = f"https://blog.python.org/blog/{page}/"

    print("Scraping page", page)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.RequestException as e:
        print("Could not access page:", e)
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    for post in soup.find_all("article"):

        heading = post.find("h3")
        date = post.find("time")

        if heading and date:

            author = date.find_previous("a")

            heading_text = heading.get_text(strip=True)
            author_text = author.get_text(strip=True) if author else ""
            date_text = date.get_text(strip=True)

            blogs.append((heading_text, author_text, date_text))


# Insert blogs into PostgreSQL
for blog in blogs:

    cursor.execute(
        """
        INSERT INTO blog_posts (heading, author, date)
        VALUES (%s, %s, %s)
	ON CONFLICT (heading) DO NOTHING
        """,
        blog
    )

connection.commit()

print("Total blogs inserted:", len(blogs))

cursor.close()
connection.close()
