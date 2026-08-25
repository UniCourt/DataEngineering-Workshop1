import pymupdf

pdf = pymupdf.open("/home/mithesh-r-shetty/DataEngineering-Workshop1/docs/sample-pdf-a4-size-65kb.pdf")

for page_number, page in enumerate(pdf, start=1):
    print(f"\n--- Page {page_number} ---")
    print(page.get_text())

pdf.close()