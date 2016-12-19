#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
urls = ['http://timesofindia.indiatimes.com/home/education/']
for i in range(2,11):
	urls.append('http://timesofindia.indiatimes.com/home/education/' + str(i))

columns = ['Heading', 'Link', 'Summary']
csv_file=open('Time_Education[Dec16].csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
	try:
		page = urllib2.urlopen(url)
	except urllib2.URLError:
		print 'Error in URL ' + lobbying[heading]['Link']
		continue
	soup = BeautifulSoup(page, 'html.parser') 
	contents = soup.find('div', attrs = {'class':'ct1stry'})
	a = contents.findAll('div',id = 'fsts')
	#print contents.prettify()
	lobbying = {}
	for ele in a:
		try:
			heading_link = ele.find('h2') 
			heading = heading_link.text.strip()
			lobbying[heading] = {}

	    		lobbying[heading]['Link'] = 'http://timesofindia.indiatimes.com' + ele.a['href']
			try:
				req = urllib2.Request(lobbying[heading]['Link'],headers= hdr)
				page = urllib2.urlopen(req)
			except urllib2.URLError:
				print 'Error in URL ' + lobbying[heading]['Link']
				del lobbying[heading] 
				continue
			soup = BeautifulSoup(page, 'html.parser') 
	 		article_content = soup.find('div', attrs = {'class' : 'Normal'})
		        rows = article_content.text.strip().encode("utf-8").split('\n')
			lobbying[heading]['Summary'] = rows[0] 
			#print("------------------------------------")
		except:
			print 'Error in stories'
			del lobbying[heading]
			continue
  
	for item in lobbying:         
	      	 writer.writerow([str(item.encode("utf-8")),lobbying[item]['Link'], lobbying[item]['Summary']])	
	

	
		







