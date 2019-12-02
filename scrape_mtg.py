import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime


def today_date():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    today = f'{month}/{day}/{year}'
    return today


def scrape_magic():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://shop.tcgplayer.com/magic/product/show?_gl=1*1at1pyd*_gcl_aw*R0NMLjE1NjQ3NTUyODYuQ2owS0NRand2b19xQlJEUUFSSXNBRS1ic0gtMlk0UzB6VmZGUEFQLWU0RlU3bzFBczVFd0E5ODJfTzE4SE9ibG5WZ0NvcFRqZXdLWHlRZ2FBbF9hRUFMd193Y0I'
    browser.visit(url)

    #######################
    #    filter set-up    #
    #######################
    # select dropdown & sort option (high to low)
    browser.find_by_id('ProductSort').click()
    time.sleep(2)
    browser.find_by_value('MinPrice DESC').click()
    time.sleep(2)
    browser.find_by_text(' Filters').click()
    # select the filters: Listings with photos, Normal, Near Mint
    time.sleep(3)
    browser.click_link_by_partial_text('Listings With Photos')
    time.sleep(3)
    browser.click_link_by_partial_text('Normal')
    time.sleep(3)
    browser.click_link_by_partial_text('Near Mint')
    # navigate back to main page
    time.sleep(3)
    browser.find_by_text(' Filters').click()
    time.sleep(3)
    browser.find_by_text('Magic: The Gathering').click()
    browser.back()

    # may need to include a database check, maybe import and then do loop to check if item is in database already
    # if database becomes too big maybe include the db call in the loop and do one card at a time

    #########################
    #     Loop Set-up       #
    #########################
    card_list = []
    counter = 1
    end_loop = False
    # outer loop
    while end_loop == False:
        counter += 1
        html = browser.html
        soup = bs(html, "html.parser")
        current_cards = soup.find_all('div', class_='product')
        # inner loop
        for current_card in current_cards:
            card = {
                'card_name':'',
                'edition': {},
                'rarity': ''
            } 
            try:
                card['card_name'] = current_card\
                    .find('div', class_="product__details")\
                    .find('a', class_='product__name').text.strip()
                card['edition'][current_card\
                    .find('div', class_="product__details")\
                    .find('a', class_='product__group').text.strip()] = {
                    today_date(): current_card
                    .find('div', class_="product__details")
                    .find('dd').text.strip()[1:]
                }
                card['rarity'] = current_card\
                    .find('div', class_="product__details")\
                    .find('div', class_='product__extended-fields').text.strip()
                print(card)
            except:
                print("skipping product")
            if card['edition'][current_card\
                .find('div', class_="product__details")\
                .find('a', class_='product__group').text.strip()][today_date()] == 'navailable':
                print('if')
                break
            # if trouble shooting increase this value to 2000
            elif float(card['edition'][current_card\
                .find('div', class_="product__details")\
                .find('a', class_='product__group').text.strip()][today_date()]) < 10:
                print('elif')
                # variable in while loop that switches it so the outer loop ends
                end_loop = True
                break
            else:
                print(card)
                card_list.append(card)
        time.sleep(3)
        browser.click_link_by_text(str(counter))
    browser.quit()
    print(card_list)
    return card_list


# mongo layout
# {
#     'card_name': '',
#     'edition': {
#         'actual addition name': {
#             'price/time': {
#                 'actual date recorded': 'actual price'
#             }
#         }
#     },
#     'rarity': '',
# }
