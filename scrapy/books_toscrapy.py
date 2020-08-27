# -*- coding: utf-8 -*-
import datetime
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path_to_chromedriver = '/usr/bin/chromedriver'
path_to_firefoxdirver = '/usr/local/bin/geckodriver'
slack_channel_url = "https://cienciadadosenap2020.slack.com/x-p1282932360838-1295849149236-1289868974755/messages/C018W8GCJAV"

def wait_element(driver, by_content, by=By.ID, timeout=8, to_sleep=0):
    try:
        element_present = EC.presence_of_element_located((by, by_content))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        pass
        return False
    if to_sleep > 0:
        time.sleep(to_sleep)
    return True


driver = webdriver.Firefox()
url = 'http://books.toscrape.com/'
driver.get(url)
print(driver)
a_tags = driver.find_elements_by_xpath('//article/h3/a')
for a in a_tags:
    a.click()
    wait_element(driver, '//tr/td', by=By.XPATH)
    product_main = driver.find_element_by_xpath('//div[contains(@class,"product_main")]')
    title = product_main.find_element_by_tag_name('h1').text
    product_main_ps = product_main.find_elements_by_tag_name('p')
    price = product_main_ps[0].text
    estoque = re.findall('\d+', product_main_ps[1].text)
    stars_colors = [x.value_of_css_property("color") for x in product_main_ps[2].find_elements_by_tag_name('i')]
    stars = stars_colors.count('rgb(230, 206, 49)')
    description = driver.find_element_by_xpath('//article/p').text
    tds = driver.find_elements_by_xpath('//tr/td')
    upc = tds[0].text
    type = tds[1].text
    price_exc_tax = tds[2].text
    price_inc_tax = tds[3].text
    tax = tds[4].text
    nreviews = tds[6].text
