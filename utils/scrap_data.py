import requests
from bs4 import BeautifulSoup


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


def get_jidipi_url_data(url, headers):
    """
    Scrape the data from Jidipi URL and return the List of Text.
    :param url: Jidipi URL
    :param headers: Chrome Header
    :return: List of Jidipi para Text.
    """
    try:
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
    except Exception as e:
        return "Invalid URL"
