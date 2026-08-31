import requests
from bs4 import BeautifulSoup
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}


url = "https://www.courtlistener.com/"
params = {
    "q": "john",
    "type": "o",
}

res = requests.get(url, headers=headers, params=params)
res.raise_for_status()
soup = BeautifulSoup(res.content, "html5lib")

cases = []

for h3 in soup.find_all("h3"):
    link = h3.find("a")
    if not link:
        continue

    case_name_full = link.get_text(strip=True)
    case_url = link.get("href")

    if not case_url or "/opinion/" not in case_url:
        continue

    court_match = re.search(r"\(([^)]+)\)\s*$", case_name_full)
    court_year = court_match.group(1) if court_match else None
    case_name = re.sub(r"\s*\([^)]+\)\s*$", "", case_name_full)

    detail_text = ""
    next_el = h3.find_next_sibling()
    if next_el:
        detail_text = next_el.get_text(" ", strip=True)

    date_filed_match = re.search(r"Date Filed:\s*([A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?,\s*\d{4})", detail_text)
    status_match = re.search(r"Status:\s*(\w+)", detail_text)
    docket_match = re.search(r"Docket Number:\s*([^\n]+?)(?:\s{2,}|$)", detail_text)


    cases.append({
        "case_name": case_name,
        "court_year": court_year,
        "date_filed": date_filed_match.group(1) if date_filed_match else None,
        "status": status_match.group(1) if status_match else None,
        "docket_number": docket_match.group(1).strip() if docket_match else None,
        "url": "https://www.courtlistener.com" + case_url if case_url.startswith("/") else case_url,
    })

print(f"Found {len(cases)} total cases on this page\n")

john_cases = [c for c in cases if re.search(r"\bjohn\b", c["case_name"], re.IGNORECASE)]

print(f"Found {len(john_cases)} cases with 'John' in the name\n")
for c in john_cases:
    print(json.dumps(c, indent=2))
    print("-" * 80)

