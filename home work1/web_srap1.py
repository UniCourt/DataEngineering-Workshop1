import requests
from bs4 import BeautifulSoup
url='https://blog.python.org/'
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
articles=soup.find_all('h3',class_='entry-title')
for article in articles:
	title=article.find('a').get_text()
	link=article.find('a')['href']
	print(f'Title:{title}')
	print(f'Link:{link}')
	print()
latest_post=soup.find('div',class_='date-header')
if latest_post  is not None:
	latest_title=latest_post.find('h2').get_text().strip()
	latest_link=latest_post.find_next_sibling().get_text().strip()
	print(f'Latest Post:{latest_title}({latest_link})')
	
	
