import requests
from bs4 import BeautifulSoup

res = requests.get('https://blog.python.org/')
res.raise_for_status()
soup = BeautifulSoup(res.content, 'html5lib')
articles = soup.find_all('article', class_='post-card')
for article in articles:
    title_el = article.find('h3')
    title = title_el.text.strip() if title_el else 'N/A'
    print(title)
