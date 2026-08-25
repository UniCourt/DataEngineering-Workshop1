import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

url = "https://sample-files.com/documents/pdf/"

# Create a session
session = requests.Session()

# Use a browser-like User-Agent
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36"
})

# Retry connection errors
retry = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

session.mount("https://", HTTPAdapter(max_retries=retry))


# Get the webpage
res = session.get(url, timeout=30)
res.raise_for_status()

# Parse the webpage
soup = BeautifulSoup(res.content, "html.parser")

# Directory where the Python file is located
directory = os.path.dirname(os.path.abspath(__file__))

# Find all PDF links
links = soup.select('a[href$=".pdf"]')

# Keep track of downloaded URLs
downloaded = set()

for link in links:

    pdf_url = urljoin(url, link["href"])

    # Skip duplicate links
    if pdf_url in downloaded:
        continue

    downloaded.add(pdf_url)

    # Get filename
    file_name = os.path.basename(pdf_url).split("?")[0]

    file_path = os.path.join(directory, file_name)

    print("Downloading:", pdf_url)

    try:
        # Download PDF
        pdf = session.get(
            pdf_url,
            stream=True,
            timeout=60
        )

        pdf.raise_for_status()

        # Save PDF
        with open(file_path, "wb") as f:
            for chunk in pdf.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("Saved:", file_path)
        print("-" * 50)

    except requests.exceptions.RequestException as e:
        print("FAILED:", pdf_url)
        print("ERROR:", e)
        print("-" * 50)

print("Finished!")
print("PDF links found:", len(downloaded))
