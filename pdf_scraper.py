import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

url = "https://sample-files.com/documents/pdf/"
folder = "pdf_downloads"

os.makedirs(folder, exist_ok=True)

html = subprocess.check_output(
    ["curl", "-L", url],
    text=True
)

soup = BeautifulSoup(html, "html.parser")
count = 0

for link in soup.find_all("a"):
    href = link.get("href")

    if href and ".pdf" in href.lower():
        pdf_url = urljoin(url, href)
        filename = pdf_url.split("/")[-1]
        filepath = os.path.join(folder, filename)

        print("Downloading:", filename)

        subprocess.run(
            ["curl", "-L", "-o", filepath, pdf_url],
            check=True
        )

        count += 1

print(f"\nDownloaded {count} PDFs successfully.")
