import requests
from bs4 import BeautifulSoup
import re

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

file = open("qn_and_answer.txt", "w")
for i in range(len(question_list)):
    file.write(question_list[i] + "\n" + answer_list[i] + "\n")
file.close()

print("The question and answer have been saved to qn_and_answer.txt file")

import psycopg2

# Read the file your scraper just created
with open("qn_and_answer.txt", "r") as file:
    scraped_data = file.read()

# Connect to the PostgreSQL container 
# (Notice the host is 'psql-db', the exact name from your yaml file!)
conn = psycopg2.connect(
    host="psql-db",
    database="demo",
    user="postgres",
    password="123456"
)
cursor = conn.cursor()

# Create a table and insert the data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS web_data (
        id SERIAL PRIMARY KEY,
        content TEXT
    )
""")
cursor.execute("INSERT INTO web_data (content) VALUES (%s)", (scraped_data,))

conn.commit()
cursor.close()
conn.close()

print("Success: Scraped data saved to PostgreSQL!")

