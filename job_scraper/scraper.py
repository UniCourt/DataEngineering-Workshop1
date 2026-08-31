import csv
import psycopg2
import requests
from bs4 import BeautifulSoup


# --------------------------------------------------
# 1. Website URL
# --------------------------------------------------

URL = "https://quotes.toscrape.com/"


# --------------------------------------------------
# 2. Scrape website
# --------------------------------------------------

response = requests.get(URL, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

scraped_data = []


# --------------------------------------------------
# 3. Extract quote and author
# --------------------------------------------------

for quote in quotes:
    text = quote.find("span", class_="text").get_text(strip=True)
    author = quote.find("small", class_="author").get_text(strip=True)

    data = {
        "quote": text,
        "author": author
    }

    scraped_data.append(data)


# --------------------------------------------------
# 4. Display scraped data
# --------------------------------------------------

print(f"Total records scraped: {len(scraped_data)}")

for item in scraped_data:
    print(item)


# --------------------------------------------------
# 5. Connect to PostgreSQL
# --------------------------------------------------

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    database="scraper_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()


# --------------------------------------------------
# 6. Create table if it does not exist
# --------------------------------------------------

cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        id SERIAL PRIMARY KEY,
        quote TEXT NOT NULL,
        author TEXT NOT NULL
    );
""")


# --------------------------------------------------
# 7. Insert scraped data into PostgreSQL
# --------------------------------------------------

for item in scraped_data:

    cursor.execute(
        """
        INSERT INTO quotes (quote, author)
        VALUES (%s, %s)
        """,
        (item["quote"], item["author"])
    )


# --------------------------------------------------
# 8. Save changes
# --------------------------------------------------

conn.commit()

print("Data saved to PostgreSQL successfully!")


# --------------------------------------------------
# 9. Close PostgreSQL connection
# --------------------------------------------------

cursor.close()
conn.close()

print("Database connection closed.")


# --------------------------------------------------
# 10. Export data to CSV
# --------------------------------------------------

with open(
    "quotes.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=["quote", "author"]
    )

    writer.writeheader()
    writer.writerows(scraped_data)


print("Data exported to quotes.csv successfully!")
