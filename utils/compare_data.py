import re
import unicodedata

from utils.scrap_data import get_blog_url_data, get_jidipi_url_data


def check_sequence_of_data(blog_txt_lst, jidipi_txt_lst):
    """

    :param blog_txt_lst: Blog Text Paragraph
    :param jidipi_txt_lst: Jidipi Text Paragraph
    :return: Boolean - Correct Sequence
    """
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

    """
    Compare the order of data with sorted order.
    """
    return seq_matcher == sorted(seq_matcher)


def get_urls(blog_url, jidipi_url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    """
    Get the Scraped Data from Scrap_data.py File.
    """
    blog = get_blog_url_data(blog_url, headers)
    jidipi = get_jidipi_url_data(jidipi_url, headers)

    """
    Eliminate extra spaces [If Any] using Regex.
    Unidecode data to remove ascii space.
    Convert the list into one whole paragraph.
    """
    blog_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog)))
    jidipi_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(jidipi)))

    """
    Get the data checked for correct order/sequence as per Jidipi URL.
    """
    status = check_sequence_of_data(blog_txt.split('.'), jidipi_txt.split('.'))

    return status, blog_txt, jidipi_txt
