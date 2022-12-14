from utils.scrap_data import get_blog_url_data, get_blog_url_data_by_parts, get_architizer_blog_url_data_by_parts
import re, math
import unicodedata

from .extras import check_extra_dots


def check_max_sentences(blog_txt, spliting_parts):
    """
    Get the whole Text. Split it into chunks and return the equally shared chunk Data.

    :param blog_txt: Blog URL Data
    :param spliting_parts: No of Splitting chunks required
    :return: Sliced data and max_length_of chunks that can be made.
    """
    punctuation = '.?!;'
    blog_lst = blog_txt.split('.')
    cleaned_blog_lst = []
    temp_string = ''
    for sentences_idx in range(len(blog_lst)):
        sentence = blog_lst[sentences_idx].strip()
        if len(sentence) < 10:
            temp_string = temp_string + sentence + '.'
            continue
        else:
            if temp_string:
                sentence = temp_string + sentence
                temp_string = ''
            if sentence[-1] in punctuation or sentence[-2] in punctuation:
                cleaned_blog_lst.append(sentence)
                continue
            cleaned_blog_lst.append(sentence + '.')

    max_length_of_data = len(cleaned_blog_lst)

    if spliting_parts > max_length_of_data:
        return False, '', max_length_of_data
    sliced_data = []

    """
    Change the floor to ceil, If you want the minimum number of sentences to
    be joined together as a paragraph.
    """
    chunks = math.floor(max_length_of_data / spliting_parts)
    idx = 0
    for i in range(spliting_parts):
        final_txt = ''.join(cleaned_blog_lst[idx:idx + chunks])
        if final_txt:
            sliced_data.append(final_txt)
        idx += chunks
    return True, sliced_data, ''


def get_data_to_split(blog_url, data_split_num, name):
    """
    GET THE INPUT OF URL FROM WHICH DATA NEEDS TO BE SCRAPPED, AND THE NUMBER OF SENTENCES FOR SPLIT

    :param blog_url: BLOG URL SCRAPPED DATA
    :param data_split_num: NUMBER OF SENTENCES TO BE SPLIT INTO.
    :return: STATUS OF DATA SPLIT, DATA ITSELF, MAX_DATA THAT CAN GE GENERATED
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

    """
    Get the Scraped Data from Scrap_data.py File.
    """
    if name == 'split_data_by_parts':
        if "architizer.com" in blog_url:
            blog = get_architizer_blog_url_data_by_parts(blog_url, headers)
        else:
            blog = get_blog_url_data_by_parts(blog_url, headers)

        check_extra_dots(blog)
        lst = []
        for blog_lst in blog:
            lst.append(re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog_lst).strip())))
        if lst:
            return True, lst
        return False, lst
    else:
        blog = get_blog_url_data(blog_url, headers)

        check_extra_dots(blog)

    """
    Eliminate extra spaces [If Any] using Regex.
    Unidecode data to remove ascii space.
    Convert the list into one whole paragraph.
    """
    blog_txt = re.sub(r'(?<=[.,])(?=[^\s])', r' ', unicodedata.normalize("NFKD", ''.join(blog).strip()))

    """
    Get the data checked for Max Sentences that can be made and return the data.
    """
    status, data, max_data = check_max_sentences(blog_txt, int(data_split_num))
    return status, data, max_data
