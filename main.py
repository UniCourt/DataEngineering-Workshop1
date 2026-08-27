from dotenv import load_dotenv

import db
import web_scraping

load_dotenv()


def main():
    conn = db.get_connection()
    try:
        db.init_db(conn)
        url = "/blog"
        page = 0
        while url:
            page += 1
            print(f"--- Page {page}: {web_scraping.BASE}{url} ---")
            items, url = web_scraping.fetch_page(url)
            print(f"Scraped {len(items)} posts")
            if items:
                db.insert_posts(conn, items)
                print(f"Inserted {len(items)} posts")
        print("Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
