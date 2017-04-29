import csv
import urllib2
import codecs
from bs4 import BeautifulSoup

html = urllib2.urlopen("https://data.j-league.or.jp/SFMS01/search?competition_years=2015&competition_frame_ids=1&tv_relay_station_name=")
soup = BeautifulSoup(html, "html.parser")
#print type(soup)

links = soup.tr.find_all('td')
f = codecs.open('test.txt','w','utf-8')
for link in links:
    #print(link)
    f.write(link.prettify() + '\n')
f.close()
print links
#print links[1].text
#print type(links[1].string)
#print links[1].string

#tbody = soup.find
#trs = soup.tbody.find_all("tr")
#for tr in trs
#    print tr

#td = soup.tbody.tr.find_all("td")
#td = tr.find_all("td")
#print type(tr)

#print tr[1]
#print type(tr[1])
