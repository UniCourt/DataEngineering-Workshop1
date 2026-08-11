import requests
from bs4 import BeautifulSoup

url = "https://www.w3schools.com/python/"
res = requests.get(url)

soup = BeautifulSoup(res.content, "html5lib")

print("Page title:")
print(soup.title.text)

print("\nHeadings:")
for heading in soup.find_all(["h1", "h2", "h3"]):
    print(heading.get_text(strip=True))
