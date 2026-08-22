import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'postgres'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', '123456'),
        port=os.environ.get('DB_PORT', '5432')
    )

def scrape_pages(search_type, search_query, pages_to_scrape):
    base_url = "https://blog.python.org/blog/"
    if search_type == 'tag':
        base_url = "https://blog.python.org/tags/"
        current_url = f"{base_url}{search_query}"
    elif search_type == 'year':
        current_url = f"{base_url}year/{search_query}/"
    else:
        current_url = base_url

    posts_inserted = 0
    pages_scraped = 0
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return

    for _ in range(pages_to_scrape):
        print(f"Scraping page {pages_scraped + 1}: {current_url}")
        try:
            res = requests.get(current_url, timeout=10)
        except Exception as e:
            print(f"Failed to fetch {current_url}: {e}")
            break

        if res.status_code != 200:
            print(f"Failed to fetch {current_url} (status code {res.status_code})")
            break
            
        soup = BeautifulSoup(res.content, 'html5lib')
        
        post_containers = soup.find_all('article')
            
        if not post_containers:
            print("No posts found on this page. Stopping.")
            break
            
        for container in post_containers:
            h3 = container.find('h3')
            title = h3.text.strip() if h3 else "Unknown Title"
            
            a_tag = h3.find_parent('a') if h3 else container.find('a')
            if a_tag and a_tag.has_attr('href'):
                url = a_tag['href']
                if url.startswith('/'):
                    url = base_url.replace('/blog/', '') + url
            else:
                url = current_url
                
            id_val = ""
            url_part = url.replace("https://blog.python.org/", "").replace("http://blog.python.org/", "")
            parts = [p for p in url_part.split('/') if p]
            if len(parts) >= 3:
                year = parts[0]
                slug = parts[-1].replace('.html', '')
                id_val = f"{year}:{slug}"
            else:
                id_val = url_part.replace('.html', '').replace('/', ':')
                
            if not id_val:
                id_val = title
                
            date_val = "Unknown Date"
            author_val = "Unknown Author"
            time_tag = container.find('time')
            if time_tag:
                date_val = time_tag.text.strip()
                parent = time_tag.parent
                if parent:
                    parts = parent.text.split('·')
                    if len(parts) > 1:
                        author_val = parts[0].strip()
                    elif parent.text.strip():
                        author_val = parent.text.replace(date_val, '').strip()
            
            p_tag = container.find('p')
            body_val = p_tag.text.strip()[:500] if p_tag else ""
            
            tag_links = container.find_all('a', href=lambda href: href and '/tags/' in href)
            tags_val = ",".join([t.text.strip() for t in tag_links]) if tag_links else ""
            
            try:
                cur.execute("""
                    INSERT INTO python_blog_posts (id, title, date, author, body, url, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (id_val, title, date_val, author_val, body_val, url, tags_val))
                if cur.rowcount > 0:
                    posts_inserted += 1
            except Exception as e:
                print(f"DB Insert error for {id_val}: {e}")
                conn.rollback()
            else:
                conn.commit()
                
        pages_scraped += 1
        
        next_link_href = None
        for a in soup.find_all('a'):
            if a.text and ('Next' in a.text or 'Older' in a.text):
                next_link_href = a.get('href')
                break
                
        if not next_link_href and pages_scraped > 0:
            if search_type == '':
                next_link_href = f"/{pages_scraped + 1}"
            
        if next_link_href:
            if next_link_href.startswith('/'):
                current_url = base_url.replace('/blog/', '') + next_link_href
            else:
                current_url = next_link_href
        else:
            print("No more pages available.")
            break
            
    cur.close()
    conn.close()
    
    print("\n--- Summary ---")
    print(f"Pages scraped: {pages_scraped}")
    print(f"Posts inserted: {posts_inserted}")


if __name__ == "__main__":
    search_type = ""
    search_query = ""
    
    print("Welcome to Python Blog Scraper!")
    q_type = input("Do you want to search by 'year' or 'tag'? (Leave blank for default homepage): ").strip().lower()
    
    if q_type in ['year', 'tag']:
        search_type = q_type
        search_query = input(f"Enter the {q_type} you want to search for: ").strip()
        
    pages_input = input("How many pages to scrape? (default 1): ").strip()
    try:
        pages_to_scrape = int(pages_input) if pages_input else 1
    except ValueError:
        pages_to_scrape = 1
        
    print("\nStarting scrape...")
    scrape_pages(search_type, search_query, pages_to_scrape)
