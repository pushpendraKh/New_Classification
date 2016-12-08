#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = []
for i in range(1,20):
	urls.append('http://www.financialexpress.com/industry/page/' + str(i) + '/')

columns = ['Heading', 'Summary', 'Link', 'PostedBy','PostedOnDate']
csv_file=open('Industry_temp.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser') 
	contents = soup.find('div', attrs = {'class':'listing'})
	a = contents.find('ul')
	lobbying = {}
	for li in a.findAll('li'):
	 	
		heading_l = li.find('h5') 
		heading = heading_l.text.strip()
		lobbying[heading] = {}
		
		lobbying[heading]['link'] = li.a['href']
	
		date_l = li.find('em', attrs={'class': 'fe-list-byline'}) 
		date = date_l.text.strip()
		d = date.split('|');
		if date.find('|') != -1:
			lobbying[heading]['postedBy'] =d[0]
			lobbying[heading]['postedOnDate'] = d[1]
		else:
			lobbying[heading]['postedBy'] = 'NA'
			lobbying[heading]['postedOnDate'] = date

		lobbying[heading]['summary'] = li.p.get_text()

	# Storing data in Industry.csv file
	for item in lobbying:         
	      	 writer.writerow([str(item.encode("utf-8")),str(lobbying[item]['summary'].encode("utf-8")),lobbying[item]['link'],lobbying[item]['postedBy'],lobbying[item]['postedOnDate']])
	 
		
		
