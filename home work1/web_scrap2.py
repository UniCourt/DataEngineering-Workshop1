import requests
from bs4 import BeautifulSoup
import sqlite3

conn= sqlite3.connect('cputest.db')
c=conn.cursor()
#c.execute('''CREATE TABLE pythonblog( title TEXT, link TEXT)''')
url='https://blog.python.org/'
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
articles=soup.find_all('h3',class_='entry-title')
for article in articles:
	title=article.find('a').get_text()
	link=article.find('a')['href']
	c.execute('''INSERT INTO pythonblog VALUES(?,?)''',(title,link))
	print(f'Title:{title}')
	print(f'Link:{link}')
	print()
latest_post=soup.find('div',class_='date-header')
if latest_post  is not None:
	latest_title=latest_post.find('h2').get_text().strip()
	latest_date=latest_post.find_next_sibling().get_text().strip()
	print(f'Latest Post:{latest_title}({latest_date})')
conn.commit()
print('complete.')
c.execute('''SELECT*FROM pythonblog''')
results=c.fetchall()
print(results)
conn.close()
