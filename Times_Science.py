#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = ['http://timesofindia.indiatimes.com/home/science/']
for i in range(2,11):
	urls.append('http://timesofindia.indiatimes.com/home/science/' + str(i))

columns = ['Heading', 'Link', 'Summary']
csv_file=open('Times_Science[Dec16].csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
        print url
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser') 
	contents = soup.find('div', attrs = {'class':'ct1stry'})
	a = contents.findAll('div',id = 'fsts')
	#print contents.prettify()
	lobbying = {}
	for ele in a:
		try:
			heading_link = ele.find('h2') 
			heading = heading_link.text.strip().encode('utf-8')
			lobbying[heading] = {}
			#print heading
	    		lobbying[heading]['Link'] = 'http://timesofindia.indiatimes.com' + ele.a['href']
		
			page = urllib2.urlopen(lobbying[heading]['Link'])
			soup = BeautifulSoup(page, 'html.parser') 
	 		article_content = soup.find('div', attrs = {'class' : 'Normal'})
		        rows = (article_content.text.strip().encode("utf-8")).split('\n')
			lobbying[heading]['Summary'] = rows[0]
		except urllib2.URLError:
			print 'Error in URL'
			del lobbying[heading]
			continue
		#print(ele.prettify()) 
  
	for item in lobbying:         
	      	 writer.writerow([item,lobbying[item]['Link'], lobbying[item]['Summary']])	
	

	
		







