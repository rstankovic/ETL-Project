from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome',**executable_path, headless = False)

def scrape_f1():
    browser = init_browser()

    url = 'https://www.formula1.com/en/results.html/2020/races.html'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html,'html.parser')

    top_row = soup.find('div',class_='resultsarchive-filter-container')
    year_ul = top_row.find('div',class_='resultsarchive-filter-wrap')
    year_ul = year_ul.find_all('ul')[0]
    years_list = year_ul.find_all('a')
    return years_list

def iterate_f1(years_list):
    year_data = {}

    for year in years_list:
        url = 'https://formula1.com' + year.get('href')

        year_data[year.find('span').get_text()] = pd.read_html(url)

    return year_data

def scrape():
    year_data = iterate_f1(scrape_f1())
    return year_data