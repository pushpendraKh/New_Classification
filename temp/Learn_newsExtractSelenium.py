#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
browser = webdriver.Firefox()
browser.get("http://timesofindia.indiatimes.com/home/science")
a = browser.find_element_by_id('fstc')
print a[0]
driver.close()
