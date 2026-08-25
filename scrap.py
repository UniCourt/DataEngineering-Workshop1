import os
import time
import requests as req
from bs4 import BeautifulSoup
import psycopg2

try:
    from rich.console import Console
    from rich.text import Text
    from rich.rule import Rule
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_banner():
    """Print minimalist header following TUI design guidelines."""
    if RICH_AVAILABLE:
        print()
        console.print("PYTHON BLOG PIPELINE", style="bold #38bdf8")
        console.print("PostgreSQL Data Engine • Workshop 1", style="dim #8b949e")
        print()
    else:
        print("\nPYTHON BLOG PIPELINE")
        print("PostgreSQL Data Engine - Workshop 1\n")


def scrape_python_blogs():
    """Scrape Python blog posts from https://blog.python.org/."""
    url = "https://blog.python.org/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    
    if RICH_AVAILABLE:
        console.print(f"Connecting to URL: [dim #58a6ff]{url}[/dim #58a6ff]", style="dim #8b949e")
    else:
        print(f"Fetching data from: {url}")

    res = req.get(url, headers=headers, timeout=15)
    doc = BeautifulSoup(res.text, "html.parser")
    
    posts = []

    # 1. User provided selector pattern: div with class "min-w-0 flex-1"
    data = doc.find_all("div", attrs={"class": "min-w-0 flex-1"})
    for row in data:
        title = row.find("h3") or row.find("h2") or row.find("h1")
        author = row.find(
            "a",
            attrs={
                "class": (
                    "font-medium text-zinc-600 hover:text-[#306998]"
                    " dark:text-zinc-300 dark:hover:text-[#ffd43b]"
                    " transition-colors"
                )
            },
        ) or row.find("span", class_=lambda c: c and "font-medium" in c)
        time_tag = row.find("time")
        link_tag = row.find("a", href=True)
        
        if title:
            title_text = title.get_text(strip=True)
            author_text = author.get_text(strip=True) if author else "Unknown"
            time_text = time_tag.get_text(strip=True) if time_tag else "N/A"
            link = link_tag["href"] if link_tag else ""
            if link and not link.startswith("http"):
                link = "https://blog.python.org" + link
                
            posts.append({
                "title": title_text,
                "author": author_text,
                "published_time": time_text,
                "post_link": link or title_text
            })

    # 2. Featured section post
    section = doc.find("section")
    if section:
        title_el = section.find(["h1", "h2", "h3"])
        if title_el:
            title_text = title_el.get_text(strip=True)
            if not any(p["title"] == title_text for p in posts):
                author_el = section.find("span", class_=lambda c: c and "font-medium" in c) or section.find("a", class_=lambda c: c and "font-medium" in c)
                time_el = section.find("time")
                link_el = section.find("a", href=True)
                link = link_el["href"] if link_el else ""
                if link and not link.startswith("http"):
                    link = "https://blog.python.org" + link
                posts.append({
                    "title": title_text,
                    "author": author_el.get_text(strip=True) if author_el else "Unknown",
                    "published_time": time_el.get_text(strip=True) if time_el else "N/A",
                    "post_link": link or title_text
                })

    # 3. Article cards
    for article in doc.find_all("article"):
        title_el = article.find(["h3", "h2", "h1"])
        if title_el:
            title_text = title_el.get_text(strip=True)
            if not any(p["title"] == title_text for p in posts):
                author_el = article.find("span", class_=lambda c: c and "font-medium" in c) or article.find("a", class_=lambda c: c and "font-medium" in c)
                time_el = article.find("time")
                link_el = article.find("a", href=True)
                link = link_el["href"] if link_el else ""
                if link and not link.startswith("http"):
                    link = "https://blog.python.org" + link
                posts.append({
                    "title": title_text,
                    "author": author_el.get_text(strip=True) if author_el else "Unknown",
                    "published_time": time_el.get_text(strip=True) if time_el else "N/A",
                    "post_link": link or title_text
                })

    if RICH_AVAILABLE:
        console.print(f"Scraped {len(posts)} articles successfully.", style="#3fb950")
    else:
        print(f"Scraped {len(posts)} posts.")

    return posts


def get_db_connection():
    """Connect to PostgreSQL with retries."""
    host = os.getenv("DB_HOST", "psql-db")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "123456")
    dbname = os.getenv("DB_NAME", "python_blogs")

    max_retries = 10
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname
            )
            if RICH_AVAILABLE:
                console.print(f"Connected to PostgreSQL database [#38bdf8]{dbname}[/#38bdf8] at [dim #8b949e]{host}:{port}[/dim #8b949e]", style="#3fb950")
            else:
                print(f"Connected to PostgreSQL database '{dbname}' at {host}:{port}")
            return conn
        except psycopg2.OperationalError as err:
            if RICH_AVAILABLE:
                console.print(f"[Attempt {attempt}/{max_retries}] Connecting to PostgreSQL...", style="dim #8b949e")
            else:
                print(f"[Attempt {attempt}/{max_retries}] Waiting for database connection...")
            time.sleep(3)
    
    raise Exception("Could not connect to PostgreSQL after multiple attempts.")


def init_db(conn):
    """Create table if not exists."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS blog_posts (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                published_time TEXT,
                post_link TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
    if RICH_AVAILABLE:
        console.print("Verified database schema: Table [dim #38bdf8]blog_posts[/dim #38bdf8] ready.", style="#3fb950")
    else:
        print("Database table 'blog_posts' verified/created.")


def save_posts_to_db(conn, posts):
    """Insert or update blog posts in the database."""
    with conn.cursor() as cur:
        for p in posts:
            cur.execute("""
                INSERT INTO blog_posts (title, author, published_time, post_link)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (post_link) 
                DO UPDATE SET 
                    title = EXCLUDED.title,
                    author = EXCLUDED.author,
                    published_time = EXCLUDED.published_time;
            """, (p["title"], p["author"], p["published_time"], p["post_link"]))
        conn.commit()
    if RICH_AVAILABLE:
        console.print(f"Saved {len(posts)} posts into PostgreSQL.", style="#3fb950")
        print()
    else:
        print(f"Saved {len(posts)} posts to database.")


def fetch_and_display_db_records(conn):
    """Display stored records using clean TUI layout."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, title, author, published_time, post_link FROM blog_posts ORDER BY id ASC;")
        rows = cur.fetchall()
        
    if RICH_AVAILABLE:
        console.print(Rule(title="[bold #38bdf8] STORED POSTGRESQL RECORDS [/bold #38bdf8]", style="#30363d"))
        print()

        for idx, row in enumerate(rows):
            record_id, title, author, pub_date, link = row
            
            item = Text()
            item.append(f"{record_id:02d}  ", style="bold #38bdf8")
            item.append(f"{title}\n", style="bold bright_white")
                
            item.append("    ", style="dim")
            item.append(f"{author}", style="dim #8b949e")
            item.append("  •  ", style="dim #484f58")
            item.append(f"{pub_date}", style="dim #8b949e")
            item.append("  •  ", style="dim #484f58")
            item.append(f"{link}\n", style="dim #58a6ff")
            
            console.print(item)

        console.print(Rule(style="#30363d"))
        console.print(f"Completed: {len(rows)} records active in PostgreSQL database.", style="dim #8b949e")
        print()
    else:
        print("\nStored Posts in PostgreSQL:")
        for row in rows:
            print(f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Date: {row[3]} | Link: {row[4]}")


def main():
    print_banner()
    posts = scrape_python_blogs()

    try:
        conn = get_db_connection()
        init_db(conn)
        save_posts_to_db(conn, posts)
        fetch_and_display_db_records(conn)
        conn.close()
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"Database operation error: {e}", style="bold #f85149")
        else:
            print(f"Database operation error: {e}")


if __name__ == "__main__":
    main()
