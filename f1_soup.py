from bs4 import BeautifulSoup as bs 
from splinter import Browser
import time

def init_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome',**executable_path, headless = False)

browser = init_browser()

url = 'https://www.formula1.com/en/results.html/2019/races.html'
browser.visit(url)
time.sleep(1)

html = browser.html
soup = bs(html,'html.parser')

table = soup.find('table', {'class':'resultsarchive-table'})
for row in table.find_all('tr'):
    new_dict = {}
    list_columns = row.find_all('td')
    print(list_columns)
    new_dict['Grand Prix'] = list_columns[1].find('a').text
    print(new_dict['Grand Prix'])