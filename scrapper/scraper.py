import requests
from bs4 import BeautifulSoup
from database import create_table, insert_blog

BASE_URL = "https://blog.python.org"

create_table()

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

headings = soup.find_all("h3")

all_posts = []

for heading in headings:
    link = heading.find_parent("a")

    if not link or not link.get("href"):
        continue

    title = heading.get_text(strip=True)
    post_url = BASE_URL + link.get("href")

    post_response = requests.get(post_url)
    post_soup = BeautifulSoup(
        post_response.text,
        "html.parser"
    )

    article = post_soup.find("article")

    if not article:
        continue

    header = article.find("header")
    author_link = header.find("a")

    author = (
        author_link.get_text(strip=True)
        if author_link
        else "Unknown"
    )

    time_tag = article.find("time")

    date = (
        time_tag.get_text(strip=True)
        if time_tag
        else "Unknown"
    )

    content_div = article.find(
        "div",
        class_="animate-fade-up stagger-1"
    )

    content = (
        content_div.get_text(" ", strip=True)
        if content_div
        else ""
    )

    post_data = {
        "title": title,
        "author": author,
        "date": date,
        "content": content,
        "url": post_url
    }

    all_posts.append(post_data)
    insert_blog(post_data)

    print(f"Saved: {title}")

print(f"\nTotal posts scraped: {len(all_posts)}")
