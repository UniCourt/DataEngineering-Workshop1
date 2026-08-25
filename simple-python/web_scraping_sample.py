import requests
from bs4 import BeautifulSoup

url = "https://nitte.edu.in/nmamit/"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

print("Status:", response.status_code)

print("\nLINKS:")

for link in soup.find_all("a"):
    text = link.get_text(" ", strip=True)
    href = link.get("href")

    if text and href:
        print(text, "->", href)
