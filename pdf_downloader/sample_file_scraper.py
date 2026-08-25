from bs4 import BeautifulSoup
from urllib.parse import urljoin
import subprocess
import os

# Website
base_url = "https://sample-files.com/"

# --------------------------------------------------
# STEP 1: Download the main webpage
# --------------------------------------------------

print("Downloading main webpage...")

subprocess.run([
    "curl",
    "-L",
    base_url,
    "-o",
    "sample.html"
], check=True)

# Read HTML
with open("sample.html", "r", encoding="utf-8") as file:
    html = file.read()

soup = BeautifulSoup(html, "html.parser")

print("Title:", soup.title.get_text(strip=True))

# --------------------------------------------------
# STEP 2: Find the PDF page
# --------------------------------------------------

pdf_page = None

for link in soup.find_all("a"):
    text = link.get_text(strip=True)
    href = link.get("href")

    if text == "PDF":
        pdf_page = urljoin(base_url, href)
        break

if not pdf_page:
    print("PDF page not found.")
    exit()

print("PDF page:", pdf_page)

# --------------------------------------------------
# STEP 3: Download the PDF page
# --------------------------------------------------

subprocess.run([
    "curl",
    "-L",
    pdf_page,
    "-o",
    "pdf_page.html"
], check=True)

# Read PDF page
with open("pdf_page.html", "r", encoding="utf-8") as file:
    pdf_html = file.read()

pdf_soup = BeautifulSoup(pdf_html, "html.parser")

# --------------------------------------------------
# STEP 4: Find all PDF links
# --------------------------------------------------

pdf_links = []

for link in pdf_soup.find_all("a"):

    href = link.get("href")

    if href and href.lower().endswith(".pdf"):

        pdf_url = urljoin(pdf_page, href)

        if pdf_url not in pdf_links:
            pdf_links.append(pdf_url)

print("\nPDF files found:", len(pdf_links))

# --------------------------------------------------
# STEP 5: Create download folder
# --------------------------------------------------

os.makedirs("pdfs", exist_ok=True)

# --------------------------------------------------
# STEP 6: Download PDFs
# --------------------------------------------------

for i, pdf_url in enumerate(pdf_links, start=1):

    filename = pdf_url.split("/")[-1]

    output_path = os.path.join("pdfs", filename)

    print(f"\nDownloading {i}/{len(pdf_links)}: {filename}")

    # Skip files that already exist
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print("Already downloaded. Skipping.")
        continue

    success = False

    # Try three times
    for attempt in range(1, 4):

        print(f"Attempt {attempt}/3")

        result = subprocess.run([
            "curl",
            "-L",
            "--retry", "2",
            "--retry-delay", "2",
            pdf_url,
            "-o",
            output_path
        ])

        if result.returncode == 0:
            success = True
            print("Downloaded successfully!")
            break

    if not success:
        print("FAILED:", filename)

# --------------------------------------------------
# DONE
# --------------------------------------------------

print("\nScraping completed!")

print("\nDownloaded files:")

for file in os.listdir("pdfs"):
    print("-", file)
