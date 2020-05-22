from bs4 import BeautifulSoup as bs 
from splinter import Browser
import time
import pymongo

def init_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome',**executable_path, headless = False)

################

browser = init_browser()
races = []
for year in range(1950,2020):

    url = f'https://www.formula1.com/en/results.html/{year}/races.html'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')
    table = soup.find('table', {'class':'resultsarchive-table'})

    for row in table.find_all('tr'):
        new_dict = {}
        race = [x.text for x in row.find_all('td')]

        if len(race) > 2:
            new_dict['Grand Prix'] = race[1].strip()
            new_dict['Date'] = race[2].strip()
            new_dict['Winner'] = ' '.join(race[3].split('\n')[1:3])
            new_dict['Car'] = race[4].strip()
            new_dict['Laps'] = race[5].strip()
            new_dict['Time'] = race[6].strip()
            new_dict['Year'] = year

        races.append(new_dict)

#################

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.f1_db

db.race_results.insert_many(races)

###################

results = db.race_results.find({'Year':1953})
for result in results:
    print(result)