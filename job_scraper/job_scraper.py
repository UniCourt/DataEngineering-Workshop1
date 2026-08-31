import requests
from bs4 import BeautifulSoup
import csv

URL = "https://books.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select("article.product_pod"):
    title = book.h3.a["title"]
    price = book.select_one(".price_color").text.strip()
    availability = book.select_one(".availability").text.strip()

    books.append({
        "title": title,
        "price": price,
        "availability": availability
    })

with open("books.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["title", "price", "availability"]
    )

    writer.writeheader()
    writer.writerows(books)

print(f"Scraped {len(books)} books successfully!")
print("Saved data to books.csv")
