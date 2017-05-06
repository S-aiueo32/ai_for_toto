import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

import csv
import os
import urllib2
from bs4 import BeautifulSoup

years = range(1992,2018)
ids = range(1,4)

for id in ids:
	for year in years:
		html = urllib2.urlopen("https://data.j-league.or.jp/SFMS01/search?competition_years=" + str(year) + "&competition_frame_ids=" + str(id) + "&tv_relay_station_name=")
		bsObj = BeautifulSoup(html, "html.parser")
		try:
			table = bsObj.findAll("table",{"class":"search-table"})[0]
			rows = table.findAll("tr")

			try:
				os.mkdir("../data")
			except WindowsError:
				pass
			try:
				os.mkdir("../data/raw")
			except WindowsError:
				pass
			try:
				os.mkdir("../data/raw/J" + str(id))
			except WindowsError:
				pass

			csvFile = open("../data/raw/J" + str(id) + "/J" + str(id) + "_"+str(year)+".csv", "wb")
			writer = csv.writer(csvFile)

			try:
				for row in rows:
					csvRow = []
					csvRowText = []
					for cell in row.findAll(['td', 'th']):
						try:
							tmp = cell.get_text().encode('shift_jis').strip()
							csvRowText.append(tmp)
						except UnicodeEncodeError:
							csvRowText.append("")
					writer.writerow(csvRowText)
			finally:
				csvFile.close()
		except IndexError:
			pass
