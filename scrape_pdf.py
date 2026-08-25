import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://sample-files.com/documents/pdf/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a"):
    if "Download" in link.text:
        pdf_url = urljoin(url, link.get("href"))
        print("PDF URL:", pdf_url)

        pdf_response = requests.get(pdf_url)

        with open("sample-pdf.pdf", "wb") as file:
            file.write(pdf_response.content)

        print("PDF downloaded successfully!")
        break
