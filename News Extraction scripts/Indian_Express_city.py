#!usr/bin/python
import urllib2  
from bs4 import BeautifulSoup 
import csv
import sys

main_url = 'http://indianexpress.com/cities/'
#hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

columns = ['City','Heading', 'Link', 'Summary', 'Date']
csv_file=open('Ind_cities.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(columns)

#page = urllib2.urlopen(req)
#for url in urls:
try: 
	main_req = urllib2.Request(main_url)
	main_page = urllib2.urlopen(main_req)
except urllib2.URLError:
	print 'Error in url ' + main_url
	sys.exit()
main_soup = BeautifulSoup(main_page, 'html.parser') 
contents = main_soup.find('div', attrs = {'class':'equal-columns'})
sections = contents.findAll('div',attrs = {'class' : 'sections'})

#Stories on Page
stories = main_soup.findAll('div',attrs = {'class':'stories'})
lobbying = {}
for one in stories:
	try:
		heading_link = one.find('h6')
		heading = str(heading_link.text.strip().encode("utf-8"))
		lobbying[heading] = {}
		lobbying[heading]['City'] = "a"
		lobbying[heading]['Link'] = one.a['href']
		story_page = urllib2.urlopen(lobbying[heading]['Link'])
		story_soup = BeautifulSoup(story_page, 'html.parser') 
		lobbying[heading]['Summary'] = str(story_soup.find('h2',attrs = {'class' :'synopsis'}).text.strip().encode("utf-8"))
   	except AttributeError:
		print 'Error in Attributes'
		del lobbying[heading];
		continue
for item in lobbying:         
	writer.writerow([lobbying[item]['City'],item,lobbying[item]['Link'], lobbying[item]['Summary']])

# Lead Stories		
lead_stories = main_soup.findAll('div',attrs = {'class':'lead-story'})
lobbying = {}
for one in lead_stories:
	try:
		heading_link = one.find('h5')
		heading = str(heading_link.text.strip().encode("utf-8"))
		lobbying[heading] = {}
		lobbying[heading]['City'] = "a"
		lobbying[heading]['Link'] = one.a['href']
		lobbying[heading]['Summary'] = str(one.p.get_text().encode("utf-8"))
   	except AttributeError:
		print 'Error in Lead stories'
		del lobbying[heading]
		continue
for item in lobbying:         
	writer.writerow([lobbying[item]['City'],item,lobbying[item]['Link'], lobbying[item]['Summary']])

# For each City
for each_section in sections:
	try:
		city_link = each_section.find('h4') 
		city_name = str(city_link.text.strip().encode("utf-8"))
		print city_name
		
		# Step1 - Extract current news from city page
	    	city_main_url = 'http://indianexpress.com' + each_section.a['href']
		try:
			city_page = urllib2.urlopen(city_main_url)
		except urllib2.URLError:
			print 'Error opening url ' + city_main_url
			continue
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
				lobbying[heading]['Link'] = city_story.a['href']
				lobbying[heading]['Summary'] = str(city_story.p.get_text().encode("utf-8")) 
			except AttributeError:
				print 'Error occured in extracting news'
				del lobbying[heading]
	       			continue 
		for item in lobbying:         
	     		writer.writerow([lobbying[item]['City'],item,lobbying[item]['Link'], lobbying[item]['Summary']])
		
		#Step2 - Extract past news from city page
		city_urls = []
		for i in range(2,50):
			city_urls.append(city_main_url + 'page/' + str(i) + '/')
		for city_url in city_urls:
				print city_url
				try:
					city_page = urllib2.urlopen(city_url)
				except urllib2.URLError:
					print 'Error opening URL '+ city_url
					continue				
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
						lobbying[heading]['Link'] = city_story.a['href']
						lobbying[heading]['Summary'] = str(city_story.p.get_text().encode("utf-8"))
						lobbying[heading]['Date'] = str(city_story.find('div',attrs = {'class' : 'date'}).text.strip().encode("utf-8")) 
					except AttributeError:
						print 'Error occured in extracting news from' + city_url
						del lobbying[heading]
			       			continue 
				for item in lobbying:         
		      	 		writer.writerow([lobbying[item]['City'],item,lobbying[item]['Link'], lobbying[item]['Summary'],lobbying[item]['Date']]) 
		#print("------------------------------------")      
	except AttributeError:
		print 'Error occured while evaluating each city page'			
