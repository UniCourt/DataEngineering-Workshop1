from pypdf import PdfReader

pdf_path = "sample-pdf.pdf"

reader = PdfReader(pdf_path)

for page in reader.pages:
    text = page.extract_text()
    lines = text.splitlines()

    for line in lines:
        if line in [
            "Sample Document for PDF Testing",
            "Introduction",
            "Text Formatting Examples",
            "Lists",
            "Quote",
            "Table"
        ]:
            print(line)

