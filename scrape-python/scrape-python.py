import requests
from bs4 import BeautifulSoup
import psycopg2


# -----------------------------------------
# 1. SCRAPE WEBSITE
# -----------------------------------------

url = "https://blog.python.org/"

print("Fetching:", url)

response = requests.get(url, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html5lib")


# -----------------------------------------
# 2. EXTRACT BLOG DATA
# -----------------------------------------

blogs = []

for row in soup.find_all("article"):

    title = row.h3.get_text(strip=True)
    date = row.time.get_text(strip=True)

    author_tag = row.find(
        "span",
        class_="font-medium text-zinc-500 dark:text-zinc-400"
    )

    author = author_tag.get_text(strip=True) if author_tag else "Unknown"
   
    blogs.append({
        "title": title,
        "author": author,
        "date": date
    })

# -----------------------------------------
# 3. DISPLAY SCRAPED DATA
# -----------------------------------------

print("\n========== SCRAPED DATA ==========\n")

for blog in blogs:

    print("Title :", blog["title"])
    print("Author:", blog["author"])
    print("Date  :", blog["date"])
    print("----------------------------------")


print(f"\nTotal blogs scraped: {len(blogs)}")


# -----------------------------------------
# 4. CONNECT TO POSTGRESQL
# -----------------------------------------

print("\nConnecting to PostgreSQL...")

conn = psycopg2.connect(
    host="psql-db",
    port="5432",
    database="postgres",
    user="postgres",
    password="123456"
)

cursor = conn.cursor()

print("Connected to PostgreSQL")


# -----------------------------------------
# 5. CREATE TABLE
# -----------------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS blogs (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT,
        date TEXT
    )
""")

conn.commit()


# -----------------------------------------
# 6. INSERT DATA
# -----------------------------------------

for blog in blogs:

    cursor.execute("""
        INSERT INTO blogs (title, author, date)
        VALUES (%s, %s, %s)
    """, (
        blog["title"],
        blog["author"],
        blog["date"]
    ))


conn.commit()

print(f"{len(blogs)} blogs inserted into PostgreSQL")


# -----------------------------------------
# 7. CLOSE CONNECTION
# -----------------------------------------

cursor.close()
conn.close()

print("Database connection closed")
