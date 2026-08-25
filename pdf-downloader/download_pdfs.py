import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

page_url = "https://sample-files.com/documents/pdf/"

response = requests.get(page_url)

print("Page status:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

os.makedirs("pdfs", exist_ok=True)

pdf_links = []

for link in soup.find_all("a", href=True):
    href = link["href"]

    if ".pdf" in href.lower():
        pdf_url = urljoin(page_url, href)

        if pdf_url not in pdf_links:
            pdf_links.append(pdf_url)

print("PDFs found:", len(pdf_links))

for number, pdf_url in enumerate(pdf_links, start=1):

    print(f"\nDownloading {number}: {pdf_url}")

    try:
        response = requests.get(
            pdf_url,
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        filename = pdf_url.split("/")[-1]
        filepath = os.path.join("pdfs", filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        print("Downloaded:", filename)

    except requests.exceptions.RequestException as error:
        print("Failed:", error)

print("\nFinished.")
