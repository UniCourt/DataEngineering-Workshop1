import requests
from bs4 import BeautifulSoup

url = "https://nitte.edu.in/nmamit/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.content, "html5lib")

print("\nHeadings found on NMAMIT website:\n")

for heading in soup.find_all(["h1", "h2", "h3"]):
    print(heading.get_text(strip=True))
