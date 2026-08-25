import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time

base_url = 'https://sample-files.com/documents/pdf/'

# Add a User-Agent header to pretend we are a normal Chrome browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Scraping {base_url} for PDF links...\n")
# Pass the headers to the initial request
response = requests.get(base_url, headers=headers)

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(response.content, 'html5lib')

# Find all anchor tags (<a>) that have an 'href' ending in '.pdf'
pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.pdf'):
        full_url = urljoin(base_url, href)
        pdf_links.append(full_url)

if not pdf_links:
    print("No PDF links found on this page.")
    exit()

print(f"Found {len(pdf_links)} PDFs. Starting download...\n")

# Loop through all the links and download them one by one
for pdf_url in pdf_links:
    filename = os.path.basename(pdf_url)
    print(f"Downloading: {filename}...")
    
    try:
        # Pass headers here as well, and increase the timeout
        pdf_response = requests.get(pdf_url, headers=headers, timeout=15)
        
        # Check if the download was successful
        if pdf_response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)
            print(f"  -> Saved successfully!")
        else:
            print(f"  -> Failed. Status code: {pdf_response.status_code}")
            
    except Exception as e:
        # If it crashes, print the error but continue to the next file
        print(f"  -> Error downloading this file: {e}")
        
    # Wait 2 seconds between downloads to be polite to the server
    time.sleep(2)

print("\nProcess finished!")
