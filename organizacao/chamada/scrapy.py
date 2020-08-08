# -*- coding: utf-8 -*-
import datetime
import time

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path_to_chromedriver = '/usr/bin/chromedriver'
path_to_firefoxdirver = '/usr/local/bin/geckodriver'
slack_channel_url = "https://cienciadadosenap2020.slack.com/x-p1282932360838-1295849149236-1289868974755/messages/C018W8GCJAV"

def wait_element(driver, id, timeout=8, by_tag=By.ID, to_sleep=0):
    try:
        element_present = EC.presence_of_element_located((by_tag, id))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        pass
        return False
    if to_sleep>0:
        time.sleep(to_sleep)
    return True

def scrapy_students(user, password, url=slack_channel_url, exclude_list=None, no_window=True):
    import os.path

    if os.path.isfile(path_to_firefoxdirver):
        options = webdriver.FirefoxOptions() #FirefoxOptions()
        if no_window:
            options.add_argument('headless')
        driver = webdriver.Firefox(firefox_options=options, executable_path=path_to_firefoxdirver)
    elif os.path.isfile(path_to_chromedriver):
        options = webdriver.ChromeOptions() #FirefoxOptions()
        if no_window:
            options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options, executable_path=path_to_chromedriver)
    else:
        print("error: no driver found")
        return None

    driver.get(url)
    result = {}

    email_input = driver.find_element_by_xpath('//input[@id="email"]')
    email_input.send_keys(user)
    password_input = driver.find_element_by_xpath('//input[@id="password"]')
    password_input.send_keys(password)
    button = driver.find_element_by_xpath('//button[@id="signin_btn"]')
    button.click()
    wait_element(driver, id='//a[@data-qa-channel-sidebar-channel-type="im"]', by_tag=By.XPATH, to_sleep=5)
    tree_items = driver.find_elements_by_xpath('//a[@data-qa-channel-sidebar-channel-type="im"]')
    students = []
    today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    for i in tree_items:
        name = i.text.replace('(you)','')
        if i.find_elements_by_tag_name('i')[1].get_attribute('title') == "Active":
            students.append({'nome': name, today: 'Ativo'})
        else:
            students.append({'nome': name, today: 'Inativo'})

    students = [s for s in students if s['nome'] not in exclude_list]
    driver.close()
    return students


