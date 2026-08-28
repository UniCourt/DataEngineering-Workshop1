import requests
from bs4 import BeautifulSoup

url = "https://blog.python.org/blog/"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

titles = soup.find_all("h3")

for title in titles:
    print("Title:", title.get_text(strip=True))

    author = title.find_next("a", href=lambda href: href and "/authors/" in href)
    if author:
        print("Author:", author.get_text(strip=True))
    else:
        print("Author: Not found")

    date = title.find_next("time")
    if date:
        print("Date:", date.get_text(strip=True))
    else:
        print("Date: Not found")

    print("--------------------------------")