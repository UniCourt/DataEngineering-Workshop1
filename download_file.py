import requests

# The direct URL to the sample PDF file
pdf_url = "https://sample-files.com/downloads/documents/pdf/sample-pdf-a4-size-65kb.pdf"

print("Downloading the file...")
response = requests.get(pdf_url)

# Save the binary content directly to your workshop folder
with open("sample_downloaded.pdf", "wb") as f:
    f.write(response.content)

print("Download complete! File saved to your workspace.")