#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

urls = []
hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
for i in range(1,1000):
	urls.append("http://www.dnaindia.com/scitech?page=" + str(i))

columns = ['Heading', 'Link', 'Summary']
csv_file=open('Dna_SciTech[Jan7].csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

for url in urls: 
	print url
        try: 
		req = urllib2.Request(url,headers= hdr)
		page = urllib2.urlopen(req)
	except urllib2.URLError:
		print 'Error in URL ' + url
	soup = BeautifulSoup(page, 'html.parser') 
	contents = soup.find('div', attrs = {'class':'media-list '})
	a = contents.findAll('div',attrs = {'class':'media'})
	#print contents.prettify()
	lobbying = {}
	for ele in a:
		try:
			lst = ele.find('div',attrs = {'class' : 'media-body'})
			heading_link = ele.find('h3') 
			heading = heading_link.text.strip().encode('utf-8')
			lobbying[heading] = {}
			#print heading
	   		lobbying[heading]['Link'] = 'http://www.dnaindia.com' + ele.a['href']
		        #print lobbying[heading]['Link']
			req = urllib2.Request(lobbying[heading]['Link'],headers= hdr)
			page = urllib2.urlopen(req)
			soup = BeautifulSoup(page, 'html.parser') 
	 		article_content = soup.find('div', attrs = {'class' : 'body-text'})
		        lobbying[heading]['Summary'] = article_content.p.get_text().encode("utf-8")
		except urllib2.URLError:
			print 'Error in URL'
			del lobbying[heading]
			continue
		except AttributeError:
			print 'Error while extracting attributes'
			del lobbying[heading]
			continue
		#print(ele.prettify()) 
  
	for item in lobbying:         
	     	 writer.writerow([item,lobbying[item]['Link'], lobbying[item]['Summary']])	
