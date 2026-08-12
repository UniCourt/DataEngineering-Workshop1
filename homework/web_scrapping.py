import requests
from bs4 import BeautifulSoup
r=requests.get('https://pythoninsider.blogspot.com/')
soup=BeautifulSoup(r.content,'html.parser')
s=soup.find('div',class_='post-body entry-content')
lines=s.find_all('p')
for line in lines:
	print(line.text)
