import requests
from bs4 import BeautifulSoup
import psycopg2
import time

time.sleep(10) 

conn = psycopg2.connect(
    host="psql-db",
    database="postgres",
    user="postgres",
    password="123456"
)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS python_blogs (title TEXT, link TEXT);")
cursor.execute("TRUNCATE TABLE python_blogs;") 
conn.commit()

url = "https://blog.python.org/"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

all_links = soup.find_all('a')

for link_element in all_links:
    href = link_element.get('href')
    
    heading = link_element.find(['h1', 'h2', 'h3'])
    if heading != None:
        title = heading.text.strip()
    else:
        title = link_element.text.strip()
    
    if href != None:
        if '/20' in href:
            if title != "":
                
                if href.startswith('/'):
                    href = "https://blog.python.org" + href
                
                cursor.execute("INSERT INTO python_blogs (title, link) VALUES (%s, %s)", (title, href))

conn.commit()
cursor.close()
conn.close()

print("Scraping completed successfully!")
