import requests
from bs4 import BeautifulSoup

url = "https://blog.python.org/blog/"

res = requests.get(url)

soup = BeautifulSoup(res.content, "html.parser")

# Find each blog post
posts = soup.find_all("article")

for post in posts:
    # Title
    title = post.find("h3")

    # Date
    date = post.find("time")

    # Author
    author = post.find(class_="author")

    print("Title:", title.get_text(strip=True) if title else "N/A")
    print("Author:", author.get_text(strip=True) if author else "N/A")
    print("Date:", date.get_text(strip=True) if date else "N/A")
    print("-" * 60)
