import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "http://sample-files.com/documents/pdf/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
download_dir = "downloaded_pdfs"
os.makedirs(download_dir, exist_ok=True)

# Use a Session for connection pooling & faster batch downloads
session = requests.Session()
session.headers.update(headers)
session.verify = False

print(f"Connecting to {base_url}...")
try:
    response = session.get(base_url, timeout=15)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")
    exit(1)

soup = BeautifulSoup(response.content, "html.parser")

# 1. Locate the table
table = soup.find("table")
pdf_links = []

if table:
    # Find the index of the "Download" header dynamically
    headers_list = [th.text.strip().lower() for th in table.find_all("th")]
    download_col_idx = headers_list.index("download") if "download" in headers_list else -1

    # 2. Iterate through table rows, skipping the header row
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols:
            # Grab the cell from the Download column (or fallback to the last column)
            target_cell = cols[download_col_idx] if download_col_idx < len(cols) else cols[-1]
            a_tag = target_cell.find("a", href=True)
            
            if a_tag and a_tag["href"].strip().lower().endswith(".pdf"):
                full_url = urljoin(base_url, a_tag["href"].strip())
                pdf_links.append(full_url)

pdf_links = list(set(pdf_links))
print(f"Found {len(pdf_links)} PDF links specifically in the Download column.\n")

# 3. Batch download using session
for i, pdf_url in enumerate(pdf_links, 1):
    filename = pdf_url.split("/")[-1]
    filepath = os.path.join(download_dir, filename)

    # takes the chunk of the pdf a
    print(f"[{i}/{len(pdf_links)}] Downloading {filename}...")
    try:
        with session.get(pdf_url, stream=True, timeout=15) as pdf_response:
            if pdf_response.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  Saved to: {filepath}")
            else:
                print(f"  Failed (Status Code: {pdf_response.status_code})")
    except Exception as e:
        print(f"  Error downloading file: {e}")

print("\nAll downloads completed!")