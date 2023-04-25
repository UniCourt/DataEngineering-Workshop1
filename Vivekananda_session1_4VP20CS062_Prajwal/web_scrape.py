import requests
from bs4 import BeautifulSoup
import csv
import psycopg2

url = 'https://blog.python.org/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

links = []
authors = []
titles =[]
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.startswith('https://blog.python.org/'):
        links.append(href)
        
 
 	
for i in soup.find_all('h3', class_='entry-title'):
 	string = i.find('a').getText()
 	titles.append(string.strip())
for i in soup.find_all('span', class_='fn'):
 	string = i.getText()
 	authors.append(string.strip())
 	

# Database connection details
db_name = 'hw1'
db_user = 'postgres'
db_password = '123456'
db_host = '172.17.0.2'
db_port = '5432'

# Connection to database
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

#cursor obj
cur = conn.cursor()

#creating table
cur.execute("""
    CREATE TABLE IF NOT EXISTS blog_data2 (
        id SERIAL PRIMARY KEY,
        link VARCHAR(255) NOT NULL
    )
""")

# Inserting into tables
for link in links:
    cur.execute("""
        INSERT INTO blog_data2 (link)
        VALUES (%s)
    """, (link,))
for i in range(4):
	cur.execute(
		"INSERT INTO python_blogs(no,title,author) VALUES(%s,%s,%s)", (i+1, titles[i], authors[i])
		)
	


conn.commit()
cur.close()
conn.close()

