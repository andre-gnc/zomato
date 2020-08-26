import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


def make_driver_chrome(mdc_url):
    mdc_driver = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'))
    mdc_driver.get(mdc_url)
    return mdc_driver


urls = ['https://www.zomato.com/melbourne/restaurants/yum-cha',
        'https://www.zomato.com/melbourne/restaurants/vietnamese',
        'https://www.zomato.com/melbourne/restaurants/vegetarian',
        'https://www.zomato.com/melbourne/restaurants/vegan',
        'https://www.zomato.com/melbourne/restaurants/thai',
        'https://www.zomato.com/melbourne/restaurants/steak',
        'https://www.zomato.com/melbourne/restaurants/spanish',
        'https://www.zomato.com/melbourne/restaurants/sea-food',
        'https://www.zomato.com/melbourne/restaurants/pizza',
        'https://www.zomato.com/melbourne/restaurants?dishv2_id=105689',
        'https://www.zomato.com/melbourne/restaurants?dishv2_id=178815',
        'https://www.zomato.com/melbourne/restaurants/mexican',
        'https://www.zomato.com/melbourne/restaurants/lebanese',
        'https://www.zomato.com/melbourne/restaurants/korean',
        'https://www.zomato.com/melbourne/restaurants/japanese',
        'https://www.zomato.com/melbourne/restaurants/indian',
        'https://www.zomato.com/melbourne/restaurants/italian',
        'https://www.zomato.com/melbourne/restaurants/greek',
        'https://www.zomato.com/melbourne/restaurants/french',
        'https://www.zomato.com/melbourne/restaurants/dumplings',
        'https://www.zomato.com/melbourne/restaurants/chinese?page=41',
        'https://www.zomato.com/melbourne/restaurants/chinese?from_query=chinese+restaurants',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=251',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=201',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=151',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=101',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=71',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=61',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=51',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=41',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=31',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=21',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6&page=11',
        'https://www.zomato.com/melbourne/caf%C3%A9?category=6',
        'https://www.zomato.com/melbourne/caf%C3%A9',
        'https://www.zomato.com/melbourne/restaurants/chinese']

STATE = 'Victoria'
POSTCODE = ''
MOBILE = ''
FAX = ''
EMAIL = ''
WEBSITE = ''

SLEEP = 2

test_page = 'full'
page_test = 72
test_url = 'yes'
item_no = 0
item_dict = {}

url_no = 0

for url in urls:
    url_no += 1
    page = 1
    while True:
        driver = make_driver_chrome(url)

        driver.minimize_window()

        try:
            title_search = driver.find_element_by_xpath('/html/body/section/div/div[2]/div[1]/div[1]/h1').text
        except NoSuchElementException:
            print('The internet maybe down.')
            print('Last url scraped: ' + url)
            driver.quit()
            break

        list_search = driver.find_element_by_xpath('/html/body/section/div/div[2]/div[3]/div[2]/div/div[6]/div/div['
                                                   '1]/section/div[1]/div[3]')
        items = list_search.find_elements_by_css_selector('div.card.search-snippet-card')
        for counter, item in enumerate(items, 1):
            # Monitor its progress.
            print(url_no, ': ', page, ': ', counter)

            cuisines = item.find_element_by_css_selector('span.col-s-11').text
            organization = item.find_element_by_css_selector('a.result-title').text
            address_full = item.find_element_by_css_selector('div.col-m-16').text
            position_coma_last = address_full.rfind(',')
            position_coma_2nd_last = address_full.rfind(',', 0, position_coma_last)
            address = address_full[:position_coma_2nd_last]
            location = item.find_element_by_css_selector('a.ln24.search-page-text').text
            # location = address_full[position_coma_2nd_last + 2:position_coma_last]
            phone = item.find_element_by_css_selector('a.item').get_attribute('data-phone-no-str')
            profile = item.find_element_by_css_selector('a.result-title').get_attribute('href')

            item_no += 1
            item_dict[item_no] = [title_search, cuisines, organization, address, location, STATE, POSTCODE, phone,
                                  MOBILE, FAX, EMAIL, WEBSITE, profile]

        page += 1

        time.sleep(SLEEP)

        try:
            url = driver.find_element_by_css_selector('a.paginator_item.next.item').get_attribute('href')
        except NoSuchElementException:
            print('Last page. It\'s finished')
            driver.quit()
            break

        driver.quit()

        if page == page_test + 1 and test_page == 'yes':
            print(url)
            break
    if test_url == 'yes':
        break
    # break
df_items = pd.DataFrame.from_dict(item_dict, orient='Index', columns=['Title', 'Cuisines', 'Organization',
                                                                      'Address', 'Location', 'State', 'Postcode',
                                                                      'Phone', 'Mobile', 'Fax', 'Email', 'Website',
                                                                      'Profile'])
df_items.to_excel('data.xlsx')
# df_items.to_csv('data.csv')
