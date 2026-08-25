import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://sample-files.com/documents/pdf/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36"
}


response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

if not table:
    print("No table found")
    exit()
rows = table.find_all("tr")


for row in rows:

    columns = row.find_all("td")

    if len(columns) >= 6:
        sixth_column = columns[5]

 
        pdf_link = sixth_column.find("a", href=True)

        if pdf_link:

            pdf_url = urljoin(url, pdf_link["href"])

            print("PDF found:", pdf_url)
