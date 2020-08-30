# -*- coding: utf-8 -*-
import datetime
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scrapy.auth_data import user_github, password_github
from scrapy.util import wait_element

url = 'https://jupyter.enap.gov.br/'
driver = webdriver.Firefox()
driver.get(url)
driver.find_element_by_xpath('//div[@class="service-login"]').click()
driver.find_element_by_xpath('//input[@id="login_field"]').send_keys(user_github)
driver.find_element_by_xpath('//input[@id="password"]').send_keys(password_github)

button_signin = driver.find_element_by_xpath('//input[@type="submit"]')
button_signin.click()
print(driver)
url_aula1 = 'https://jupyter.enap.gov.br/user/alexlopespereira/notebooks/bootcamp/Aula2/Aula2_Exercicios.ipynb'
wait_element(driver, '//input[@type="checkbox"]', by=By.XPATH)
driver.get(url_aula1)
wait_element(driver, '//div[@class="input_area"]', by=By.XPATH)
div_area = driver.find_elements_by_xpath('//div[@class="prompt_container"]')[0]
while True:
    div_area.click()
    driver.find_element_by_xpath('//button[@title="Run"]').click()
    sleep(5*60)
    print('running now at {0}'.format(datetime.datetime.now()))
    with open("./log.txt", "a") as file_object:
        file_object.write('running now at {0}\n'.format(datetime.datetime.now()))

driver.close()

