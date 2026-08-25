import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

url = "https://sample-files.com/documents/pdf/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

pdfs = []


for table in soup.find_all("table"):

    rows = table.find_all("tr")

    for row in rows:

        columns = row.find_all(["td", "th"])

        if len(columns) >= 6:

            link = columns[5].find("a")

            if link and link.get("href"):

                pdf_url = urljoin(url, link["href"])

                filename = Path(pdf_url).name

                if pdf_url not in [item[0] for item in pdfs]:
                    pdfs.append((pdf_url, filename))


if not pdfs:
    print("No PDFs found.")
    exit()


print("\n========== PDF FILES ==========\n")

for i, (pdf_url, filename) in enumerate(pdfs, 1):
    print(f"{i}. {filename}")

choice = int(
    input(f"\nChoose PDF number (1-{len(pdfs)}): ")
)

pdf_url, filename = pdfs[choice - 1]

print("\nSelected:", filename)
print("Downloading...")

pdf_response = requests.get(pdf_url)
pdf_response.raise_for_status()

with open(filename, "wb") as file:
    file.write(pdf_response.content)

print("\nPDF downloaded successfully!")
print("Saved as:", filename)