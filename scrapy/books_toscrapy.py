# -*- coding: utf-8 -*-
import datetime
import json
import time
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from scrapy.util import wait_element


def get_page_data(driver):
    a_tags = driver.find_elements_by_xpath('//article/h3/a')
    dataset = []
    current_page_driver = webdriver.Firefox()
    for a in a_tags:
        href = a.get_attribute('href')
        current_page_driver.get(href)
        wait_element(current_page_driver, '//tr/td', by=By.XPATH)
        product_main = current_page_driver.find_element_by_xpath('//div[contains(@class,"product_main")]')
        product_main_text = product_main.text.split('\n')
        title = product_main_text[0]
        price = product_main_text[1]
        stock = re.findall('\d+', product_main_text[2])
        product_main_ps = product_main.find_elements_by_tag_name('p')
        stars_colors = [x.value_of_css_property("color") for x in product_main_ps[2].find_elements_by_tag_name('i')]
        stars = stars_colors.count('rgb(230, 206, 49)')
        description = current_page_driver.find_element_by_xpath('//article/p').text
        tds = current_page_driver.find_elements_by_xpath('//tr/td')
        upc = tds[0].text
        type = tds[1].text
        price_exc_tax = tds[2].text
        price_inc_tax = tds[3].text
        tax = tds[4].text
        nreviews = tds[6].text
        record = {'title': title, 'price': price, 'stars': stars, 'description': description, 'stock': stock,
                  'upc': upc, 'type': type, 'price_exc_tax': price_exc_tax, 'price_inc_tax': price_inc_tax,
                  'tax': tax, 'nreviews': nreviews}
        dataset.append(record)
    current_page_driver.close()
    return dataset


def scrapy_books(url):
    driver = webdriver.Firefox()
    driver.get(url)
    to_continue = True
    whole_dataset = []
    while to_continue:
        current_items = get_page_data(driver)
        whole_dataset.extend(current_items)
        try:
            next_button = driver.find_element_by_xpath('//li[@class="next"]/a')
        except NoSuchElementException:
            pass
            break
        next_button.click()
        wait_element(driver, '//img[@class="thumbnail"]', by=By.XPATH)
    driver.close()
    return whole_dataset


url = 'http://books.toscrape.com'
result = scrapy_books(url)
with open('data.json', 'w') as fp:
    json.dump(result, fp)
print(result)


