import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://blog.python.org/')
bs = BeautifulSoup(html, 'html.parser')
table = bs.find('table',class_='entry-title')
rows = table.findAll('tr')
csvFile = open('Text-Editor-Data.csv', 'wt+')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
            writer.writerow(csvRow)
finally:
    csvFile.close()
