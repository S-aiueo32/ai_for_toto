import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

import csv
import codecs
import urllib2
from bs4 import BeautifulSoup


years = range(1993,2018)
ids = range(1,4)

for id in ids:
	for year in years:
		html = urllib2.urlopen("https://data.j-league.or.jp/SFMS01/search?competition_years=" + str(year) + "&competition_frame_ids=" + str(id) + "&tv_relay_station_name=")
		bsObj = BeautifulSoup(html, "html.parser")
		try:
			table = bsObj.findAll("table",{"class":"search-table"})[0]
			rows = table.findAll("tr")

			#csvFile = codecs.open("./Data/J3/J3_"+str(year)+".csv", "wb", "shift_jis")
			csvFile = open("./Data/J" + str(id) + "/J" + str(id) + "_"+str(year)+".csv", "wb")
			writer = csv.writer(csvFile)

			try:
				for row in rows:
					csvRow = []
					csvRowText = []
					for cell in row.findAll(['td', 'th']):
						#print type(cell.get_text())
						#csvRow.append(cell.encode('shift_jis'))
						try:
							csvRowText.append(cell.get_text().encode('shift_jis'))
						except UnicodeEncodeError:
							pass
					writer.writerow(csvRowText)
			finally:
				csvFile.close()
		except IndexError:
			pass
