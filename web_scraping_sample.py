import requests
from bs4 import BeautifulSoup

url = "https://lms.nmamit.in/"

response = requests.get(url)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

print("\nWebsite Title:")
print(soup.title.text)

print("\nHeadings:")
for heading in soup.find_all(["h1", "h2", "h3"]):
    print(heading.get_text(strip=True))
