from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import selenium.webdriver.support.expected_conditions as EC 
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pandas import DataFrame
import os 
import time


#creating some of the options for chrome 
scroll_height = 500
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors')#ignoring the ssl certificate
options.add_argument('--ignore-certificate-errors')#ignoring certificate
dir_path = os.path.dirname(os.path.realpath(__file__))
chrome_driver = os.path.join(dir_path , 'chromedriver')
driver = webdriver.Chrome(options=options)
url = 'YoutTubeVideoURL'
driver.get(url)
time.sleep(10)

#loading parent comments
for i in range(1,30):
	driver.execute_script(f'window.scrollTo(0,{scroll_height*i})')
	time.sleep(1)
driver.execute_script('window.scrollTo(0, 0 )')


#loading children comment
replies = driver.find_elements_by_xpath('//*[@icon="yt-icons:expand-more"]')
for reply in replies:
	ActionChains(driver).move_to_element_with_offset(reply, 0, 10).click().perform()
	time.sleep(3)


#parsing the page to BeautifulSoup
html = driver.page_source
soup = BeautifulSoup(html , 'html.parser')
comments = soup.find('ytd-comments' , {'id':'comments'})
base_url = 'https://www.youtube.com/'
names = []
links = []
users = comments.find_all('a' , {'class':'yt-simple-endpoint style-scope ytd-comment-renderer'})
driver.quit()
for user in users:
	if not(user.text in names):
		names.append(user.text)
		links.append(base_url + user['href'])

df = DataFrame(list(zip(names , links)))

df.to_excel('YouTube_comments.xlsx' , header=False)
