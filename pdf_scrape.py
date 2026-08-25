from pypdf import PdfReader

pdf_path = "/home/ankitha/Downloads/basic-text.pdf"

reader = PdfReader(pdf_path)

for page in reader.pages:
    text = page.extract_text()
    print(text)
