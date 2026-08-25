xximport requests
from bs4 import BeautifulSoup
import os
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://sample-files.com/documents/pdf/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

try:
    response = requests.get(
        url,
        headers=headers,
        timeout=30,
        verify=False
    )
	
    soup = BeautifulSoup(response.content, "html.parser")

    # Create downloads folder
    os.makedirs("downloads", exist_ok=True)

    pdf_links = []

    # Find all PDF links
    for link in soup.find_all("a", href=True):
        href = link["href"]

        if ".pdf" in href.lower():

            if href.startswith("http"):
                pdf_url = href
            else:
                pdf_url = "https://sample-files.com" + href

            if pdf_url not in pdf_links:
                pdf_links.append(pdf_url)

    print(f"\nFound {len(pdf_links)} PDFs\n")

    for i, pdf_url in enumerate(pdf_links, start=1):

        try:
            print(f"Downloading PDF {i}: {pdf_url}")

            pdf_response = requests.get(
                pdf_url,
                headers=headers,
                timeout=60,
                verify=False
            )

            filename = f"downloads/sample_{i}.pdf"

            with open(filename, "wb") as f:
                f.write(pdf_response.content)

            print(f"Saved: {filename}\n")

        except Exception as e:
            print(f"Failed to download: {pdf_url}")
            print(f"Error: {e}\n")

    print("All possible PDFs processed.")

except Exception as e:
    print("Error accessing website:")
    print(e)
