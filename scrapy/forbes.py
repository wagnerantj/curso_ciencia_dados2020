# -*- coding: utf-8 -*-
import datetime
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from scrapy.util import wait_element, remove_element
import json

def get_page_data(driver):
    rows = driver.find_elements_by_xpath('//div[@role="row"]')
    dataset = []
    first = True
    for r in rows:
        if first:
            print("rows")
            first = False
            continue
        cols = r.text.split('\n')
        record = {'rank': cols[0], 'name': cols[1], 'revenues': cols[2], 'revenue_pc': cols[3], 'profit': cols[4],
                  'profit_pc': cols[5], 'assets': cols[6], 'employees': cols[7], 'change_rank': cols[8],
                  'years_500': cols[9]}
        dataset.append(record)

    return dataset


def scrapy_forbes(url):
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver)
    to_continue = True
    # Espera a página carregar. Esperando pelo ID da propaganda
    wait_element(driver, 'piano-wrapper', by=By.ID)
    # Remove o elemento de propaganda sobreposto à página
    remove_element(driver, driver.find_element_by_id('piano-wrapper'))
    # Muda a paginação para 100
    wait_element(driver, '//option[@value="100"]', by=By.XPATH)
    o100 = driver.find_element_by_xpath('//option[@value="100"]')
    o100.click()

    whole_dataset = []
    while to_continue:
        current_items = get_page_data(driver)
        whole_dataset.extend(current_items)
        try:
            driver.find_element_by_xpath('//div[@class="-next"]/button[@disabled]')
            break
        except NoSuchElementException:
            pass

        next_button = driver.find_element_by_xpath('//div[@class="-next"]/button')
        next_button.click()
        wait_element(driver, '//div[@role="row"]', by=By.XPATH)
    driver.close()
    return whole_dataset


url = 'https://fortune.com/global500/2020/search/'
result = scrapy_forbes(url)
with open('data.json', 'w') as fp:
    json.dump(result, fp)
print(result)