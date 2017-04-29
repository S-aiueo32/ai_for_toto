import csv
import urllib2
from bs4 import BeautifulSoup

for year in range(2014,2017):
	html = urllib2.urlopen("https://data.j-league.or.jp/SFMS01/search?competition_years=" + str(year) + "&competition_frame_ids=3&tv_relay_station_name=")

	bsObj = BeautifulSoup(html, "html.parser")
	table = bsObj.findAll("table",{"class":"search-table"})[0]
	rows = table.findAll("tr")

	csvFile = open("./Data/J3/J3_"+str(year)+".csv", 'wb')
	writer = csv.writer(csvFile)

	try:
		for row in rows:
			csvRow = []
			for cell in row.findAll(['td', 'th']):
				csvRow.append(cell.get_text())
			writer.writerow(csvRow)
	finally:
		csvFile.close()
