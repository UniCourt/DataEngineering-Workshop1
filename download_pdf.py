import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

page_url = "https://sample-files.com/documents/pdf/"

response = requests.get(
    page_url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
soup = BeautifulSoup(response.content, "html.parser")

# Find the first Download link
for link in soup.find_all("a"):
    if link.text.strip() == "Download":
        pdf_url = urljoin(page_url, link.get("href"))
        print("PDF URL:", pdf_url)

        # Download the PDF
        pdf_response = requests.get(
            pdf_url,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            timeout=30
        )

        pdf_response.raise_for_status()

        with open("sample.pdf", "wb") as file:
            for chunk in pdf_response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

        print("PDF downloaded successfully!")
        break
from pypdf import PdfReader

reader = PdfReader("sample.pdf")

print("\n===== PDF CONTENT =====\n")

for page in reader.pages:
    print(page.extract_text())
