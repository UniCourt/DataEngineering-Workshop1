import requests
from bs4 import BeautifulSoup
import os
import urllib3

# Ignore SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://sample-files.com/documents/pdf/"

# Get webpage
response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    verify=False
)

soup = BeautifulSoup(response.content, "html.parser")

# Find table
table = soup.find("table")

# Create downloads folder
os.makedirs("downloads", exist_ok=True)

# Skip header row
rows = table.find_all("tr")[1:]

print(f"Found {len(rows)} PDFs\n")

for index, row in enumerate(rows, start=1):

    cols = row.find_all("td")

    # First column = File Name
    file_name = cols[0].text.strip()

    # Last column contains Download link
    pdf_link = cols[5].find("a")["href"]

    # Convert relative URL to full URL
    if not pdf_link.startswith("http"):
        pdf_link = "https://sample-files.com" + pdf_link

    print(f"Downloading PDF {index}: {file_name}")
    print(pdf_link)

    try:
        pdf = requests.get(
            pdf_link,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
            verify=False
        )

        with open(f"downloads/sample_{index}.pdf", "wb") as f:
            f.write(pdf.content)

        print(f"Saved: downloads/sample_{index}.pdf\n")

    except Exception as e:
        print(f"Failed to download: {pdf_link}")
        print(f"Error: {e}\n")
        continue

print("All PDFs processed.")
