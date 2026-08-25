import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from pypdf import PdfReader

url = "https://sample-files.com/documents/pdf/"

# -------------------------------
# STEP 1: Get webpage
# -------------------------------
response = requests.get(url)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# -------------------------------
# STEP 2: Find PDF links
# -------------------------------
pdf_links = []

for link in soup.find_all("a", href=True):
    href = link["href"]

    # Convert relative URL to absolute URL
    pdf_url = urljoin(url, href)

    # Check if link is a PDF
    if ".pdf" in pdf_url.lower():
        if pdf_url not in pdf_links:
            pdf_links.append(pdf_url)

print("PDF links found:")
for pdf in pdf_links:
    print(pdf)

# -------------------------------
# STEP 3: Select ONE PDF
# -------------------------------
if not pdf_links:
    print("No PDF found.")
    exit()

pdf_url = pdf_links[0]

print("\nSelected PDF:")
print(pdf_url)

# -------------------------------
# STEP 4: Download the PDF
# -------------------------------
os.makedirs("pdfs", exist_ok=True)

filename = pdf_url.split("/")[-1].split("?")[0]

if not filename:
    filename = "downloaded.pdf"

filepath = os.path.join("pdfs", filename)

pdf_response = requests.get(pdf_url)
pdf_response.raise_for_status()

with open(filepath, "wb") as file:
    file.write(pdf_response.content)

print("\nPDF downloaded:")
print(filepath)

# -------------------------------
# STEP 5: Scrape / extract PDF text
# -------------------------------
reader = PdfReader(filepath)

print("\nNumber of pages:", len(reader.pages))

print("\n========== PDF DATA ==========\n")

for page_number, page in enumerate(reader.pages, start=1):

    text = page.extract_text()

    print(f"\n--- Page {page_number} ---\n")

    if text:
        print(text)
    else:
        print("No text found on this page.")
