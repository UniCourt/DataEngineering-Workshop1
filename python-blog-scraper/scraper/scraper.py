import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from database import insert_posts

from cleaner import (
    clean_text, 
    parse_date, 
    is_valid_post,
    remove_duplicates,
    get_scraped_at
)


URL = "https://blog.python.org/"

HEADERS = {
    "User-Agent": "curl/8.5.0"
}


def scrape_posts():

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    articles = soup.select("article.post-card")

    print(f"Found {len(articles)} articles")

    posts = []

    for article in articles:

        title_element = article.select_one("h3")
        date_element = article.select_one("time")
        summary_element = article.select_one("p")

        if not title_element:
            continue

        title = title_element.get_text(
            " ",
            strip=True
        )

        published_date = (
            date_element.get("datetime")
            if date_element
            else None
        )

        author_element = (
            date_element.parent.select_one("span")
            if date_element
            else None
        )

        author = (
            author_element.get_text(
                strip=True
            )
            if author_element
            else "Unknown"
        )

        summary = (
            summary_element.get_text(
                " ",
                strip=True
            )
            if summary_element
            else ""
        )

        link_element = title_element.find_parent("a")

        if not link_element:
            continue

        url = urljoin(
            URL,
            link_element.get("href")
        )

        post = {
            "title": clean_text(title),
            "author": clean_text(author),
            "published_date": parse_date(published_date),
            "summary": clean_text(summary),
            "url": clean_text(url),
	    "scraped_at": get_scraped_at()
        }

        if is_valid_post(post):
            posts.append(post)
    unique_posts = remove_duplicates(posts)
    print(
        f"After deduplication: {len(unique_posts)} posts"
    )
    return unique_posts


if __name__ == "__main__":

    posts = scrape_posts()

    print("\n========== BLOG POSTS ==========\n")

    for post in posts:
        print(post)
        print("-" * 80)

    inserted_count = insert_posts(posts)

    print(
        f"\nInserted {inserted_count} new posts into PostgreSQL."
    )
