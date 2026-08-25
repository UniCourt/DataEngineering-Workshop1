from pypdf import PdfReader

pdf_path = "/mnt/c/Users/shubh/Downloads/sample-pdf-a4-size-65kb.pdf"

reader = PdfReader(pdf_path)

print("Total pages:", len(reader.pages))

for page_number, page in enumerate(reader.pages, start=1):
    print(f"\n===== PAGE {page_number} =====\n")
    print(page.extract_text())
