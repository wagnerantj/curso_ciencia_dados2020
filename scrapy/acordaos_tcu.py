# -*- coding: utf-8 -*-
import datetime
import re
from selenium import webdriver

login = "usuario"
passowrd = "senha"

url = 'https://pesquisa.apps.tcu.gov.br/#/resultado/acordao-completo/*/%2520/%2520'
driver = webdriver.Firefox()
driver.get(url)


print(driver)
driver.close()

