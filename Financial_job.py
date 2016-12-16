#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = []
for i in range(1,91):
	urls.append('http://www.financialexpress.com/jobs/page/' + str(i) + '/')

columns = ['Heading', 'Summary', 'Link', 'PostedBy','PostedOnDate']
csv_file=open('Financial_Job[Dec16].csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
	try:
		page = urllib2.urlopen(url)
	except urllib2.URLError:
		print 'Error in URL ' + url
		continue
	soup = BeautifulSoup(page, 'html.parser') 
	print url
	contents = soup.find('div', attrs = {'class':'listing'})
	#print contents
	a = contents.find('ul')
	lobbying = {}
	for li in a.find_all('li'):
	 	try:
			heading_l = li.find('h5') 
			heading = str(heading_l.text.strip().encode("utf-8"))
			lobbying[heading] = {}
		
			lobbying[heading]['Link'] = li.a['href']
	
			date_l = li.find('em', attrs={'class': 'fe-list-byline'}) 
			date = date_l.text.strip()
			d = date.split('|');
			if date.find('|') != -1:
				lobbying[heading]['PostedBy'] = str(d[0].encode("utf-8"))
				lobbying[heading]['PostedOnDate'] = str(d[1].encode("utf-8"))
			else:
				lobbying[heading]['PostedBy'] = 'NA'
				lobbying[heading]['PostedOnDate'] = date

			lobbying[heading]['Summary'] = str(li.p.get_text().encode("utf-8"))
		except AttributeError:
			print 'Error in Attributes'
			del lobbying[heading]
			continue


	# Storing data in Industry.csv file
	for item in lobbying:         
	      	 writer.writerow([item,lobbying[item]['Summary'],lobbying[item]['Link'],lobbying[item]['PostedBy'],lobbying[item]['PostedOnDate']])
	 
		
		
