import copy
from time import sleep

from pysus.online_data.SIH import download
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import fnmatch
import os


def wait_download(path, extension, current_nfiles, max_wait=60):
    nfiles = len(fnmatch.filter(os.listdir(path), '*.{0}'.format(extension)))
    count = 0
    while nfiles == current_nfiles and count < max_wait:
        sleep(1)
        count += 1
        print(count)
        nfiles = len(fnmatch.filter(os.listdir(path), '*.{0}'.format(extension)))


def scrapy_datasus(value, download_path):
    url = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/qiuf.def'
    # options = webdriver.FirefoxOptions()
    # options.add_argument("download.default_directory=~/Downloads")  # Set the download Path
    # driver = webdriver.Firefox(options=options)
    options = webdriver.ChromeOptions()
    options.add_argument("download.default_directory={0}".format(download_path))  # Set the download Path
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.find_elements_by_xpath("//select[@id='L']/option")[2].click()
    options_I = driver.find_elements_by_xpath("//select[@id='I']/option")
    options_I[0].click()
    for o in options_I:
        o.click()

    driver.find_element_by_xpath("//label[@for='S4']").find_element_by_xpath('../img').click()
    driver.find_element_by_xpath("//select[@id='S4']/option[@value='{0}']".format(value)).click()
    options_A = driver.find_elements_by_xpath("//select[@id='A']/option")
    n_months = len(options_A)
    options_A[0].click()

    for n in range(n_months):
        if n > 0:
            options_A[n-1].click()
        options_A[n].click()
        driver.find_elements_by_xpath("//input[@id='F']")[1].click()
        driver.find_element_by_xpath("//input[@type='submit']").click()
        wait_element(driver, '//tr/td/a', by=By.XPATH)
        sleep(2)
        buttons = driver.find_elements_by_xpath("//tr/td/a")
        current_nfiles = len(fnmatch.filter(os.listdir(download_path), '*.{0}'.format('csv')))
        buttons[0].click()
        wait_download(download_path, 'csv', current_nfiles)
        sleep(1)
        buttons[-1].click()
        wait_element(driver, "//select[@id='A']/option", by=By.XPATH)
        options_A = driver.find_elements_by_xpath("//select[@id='A']/option")

def concat_pysus(ufs, y_begin, y_end):
    pieces = []
    for y in range(y_begin, y_end+1):
        for m in range(1, 13):
            for uf in ufs:
                df = download(uf, month=m, year=y)
                if df is not None:
                    pieces.append(df)

    result = pd.concat(pieces, ignore_index=True)
    return result

# uf = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
# df_concat = concat_pysus(uf, 2008, 2008)
# df_concat.tocsv("./test.csv")

scrapy_datasus(3809, '/home/alex/Downloads')