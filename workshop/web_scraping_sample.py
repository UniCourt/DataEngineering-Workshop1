import requests
from bs4 import BeautifulSoup
import os
import psycopg2

# PostgreSQL connection
# Host uses the Docker Compose service name, not localhost
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "psql-db"),
    database=os.environ.get("DB_NAME", "postgres"),
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", "123456"),
    port=int(os.environ.get("DB_PORT", 5432))
)

cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS downloaded_pdfs (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255),
        url TEXT,
        file_size BIGINT
    )
""")
conn.commit()

n = int(input("How many PDFs to download? "))

url = "https://sample-files.com/pdf/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")

os.makedirs("pdfs", exist_ok=True)

count = 0

for a in soup.find_all("a", href=True):
    if ".pdf" in a["href"].lower():

        link = a["href"]

        if not link.startswith("http"):
            link = "https://sample-files.com" + link

        name = link.split("/")[-1]

        data = requests.get(link).content

        filepath = "pdfs/" + name

        with open(filepath, "wb") as f:
            f.write(data)

        file_size = os.path.getsize(filepath)

        # Store file information in PostgreSQL
        cur.execute("""
            INSERT INTO downloaded_pdfs (filename, url, file_size)
            VALUES (%s, %s, %s)
        """, (name, link, file_size))

        conn.commit()

        print("Downloaded:", name)
        count += 1

        if count == n:
            break

cur.close()
conn.close()

print(f"\nDownloaded {count} PDFs.")
