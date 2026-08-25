import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import os

website = 'https://sample-files.com/documents/pdf/'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

# Get the webpage
res = requests.get(website, headers=headers, timeout=30)
res.raise_for_status()

# Parse HTML
soup = BeautifulSoup(res.content, 'html5lib')

# Find all links
links = soup.find_all('a', href=True)

# Create folder for PDFs
os.makedirs("pdfs", exist_ok=True)

count = 0

# Check every link
for link in links:

    href = link['href']

    # Check if link is a PDF
    if re.search(r'\.pdf(?:$|[?#])', href, re.IGNORECASE):

        pdf_url = urljoin(website, href)

        print("PDF found:")
        print(pdf_url)

        try:
            # Download PDF
            pdf_res = requests.get(
                pdf_url,
                headers=headers,
                timeout=30
            )

            pdf_res.raise_for_status()

            # Get filename from URL
            filename = pdf_url.split("/")[-1].split("?")[0]

            # Save PDF
            filepath = os.path.join("pdfs", filename)

            with open(filepath, "wb") as file:
                file.write(pdf_res.content)

            count += 1

            print("Downloaded:", filename)
            print()

        except requests.RequestException as e:
            print("Failed to download:", pdf_url)
            print("Error:", e)

print("================================")
print("Total PDFs downloaded:", count)
print("================================")