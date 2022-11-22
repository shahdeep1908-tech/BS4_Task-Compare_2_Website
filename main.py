import re
import unicodedata

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}


def check_sequence_of_data():
    pass


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
                if check_element.find("strong"):
                    flag = True
                    continue
            if not flag:
                cleaned_data = paragraph_tag.text.strip()
                if cleaned_data not in jidipi_result:
                    jidipi_result.append(cleaned_data)

    return jidipi_result


blog_url = "https://www.archdaily.com/938054/chinese-culture-exhibition-center-qingdao-tengyuan-design-plus-eca2"
jidipi_url = "https://architectures.jidipi.com/j00063373/en/chinese-culture-exhibition-center"

blog = get_blog_url_data(blog_url)
jidipi = get_jidipi_url_data(jidipi_url)

with open('blog.txt', 'w') as f:
    # f.write(re.sub(r'(?<=[.,])(?=[^\s])', r' ', ''.join(blog)))
    f.write(re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog))))

with open('jidipi.txt', 'w') as f:
    # f.write(re.sub(r'(?<=[.,])(?=[^\s])', r' ', ''.join(jidipi)))
    f.write(re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(jidipi))))
