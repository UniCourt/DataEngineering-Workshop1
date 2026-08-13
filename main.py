import os
from scraper import scrape
from db import get_connection, create_table, insert_posts


def main():
    # Set MAX_PAGES env var to limit pages while testing (e.g. MAX_PAGES=2).
    # Leave unset / 0 to scrape all ~17 pages (~325 posts).
    max_pages_env = os.getenv("MAX_PAGES", "0")
    max_pages = int(max_pages_env) if max_pages_env.isdigit() and int(max_pages_env) > 0 else None

    posts = scrape(max_pages=max_pages)

    conn = get_connection()
    try:
        create_table(conn)
        insert_posts(conn, posts)
    finally:
        conn.close()

    print("[main] Done.")


if __name__ == "__main__":
    main()