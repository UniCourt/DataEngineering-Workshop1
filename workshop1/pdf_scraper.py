import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://sample-files.com/documents/pdf/"

response = requests.get(url)

print("Website status:", response.status_code)

soup = BeautifulSoup(response.content, "html5lib")

for link in soup.find_all("a"):
    href = link.get("href")

    if href and ".pdf" in href.lower():
        pdf_url = urljoin(url, href)

        print("PDF found:")
        print(pdf_url)

        pdf_response = requests.get(
            pdf_url,
            verify=False
        )

        with open("sample.pdf", "wb") as file:
            file.write(pdf_response.content)

        print("PDF downloaded successfully!")

        break
