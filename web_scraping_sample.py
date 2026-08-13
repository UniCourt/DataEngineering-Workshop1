import requests
from bs4 import BeautifulSoup

url = "https://blog.python.org/"

response = requests.get(url)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

posts = soup.find_all("article")

for post in posts:
    title = post.find(["h1", "h2", "h3"])

    if title:
        print("\nTitle:", title.get_text(" ", strip=True))

    author = post.find(class_=lambda c: c and "author" in str(c).lower())

    if author:
        print("Author:", author.get_text(" ", strip=True))

    date = post.find("time")

    if date:
        print("Date:", date.get_text(" ", strip=True))

    print("Paragraphs:")

    for p in post.find_all("p"):
        text = p.get_text(" ", strip=True)
        if text:
            print(text)

    print("-" * 80)
