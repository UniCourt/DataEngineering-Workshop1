import requests
from bs4 import BeautifulSoup
import re
import psycopg2

conn = psycopg2.connect(database = "hw", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "123456",
                        port = 5434)
cursor = conn.cursor()

res = requests.get('https://blog.python.org/')
soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
data=soup.find('div',id='Blog1')
	
#footer = data.find('div',class_='post-footer').get_text()
count=0
for row in data.find('div',class_='post-footer'):
	count=count+1;
	
page1 = data.find('div')
page1 = page1.get_text(strip=False, separator=' ')

print(page1+"\n----------------------------------------\n")

query = "INSERT INTO scrapedData (page) VALUES (%s);"
data = (page1)

cursor.execute("INSERT INTO scrapedData (page) VALUES (%s);",(page1,))

# Commit the transaction
cursor.close()
conn.commit()
