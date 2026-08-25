import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

url = "https://sample-files.com/documents/pdf/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Try the webpage a few times
for attempt in range(3):
    try:
        print(f"Connecting to website... Attempt {attempt + 1}")

        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        print("Website downloaded successfully!")
        break

    except requests.exceptions.RequestException as e:
        print("Connection failed:", e)

        if attempt == 2:
            raise

        time.sleep(2)


soup = BeautifulSoup(response.content, "html5lib")

# Find PDF links
pdf_links = []

for link in soup.find_all("a", href=True):
    href = link["href"]

    if ".pdf" in href.lower():
        pdf_links.append(urljoin(url, href))


print("PDF links found:", len(pdf_links))

for pdf in pdf_links:
    print(pdf)


# Download the first PDF
if pdf_links:
    pdf_url = pdf_links[0]

    print("Downloading:", pdf_url)

    pdf_response = requests.get(
        pdf_url,
        headers=headers,
        timeout=30
    )

    pdf_response.raise_for_status()

    with open("sample.pdf", "wb") as file:
        file.write(pdf_response.content)

    print("PDF downloaded successfully!")
else:
    print("No PDF links found.")
