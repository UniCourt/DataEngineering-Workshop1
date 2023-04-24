import requests
from bs4 import BeautifulSoup

r=requests.get('https://blog.python.org/')
soup=BeautifulSoup(r.content,'html.parser')

for link in soup.find_all('a'):
	print(link.get('href'))
