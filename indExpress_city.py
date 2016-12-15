#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv

main_url = 'http://indianexpress.com/cities/'
#hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

columns = ['City','Heading', 'Link', 'Summary', 'Date']
csv_file=open('Ind_cities.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

#page = urllib2.urlopen(req)
#for url in urls: 
main_req = urllib2.Request(main_url)
main_page = urllib2.urlopen(main_req)
main_soup = BeautifulSoup(main_page, 'html.parser') 
contents = main_soup.find('div', attrs = {'class':'equal-columns'})
sections = contents.findAll('div',attrs = {'class' : 'sections'})
print 'Number of cities' + str(len(sections))

for each_section in sections:
	try:
		city_link = each_section.find('h4') 
		city_name = str(city_link.text.strip().encode("utf-8"))
		print city_name
		#preprocessing on each page before opening it
		
		# Step1 - Extract current news from city page
	    	city_main_url = 'http://indianexpress.com' + each_section.a['href']
		city_page = urllib2.urlopen(city_main_url)
		city_soup = BeautifulSoup(city_page, 'html.parser')
		city_contents = city_soup.find('div', attrs = {'class':'cities-stories'}) 
		city_stories = city_contents.findAll('div',attrs = {'class' : 'story'})
		lobbying = {}
		for city_story in city_stories:
			try:
				story_link = city_story.find('h6')
				heading = str(story_link.text.strip().encode("utf-8"))
				lobbying[heading] = {}			
				lobbying[heading]['City'] = city_name
				lobbying[heading]['link'] = city_story.a['href']
				lobbying[heading]['summary'] = str(city_story.p.get_text().encode("utf-8")) 
			except AttributeError:
				print 'Error occured in extracting news'
	       			continue 
		for item in lobbying:         
	     		writer.writerow([lobbying[item]['City'],item,lobbying[item]['link'], lobbying[item]['summary']])
		
		#Step2 - Extract past news from city page
		city_urls = []
		for i in range(2,50):
			city_urls.append(city_main_url + 'page/' + str(i) + '/')
		for city_url in city_urls:
			try:
				print city_url
				city_page = urllib2.urlopen(city_url)
				city_soup = BeautifulSoup(city_page, 'html.parser')
				city_contents = city_soup.find('div', attrs = {'class':'nation'}) 
				city_stories = city_contents.findAll('div',attrs = {'class' : 'articles'})
				#print len(city_stories)
				lobbying = {}
				for city_story in city_stories:
					try:
						story_link = city_story.find('div', attrs = {'class':'title'})
						heading = str(story_link.text.strip().encode("utf-8"))
						lobbying[heading] = {}			
						lobbying[heading]['City'] = city_name
						lobbying[heading]['link'] = city_story.a['href']
						lobbying[heading]['summary'] = str(city_story.p.get_text().encode("utf-8"))
						lobbying[heading]['Date'] = str(city_story.find('div',attrs = {'class' : 'date'}).text.strip().encode("utf-8")) 
					except AttributeError:
						print 'Error occured in extracting news from' + city_url
			       			continue 
				for item in lobbying:         
		      	 		writer.writerow([lobbying[item]['City'],item,lobbying[item]['link'], lobbying[item]['summary'],lobbying[item]['Date']])
			except AttributeError:
				print 'Error Occured in city_url' 
		#print("------------------------------------")      
	except AttributeError:
		print 'Error occured while evaluating each city page'			
