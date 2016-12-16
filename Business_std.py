#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = []
for i in range(1,10000):
	urls.append('http://www.business-standard.com/category/pti-stories-national-13902.htm/' + str(i) + '/')

columns = ['Heading', 'Summary', 'Link','PostedOnDate']
csv_file=open('Business_std[Dec16].csv', 'w')
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
	a = soup.find('ul', attrs = {'class':'listing'})
	#print contents
	lobbying = {}
	for li in a.find_all('li'):
	 	try:
			lst = li.find('div',attrs = {'class' : 'listing-txt'})
			#print lst
			heading_l = lst.find('h2') 
			heading = str(heading_l.text.strip().encode("utf-8"))
			lobbying[heading] = {}
			lobbying[heading]['Link'] = li.a['href']
			paras = lst.find_all('p')
			date = str(paras[0].text.strip().encode("utf-8"))
			lobbying[heading]['PostedOnDate'] = date
			lobbying[heading]['Summary'] = str(paras[1].text.strip().encode("utf-8"))
		except AttributeError:
			print 'Error in Attributes'
			del lobbying[heading]
			continue


	# Storing data in Industry.csv file
	for item in lobbying:         
	      	 writer.writerow([item,lobbying[item]['Summary'],lobbying[item]['Link'],lobbying[item]['PostedOnDate']])
	 
		
		
