import requests
from bs4 import BeautifulSoup

url = "https://blog.python.org/2026/08/python-31214-31116-31021"

res = requests.get(url)
print("Status:", res.status_code)

soup = BeautifulSoup(res.content, "html.parser")

title = soup.find("h1")

if title:
    print(title.text.strip())
else:
    print("Title not found")

