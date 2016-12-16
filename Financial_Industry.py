#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = []
for i in range(1,300):
	urls.append('http://www.financialexpress.com/industry/page/' + str(i) + '/')

columns = ['Heading', 'Summary', 'Link', 'PostedBy','PostedOnDate']
csv_file=open('Financial_Industry[Dec16].csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
	try:
		page = urllib2.urlopen(url)
	except urllib2.URLError:
		print 'Error in URL ' + url
		continue
	soup = BeautifulSoup(page, 'html.parser') 
	contents = soup.find('div', attrs = {'class':'listing'})
	a = contents.find('ul')
	lobbying = {}
	for li in a.find_all('li'):
	 	try:
			heading_l = li.find('h5') 
			heading = heading_l.text.strip()
			lobbying[heading] = {}
		
			lobbying[heading]['Link'] = li.a['href']
	
			date_l = li.find('em', attrs={'class': 'fe-list-byline'}) 
			date = date_l.text.strip()
			d = date.split('|');
			if date.find('|') != -1:
				lobbying[heading]['PostedBy'] =d[0]
				lobbying[heading]['PostedOnDate'] = d[1]
			else:
				lobbying[heading]['PostedBy'] = 'NA'
				lobbying[heading]['PostedOnDate'] = date

			lobbying[heading]['Summary'] = li.p.get_text()
		except AttributeError:
			print 'Error in Attributes'
			del lobbying[heading]
			continue


	# Storing data in Industry.csv file
	for item in lobbying:         
	      	 writer.writerow([str(item.encode("utf-8")),str(lobbying[item]['Summary'].encode("utf-8")),lobbying[item]['Link'],lobbying[item]['PostedBy'],lobbying[item]['PostedOnDate']])
	 
		
		
