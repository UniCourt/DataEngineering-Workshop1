import requests
from bs4 import BeautifulSoup

res = requests.get('https://blog.python.org/blog')
res.raise_for_status()
soup = BeautifulSoup(res.content, 'html5lib')
articles = soup.find_all('article', class_='post-card')
for article in articles:
    title_el = article.find('h3')
    author_el = article.find('a', class_=lambda c: c and 'font-medium' in c)
    time_el = article.find('time')
    title = title_el.text.strip() if title_el else 'N/A'
    author = author_el.text.strip() if author_el else 'N/A'
    time_text = time_el.get_text(strip=True) if time_el else 'N/A'
    print(f"Title: {title}\nAuthor: {author}\nTime: {time_text}\n")