import csv
import urllib2
from bs4 import BeautifulSoup


html = urllib2.urlopen("https://www.oreilly.co.jp/ebook/")
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.findAll("table",{"class":"tablesorter"})[0]
rows = table.findAll("tr")

csvFile = open("ebooks.csv", 'wt')
writer = csv.writer(csvFile)

try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
