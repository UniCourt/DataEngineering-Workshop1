import os
import time
import psycopg2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://sample-files.com/documents/pdf/"
user_agent = "Mozilla/5.0"

# Fetch environment variables for DB connection
db_host = os.environ.get("DB_HOST", "localhost")
db_name = os.environ.get("DB_NAME", "workshop_db")
db_user = os.environ.get("DB_USER", "postgres")
db_password = os.environ.get("DB_PASSWORD", "postgres")
db_port = os.environ.get("DB_PORT", "5432")

# Connection retry logic
conn = None
for i in range(15):
    try:
        print(f"Connecting to database at {db_host}:{db_port} (attempt {i+1}/15)...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Successfully connected to the database!")
        break
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}. Retrying in 2 seconds...")
        time.sleep(2)

if conn is None:
    raise Exception("Could not connect to PostgreSQL after 15 attempts. Exiting.")

try:
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_pages (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            html_content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    # Fetch HTML from url
    print(f"Fetching: {url}")
    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    # Insert HTML into PostgreSQL
    print("Saving HTML content to PostgreSQL...")
    cursor.execute(
        "INSERT INTO scraped_pages (url, html_content) VALUES (%s, %s) RETURNING id;",
        (url, html_content)
    )
    inserted_id = cursor.fetchone()[0]
    conn.commit()
    print(f"HTML content saved successfully with ID: {inserted_id}")

    # Parse and extract table
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.select_one(".has-fixed-layout")

    if not table:
        print("Error: Could not find the sample files table in the page.")
    else:
        dc = 0
        for row in table.select("tbody tr"):
            if dc >= 5:
                break

            title_el = row.select_one("td:nth-child(1)")
            link_el = row.select_one("td:nth-child(6) a")

            if not title_el or not link_el:
                continue

            title = title_el.get_text(strip=True)
            pdf_url = urljoin(url, link_el.get("href"))

            folder = title.replace("/", "-")
            os.makedirs(folder, exist_ok=True)

            filepath = os.path.join(folder, title + ".pdf")
            
            print(f"Downloading: {title} from {pdf_url}...")
            try:
                pdf_res = requests.get(pdf_url, headers=headers, stream=True)
                pdf_res.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in pdf_res.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Downloaded:", title)
                dc += 1
            except Exception as download_err:
                print(f"Failed to download {title}: {download_err}")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")