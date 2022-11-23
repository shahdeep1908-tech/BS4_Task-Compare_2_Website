import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


def mismatch():
    """
    Set the difference for Minor Mismatch with two strings.
    """
    # SequenceMatcher(a=a, b=b).ratio()
    pass


def check_sequence_of_data(blog_txt_lst, jidipi_txt_lst):
    blog_txt_lst = [item.lstrip() for item in blog_txt_lst]
    jidipi_txt_lst = [item.lstrip() for item in jidipi_txt_lst]
    seq_matcher = []
    try:
        for para_txt in jidipi_txt_lst:
            if para_txt in blog_txt_lst:
                seq_matcher.append(blog_txt_lst.index(para_txt))
            else:
                seq_matcher.append(-1)
    except ValueError:
        print("No Text Found! :::")

    return seq_matcher == sorted(seq_matcher)


def get_blog_url_data(url, headers):
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    blog_result = []
    for parent_tag in soup.find_all(attrs={"id": "single-content"}):
        for paragraph_tag in parent_tag.find_all("p"):
            if not paragraph_tag.has_attr("class"):
                blog_result.append(paragraph_tag.text)
                continue
    return blog_result


def get_jidipi_url_data(url, headers):
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
                cleaned_data = paragraph_tag.text
                if cleaned_data not in jidipi_result and len(cleaned_data) > 60:
                    jidipi_result.append(cleaned_data)

    return jidipi_result


def get_urls(blog_url, jidipi_url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    blog = get_blog_url_data(blog_url, headers)
    jidipi = get_jidipi_url_data(jidipi_url, headers)

    blog_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog)))
    jidipi_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(jidipi)))

    status = check_sequence_of_data(blog_txt.split('.'), jidipi_txt.split('.'))

    return status

# blog_url = "https://www.archdaily.com/938054/chinese-culture-exhibition-center-qingdao-tengyuan-design-plus-eca2"
# blog_url = "https://www.archdaily.com/246905/villa-jian-cu-office?ad_source=search&ad_medium=projects_tab"
# jidipi_url = "https://architectures.jidipi.com/j00063373/en/chinese-culture-exhibition-center"
# jidipi_url = "https://architectures.jidipi.com/j00030499/en/villa-jian"
