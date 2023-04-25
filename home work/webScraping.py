import requests
from bs4 import BeautifulSoup
import re
import psycopg2
conn = psycopg2.connect(
host="172.17.0.2",
port="5432",
database="pybd",
user="postgres",
password="123456"
)
print("Connection Successful")
cur = conn.cursor()
res = requests.get('https://blog.python.org/')
soup = BeautifulSoup(res.content, 'html5lib')
titles=[]
authors=[]
for i in soup.find_all('h3', class_='entry-title'):
 string = i.find('a').getText()
 titles.append(string.strip())
for i in soup.find_all('span', class_='fn'):
 string = i.getText()
 authors.append(string.strip())
for i in range(4):
 cur.execute(
 "INSERT INTO py_blogs(no,title,author) VALUES(%s,%s,%s)", (i+1, titles[i], authors[i])
 )
conn.commit()
cur.close()
conn.close()
