import requests
from bs4 import BeautifulSoup
import re
import psycopg2

res = requests.get('https://www.lipsum.com/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data = soup.find('div', id=re.compile(r"Panes"))
print(soup.find("h1").text)

question_list = []
answer_list = []
for row in data.find_all("div"):
    question_header = row.h2
    question_list.append(question_header.text)
    answer_string = ""
    parent_div_element = row.find_parent("div")
    all_p_tag_list = parent_div_element.find_all("p")
    for p_tag in all_p_tag_list:
        answer_string = answer_string + p_tag.text + "\n"
    answer_list.append(answer_string)

# Connect to PostgreSQL with retry logic
import time
max_retries = 5
for i in range(max_retries):
    try:
        conn = psycopg2.connect(
            host="psql-db",
            database="postgres",
            user="postgres",
            password="123456"
        )
        break
    except psycopg2.OperationalError as e:
        if i == max_retries - 1:
            raise e
        print("Waiting for database...")
        time.sleep(2)

cur = conn.cursor()

# Create table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS scraped_data (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
""")

# Insert the scraped data into the database
for i in range(len(question_list)):
    cur.execute(
        "INSERT INTO scraped_data (question, answer) VALUES (%s, %s)",
        (question_list[i], answer_list[i])
    )

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("The question and answer have been saved to PostgreSQL database in the 'scraped_data' table.")

