import os

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
from dotenv import load_dotenv

load_dotenv()


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
    """

    :param driver: DRIVER OBJECT TO SCRAPE DATA FROM PAGE 2
    :param url: NEXT PAGE URL
    :return: LIST OF SENTENCES FETCHED FROM JIDIPI WEBSITE.
    """
    time.sleep(2)
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="area-tooltip"]/div[1]/button[1]')))

    jidipi_result = []
    driver.find_element(By.XPATH, '//*[@id="area-tooltip"]/div[1]/button[1]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "setka-editor")))

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
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    """
    Uncomment Below Code if any errors Related to Driver comes in action.
    """
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--start-maximized")
    # options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-field ")))

        if driver.current_url == url:
            get_system_jidipi_data(driver, url)
        elif driver.current_url == "https://system.jidipi.com/login":
            email = driver.find_element(By.CLASS_NAME, "input-field ")
            email.send_keys(os.environ.get('EMAIL'))

            password = driver.find_element(By.CLASS_NAME, "form-control")
            password.send_keys(os.environ.get('PASSWORD'))

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn")))

            submit = driver.find_element(By.CLASS_NAME, "btn")
            submit.click()

            jidipi_result = get_system_jidipi_data(driver, url)
            return jidipi_result
        else:
            return "Invalid URL"
    except Exception as e:
        return "Invalid URL"
