import csv
import urllib2
from bs4 import BeautifulSoup


html = urllib2.urlopen("https://data.j-league.or.jp/SFMS01/search?competition_years=2015&competition_frame_ids=1&tv_relay_station_name=")
bsObj = BeautifulSoup(html, "html.parser")

table = bsObj.findAll("table",{"class":"search-table"})[0]
rows = table.findAll("tr")

csvFile = open("ebooks.csv", 'wb')
writer = csv.writer(csvFile)

try:
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()
