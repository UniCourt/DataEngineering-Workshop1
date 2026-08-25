import urllib.request
from bs4 import BeautifulSoup
import io
import pypdf
import os

BASE_URL = \x27https://sample-files.com\x27
CATALOG_URL = f\x27{BASE_URL}/documents/pdf/\x27

def fetch_url(url):
    req = urllib.request.Request(url, headers={\x27User-Agent\x27: \x27Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\x27})
    with urllib.request.urlopen(req) as resp:
        return resp.read()

print(f\x221. Crawling catalog page: {CATALOG_URL}\x22)
html_content = fetch_url(CATALOG_URL)
soup = BeautifulSoup(html_content, \x27html.parser\x27)

all_download_items = []
table = soup.find(\x27figure\x27, class_=\x27wp-block-table\x27)

if table:
    rows = table.find_all(\x27tr\x27)
    for row in rows:
        cols = row.find_all(\x27td\x27)
        link_tag = row.find(\x27a\x27, href=True)
        if cols and link_tag:
            doc_name = cols[0].get_text(strip=True)
            doc_size = cols[1].get_text(strip=True) if len(cols) > 1 else \x27Unknown\x27
            relative_link = link_tag[\x27href\x27]
            full_link = f\x22{BASE_URL}{relative_link}\x22 if relative_link.startswith(\x27/\x27) else relative_link
            filename = relative_link.split(\x27/\x27)[-1]
            all_download_items.append({
                \x27name\x27: doc_name,
                \x27size\x27: doc_size,
                \x27url\x27: full_link,
                \x27filename\x27: filename
            })

print(f\x22   -> Discovered {len(all_download_items)} PDF files in catalog!\n\x22)

with open(\x27all_pdf_links.txt\x27, \x27w\x27, encoding=\x27utf-8\x27) as f:
    f.write(f\x22Total PDF Files Cataloged: {len(all_download_items)}\n\x22)
    f.write(\x22=\x22 * 70 + \x22\n\n\x22)
    for idx, item in enumerate(all_download_items, start=1):
        f.write(f\x22#{idx} Name: {item[\x27name\x27]}\n\x22)
        f.write(f\x22   Size: {item[\x27size\x27]}\n\x22)
        f.write(f\x22   URL:  {item[\x27url\x27]}\n\x22)
        f.write(\x22-\x22 * 70 + \x22\n\x22)

print(\x222. Saved catalog manifest to \x27all_pdf_links.txt\x27!\x22)

os.makedirs(\x27downloaded_pdfs\x27, exist_ok=True)
os.makedirs(\x27extracted_texts\x27, exist_ok=True)

print(\x22\n3. Downloading PDFs and extracting plain text...\x22)
for idx, item in enumerate(all_download_items[:5], start=1):
    print(f\x22   [{idx}/5] Processing: {item[\x27name\x27]} ({item[\x27filename\x27]})...\x22)
    try:
        pdf_bytes = fetch_url(item[\x27url\x27])
        pdf_save_path = os.path.join(\x27downloaded_pdfs\x27, item[\x27filename\x27])
        with open(pdf_save_path, \x27wb\x27) as f:
            f.write(pdf_bytes)
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        full_text = \x27\n\x27.join([page.extract_text() for page in reader.pages])
        txt_filename = item[\x27filename\x27].replace(\x27.pdf\x27, \x27.txt\x27)
        txt_save_path = os.path.join(\x27extracted_texts\x27, txt_filename)
        with open(txt_save_path, \x27w\x27, encoding=\x27utf-8\x27) as f:
            f.write(full_text)
        print(f\x22      -> Saved PDF to:  \x27{pdf_save_path}\x27\x22)
        print(f\x22      -> Saved Text to: \x27{txt_save_path}\x27\x22)
    except Exception as e:
        print(f\x22      -> Error processing {item[\x27filename\x27]}: {e}\x22)

print(\x22\n4. Complete! All catalog links and extracted text files are ready in your workspace.\x22)
