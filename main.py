import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


def make_soup(ms_url):
    # Make soups of each url.
    response = requests.get(ms_url)
    data = response.text
    ms_soup = BeautifulSoup(data, 'html.parser')
    return ms_soup


def make_driver_chrome(mdc_url):
    mdc_driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'))
    mdc_driver.get(mdc_url)
    return mdc_driver


urls = ['https://www.zomato.com/melbourne/caf%C3%A9',
        'https://www.zomato.com/melbourne/restaurants/chinese']

item_no = 0
item_dict = {}

for url in urls:
    page = 1
    while True:
        driver = make_driver_chrome(url)

        title_search = driver.find_element_by_xpath('/html/body/section/div/div[2]/div[1]/div[1]/h1').text

        list_search = driver.find_element_by_xpath('/html/body/section/div/div[2]/div[3]/div[2]/div/div[6]/div/div['
                                                   '1]/section/div[1]/div[3]')
        items = list_search.find_elements_by_css_selector('div.card.search-snippet-card')
        for counter, item in enumerate(items, 1):
            # Monitor its progress.
            print(page, ': ', counter)

            cuisines = item.find_element_by_css_selector('span.col-s-11').text
            organization = item.find_element_by_css_selector('a.result-title').text
            address_full = item.find_element_by_css_selector('div.col-m-16').text
            position_coma_last = address_full.rfind(',')
            position_coma_2nd_last = address_full.rfind(',', 0, position_coma_last)
            address = address_full[:position_coma_2nd_last]
            location = address_full[position_coma_2nd_last + 2:position_coma_last]
            phone = item.find_element_by_css_selector('a.item').get_attribute('data-phone-no-str')

            item_no += 1
            item_dict[item_no] = [title_search, cuisines, organization, address, location, phone]

            print(
                title_search + '\n' + cuisines + '\n' + organization + '\n' + address + '\n' + location + '\n' + phone +
                '\n')
            # break
        page += 1
        time.sleep(10)
        try:
            url = driver.find_element_by_xpath('/html/body/section/div/div[2]/div[3]/div[2]/div/div[6]/div/div['
                                               '1]/section/div[2]/div[1]/div[2]/div/div/a[7]').get_attribute('href')
        except NoSuchElementException:
            break
        driver.quit()
        if page == 3:
            break
    break
df_items = pd.DataFrame.from_dict(item_dict, orient='Index', columns=['Title', 'Cuisines', 'Organization',
                                                                      'Address', 'Location', 'Phone'])
df_items.to_excel('data.xlsx')
# df_items.to_csv('data.csv')
