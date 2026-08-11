import requests
from bs4 import BeautifulSoup

url = "https://www.w3schools.com/python/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\nPage Title:")
print(soup.title.get_text(strip=True))

print("\nHeadings:")

for heading in soup.find_all(["h1", "h2", "h3"]):
    print(heading.get_text(strip=True))
