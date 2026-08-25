from bs4 import BeautifulSoup

html = """
<html>
<head>
<title>Beautiful Soup Example</title>
</head>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

print(soup.title)
