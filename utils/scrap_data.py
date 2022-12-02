import requests
from bs4 import BeautifulSoup

import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_blog_url_data(url, headers):
    """
    Scrape the data from Blog URL and return the List of Text.
    :param url: Blog Data URL
    :param headers: Chrome Header
    :return: List of text
    """
    try:
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')

        blog_result = []
        for parent_tag in soup.find_all(attrs={"id": "single-content"}):
            for paragraph_tag in parent_tag.find_all("p"):
                if not paragraph_tag.has_attr("class"):
                    blog_result.append(paragraph_tag.text)
                    continue
        return blog_result
    except Exception as e:
        return "Invalid URL"


def get_system_jidipi_data(driver, url):
    time.sleep(1)
    driver.get(url)
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="area-tooltip"]/div[1]/button[1]')))

    jidipi_result = []
    driver.find_element(By.XPATH, '//*[@id="area-tooltip"]/div[1]/button[1]').click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "setka-editor")))

    for parent in driver.find_elements(By.ID, 'setka-editor'):
        for txt in parent.find_elements(By.CSS_SELECTOR, 'p[data-ce-tag="paragraph"]'):
            unnecessary_tag = txt.find_element(By.XPATH, './..').get_attribute('innerHTML')
            if '<strong' in txt.get_attribute('innerHTML') or '<h4' in unnecessary_tag or not txt.text:
                continue
            jidipi_result.append(re.sub(r'\n', '', txt.text))
    return jidipi_result


def get_jidipi_url_data(url):
    """
    Scrape the data from Jidipi URL and return the List of Text.
    :param url: Jidipi URL
    :param headers: Chrome Header
    :return: List of Jidipi para Text.
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--lang=en_US')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "input-field ")))

        if driver.current_url == url:
            get_system_jidipi_data(driver, url)
        elif driver.current_url == "https://system.jidipi.com/login":
            email = driver.find_element(By.CLASS_NAME, "input-field ")
            email.send_keys("dipen2soni@gmail.com")

            password = driver.find_element(By.CLASS_NAME, "form-control")
            password.send_keys("goldeneye123")

            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "btn")))

            submit = driver.find_element(By.CLASS_NAME, "btn")
            submit.click()

            jidipi_result = get_system_jidipi_data(driver, url)
            return jidipi_result
        else:
            return "Invalid URL"
    except Exception as e:
        return "Invalid URL"
