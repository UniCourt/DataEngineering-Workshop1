import os
import requests
import pdfplumber
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_URL = "https://sample-files.com/documents/pdf/"

PDF_FOLDER = "pdfs"
TEXT_FOLDER = "extracted_text"

MAX_PDFS = 5


# --------------------------------------------------
# Browser-like headers
# --------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/avif,image/webp,"
        "*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}


# --------------------------------------------------
# Create output directories
# --------------------------------------------------

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(TEXT_FOLDER, exist_ok=True)


# --------------------------------------------------
# 1. Fetch the PDF listing page
# --------------------------------------------------

print("=" * 60)
print("Fetching PDF listing page...")
print("=" * 60)

try:
    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=30
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

except requests.exceptions.RequestException as error:
    print("Failed to access the website.")
    print("Error:", error)
    exit(1)


# --------------------------------------------------
# 2. Parse the HTML
# --------------------------------------------------

soup = BeautifulSoup(response.content, "html.parser")


# --------------------------------------------------
# 3. Find all PDF links
# --------------------------------------------------

pdf_links = []

for link in soup.find_all("a", href=True):

    href = link["href"].strip()

    # Check whether the link points to a PDF
    if ".pdf" in href.lower():

        pdf_url = urljoin(BASE_URL, href)

        # Avoid duplicate links
        if pdf_url not in pdf_links:
            pdf_links.append(pdf_url)


# --------------------------------------------------
# 4. Select the first 5 PDFs
# --------------------------------------------------

pdf_links = pdf_links[:MAX_PDFS]


print()
print("=" * 60)
print(f"Found {len(pdf_links)} PDF links")
print("=" * 60)

for index, pdf_url in enumerate(pdf_links, start=1):
    print(f"{index}. {pdf_url}")


# --------------------------------------------------
# Check whether PDFs were found
# --------------------------------------------------

if not pdf_links:

    print()
    print("No PDF links were found.")
    print("The website may be blocking automated requests.")
    exit(1)


# --------------------------------------------------
# 5. Download and extract each PDF
# --------------------------------------------------

for index, pdf_url in enumerate(pdf_links, start=1):

    print()
    print("=" * 60)
    print(f"Processing PDF {index}/{len(pdf_links)}")
    print("=" * 60)

    print("URL:", pdf_url)

    try:

        # ------------------------------------------
        # Download PDF
        # ------------------------------------------

        pdf_response = requests.get(
            pdf_url,
            headers=HEADERS,
            timeout=60
        )

        print("Download status:", pdf_response.status_code)

        pdf_response.raise_for_status()


        # ------------------------------------------
        # Determine PDF filename
        # ------------------------------------------

        path = urlparse(pdf_url).path

        filename = os.path.basename(path)

        if not filename:
            filename = f"sample_{index}.pdf"

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"


        # ------------------------------------------
        # Save PDF
        # ------------------------------------------

        pdf_path = os.path.join(
            PDF_FOLDER,
            filename
        )

        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)

        print("PDF saved:", pdf_path)


        # ------------------------------------------
        # Create TXT filename
        # ------------------------------------------

        txt_filename = os.path.splitext(filename)[0] + ".txt"

        txt_path = os.path.join(
            TEXT_FOLDER,
            txt_filename
        )


        # ------------------------------------------
        # Extract text using pdfplumber
        # ------------------------------------------

        print("Extracting text...")

        with pdfplumber.open(pdf_path) as pdf:

            with open(
                txt_path,
                "w",
                encoding="utf-8"
            ) as text_file:

                for page_number, page in enumerate(
                    pdf.pages,
                    start=1
                ):

                    text = page.extract_text()

                    text_file.write(
                        f"\n"
                        f"========== PAGE {page_number} "
                        f"==========\n\n"
                    )

                    if text:
                        text_file.write(text)
                    else:
                        text_file.write(
                            "[No text found on this page]"
                        )

                    text_file.write("\n")


        print("Text saved:", txt_path)


    except requests.exceptions.RequestException as error:

        print("Download failed.")
        print("Error:", error)

        continue


    except Exception as error:

        print("PDF processing failed.")
        print("Error:", error)

        continue


# --------------------------------------------------
# Finished
# --------------------------------------------------

print()
print("=" * 60)
print("PDF SCRAPING COMPLETED")
print("=" * 60)

print()
print("Downloaded PDFs:")
print(f"    {PDF_FOLDER}/")

print()
print("Extracted text:")
print(f"    {TEXT_FOLDER}/")