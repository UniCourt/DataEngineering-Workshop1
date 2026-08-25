import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from io import BytesIO
from urllib.parse import urljoin

url = "https://sample-files.com/documents/pdf/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Download and parse the webpage
response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

# Find all PDF links
pdf_links = []

for link in soup.find_all("a"):
    href = link.get("href")

    if href and ".pdf" in href.lower():
        pdf_url = urljoin(url, href)

        if pdf_url not in pdf_links:
            pdf_links.append(pdf_url)

print(f"Found {len(pdf_links)} PDF links")

# Open ONE output file for all PDFs
with open("all_pdf_text.txt", "w", encoding="utf-8") as output_file:

    # Go through every PDF
    for number, pdf_url in enumerate(pdf_links, start=1):
        print(f"Scraping PDF {number}: {pdf_url}")

        try:
            # Download the PDF
            pdf_response = requests.get(
                pdf_url,
                headers=headers,
                timeout=30
            )
            pdf_response.raise_for_status()

            # Read the PDF from memory
            pdf = PdfReader(BytesIO(pdf_response.content))

            # Add a heading so we know where each PDF starts
            output_file.write("\n")
            output_file.write("=" * 80 + "\n")
            output_file.write(f"PDF {number}: {pdf_url}\n")
            output_file.write("=" * 80 + "\n\n")

            # Extract text from every page
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    output_file.write(page_text + "\n")

        except Exception as error:
            print(f"Could not scrape PDF {number}: {error}")

print("\nAll PDF text has been saved to all_pdf_text.txt")
