#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
from selenium import webdriver
import csv

urls = ['http://timesofindia.indiatimes.com/home/science/6']
for i in range(7,10):
	urls.append('http://timesofindia.indiatimes.com/home/science/' + str(i))

columns = ['Heading', 'Link', 'Summary']
csv_file=open('Sciencefrom6.csv', 'w')
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
		heading_link = ele.find('h2') 
		heading = heading_link.text.strip().encode('utf-8')
		lobbying[heading] = {}
		print heading
    		lobbying[heading]['link'] = 'http://timesofindia.indiatimes.com' + ele.a['href']
		
		page = urllib2.urlopen(lobbying[heading]['link'])
	        soup = BeautifulSoup(page, 'html.parser') 
 		article_content = soup.find('div', attrs = {'class' : 'Normal'})
                rows = (article_content.text.strip().encode("utf-8")).split('\n')
		lobbying[heading]['summary'] = rows[0]
		print("------------------------------------")
		#print(ele.prettify()) 
  
	for item in lobbying:         
	      	 writer.writerow([item,lobbying[item]['link'], lobbying[item]['summary']])	
	

	
		







