import requests
from bs4 import BeautifulSoup

url = "https://nitte.edu.in/nmamit/"

res = requests.get(url)

print("Status Code:", res.status_code)

soup = BeautifulSoup(res.content, "html5lib")

print("Page Title:", soup.title)

print("\nTitle Text:")
print(soup.title.get_text(strip=True))
