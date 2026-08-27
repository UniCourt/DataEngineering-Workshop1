import requests
from bs4 import BeautifulSoup
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="postgres_service",
    database="LipsumGenerator",
    user="postgres",
    password="admin"
)

cursor = conn.cursor()

# Python Blog URL
url = "https://blog.python.org/"

# Request the webpage
response = requests.get(url)

print("Status Code:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.content, "html.parser")

# Find blog posts
posts = soup.find_all("article")

print("Posts found:", len(posts))

# Insert posts into PostgreSQL
for post in posts:
    title_tag = post.find(["h2", "h3"])

    if title_tag:
        title = title_tag.get_text(strip=True)

        # Find date if available
        date_tag = post.find("time")

        if date_tag:
            date = date_tag.get_text(strip=True)
        else:
            date = "N/A"

        print("Title:", title)
        print("Date:", date)
        print("-" * 50)

        cursor.execute(
            "INSERT INTO qn_ans (question, answer) VALUES (%s, %s)",
            (title, date)
        )

# Save changes
conn.commit()

cursor.close()
conn.close()

print("Blog data inserted into PostgreSQL successfully.")
