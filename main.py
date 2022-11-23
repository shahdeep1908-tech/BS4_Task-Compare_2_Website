import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}


def mismatch():
    """
    Set the difference for Minor Mismatch with two strings.
    """
    # SequenceMatcher(a=a, b=b).ratio()
    pass


def check_sequence_of_data(blog_txt_lst, jidipi_txt_lst):
    for jidipi_str, blog_str in zip(jidipi_txt_lst, blog_txt_lst):
        if jidipi_str == blog_str:
            print(True)
        else:
            print(False)
    return


def get_blog_url_data(url):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    blog_result = []
    for parent_tag in soup.find_all(attrs={"id": "single-content"}):
        for paragraph_tag in parent_tag.find_all("p"):
            if not paragraph_tag.has_attr("class"):
                blog_result.append(paragraph_tag.text.strip())
                continue
    return blog_result


def get_jidipi_url_data(url):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    jidipi_result = []
    for parent_tag in soup.find_all("div", attrs={"class": ["valign-middle", "jdp-grid-col"]}):
        for paragraph_tag in parent_tag.find_all("p", attrs={"class": "jdp-reset"}):
            parent_tag = parent_tag.find("p").parent
            flag = False
            for check_element in parent_tag.contents:
                if check_element.find("strong") or check_element.find("h4"):
                    flag = True
                    continue
            if not flag:
                cleaned_data = paragraph_tag.text.strip()
                print(cleaned_data, len(cleaned_data), ':::')
                if cleaned_data not in jidipi_result:
                    jidipi_result.append(cleaned_data)

    return jidipi_result


# blog_url = "https://www.archdaily.com/938054/chinese-culture-exhibition-center-qingdao-tengyuan-design-plus-eca2"
blog_url = "https://www.archdaily.com/246905/villa-jian-cu-office?ad_source=search&ad_medium=projects_tab"
# jidipi_url = "https://architectures.jidipi.com/j00063373/en/chinese-culture-exhibition-center"
jidipi_url = "https://architectures.jidipi.com/j00030499/en/villa-jian"

blog = get_blog_url_data(blog_url)
jidipi = get_jidipi_url_data(jidipi_url)

blog_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog)))
jidipi_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(jidipi)))

# print(blog_txt.split('.'))
# print(len(blog_txt.split('.')))
# print()
# print(jidipi_txt.split('.'))
# print(len(jidipi_txt.split('.')))
check_sequence_of_data(blog_txt.split('.'), jidipi_txt.split('.'))
