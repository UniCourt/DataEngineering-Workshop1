import requests
from bs4 import BeautifulSoup

url = "https://blog.python.org/"

response = requests.get(url, timeout=10)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("article")

for article in articles:

    # Title
    title_tag = article.find(["h1", "h2", "h3"])

    # Author
    author_tag = article.find(
        class_=lambda x: x and "author" in " ".join(x).lower()
    )

    # Date
    date_tag = article.find("time")

    # Paragraphs
    paragraphs = article.find_all("p")

    print()
    print("Title:", title_tag.get_text(strip=True) if title_tag else "N/A")

    print(
        "Author:",
        author_tag.get_text(" ", strip=True)
        if author_tag
        else "N/A"
    )

    print(
        "Date:",
        date_tag.get_text(strip=True)
        if date_tag
        else "N/A"
    )

    print("Paragraphs:")

    for paragraph in paragraphs:
        text = paragraph.get_text(" ", strip=True)

        if text:
            print(text)

    print("-" * 80)
