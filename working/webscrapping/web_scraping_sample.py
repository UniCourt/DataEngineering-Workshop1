# import requests
# from bs4 import BeautifulSoup

# soup = BeautifulSoup(requests.get("https://sample-files.com/documents/pdf/").text, "html.parser")
# for a in soup.find_all("a", href=True):
#     if ".pdf" in a["href"].lower():
#         print(a["href"])    



import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

url = "https://sample-files.com/documents/pdf/"

# Get webpage
res = requests.get(url)

# Parse webpage
soup = BeautifulSoup(res.content, "html5lib")

# Create folder
folder_name = "pdf_files"
os.makedirs(folder_name, exist_ok=True)

# Find all links
links = soup.find_all("a")

pdf_count = 0

for link in links:

    href = link.get("href")

    # Check if link is a PDF
    if href and ".pdf" in href.lower():

        # Convert relative URL to absolute URL
        pdf_url = urljoin(url, href)

        # Get filename from URL
        filename = pdf_url.split("/")[-1]

        # Remove query parameters if present
        filename = filename.split("?")[0]

        # Complete path
        filepath = os.path.join(folder_name, filename)

        print("PDF:", filename)
        print("URL:", pdf_url)

        # Download PDF
        pdf_res = requests.get(pdf_url)

        # Save PDF
        with open(filepath, "wb") as file:
            file.write(pdf_res.content)

        print("Downloaded:", filepath)
        print("-" * 80)

        pdf_count += 1

print("Total PDFs downloaded:", pdf_count)