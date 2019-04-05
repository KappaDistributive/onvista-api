#!/usr/bin/python
import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

DIRNAME = os.path.dirname(__file__)

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def etf_data(base_url, isin):
    raw_html = simple_get(base_url + isin)
    soup = BeautifulSoup(raw_html, 'html.parser')
    [price, currency] = soup.find('span', class_='price').contents[0].replace(',', '.').strip().split(' ')
    name = soup.find('title').contents[0].split('-')[0].strip()
    return [name, 'ETF', isin, float(price), currency]


def isin_list(filename):
    result = [] 
    with open(os.path.join(DIRNAME,filename), 'r') as f:
        for entry in f:
            result.append(entry.strip())
    return result 

def etf_data_list():
    data = isin_list('etf.list')
    result = []
    for isin in data:
        result.append(etf_data('https://www.onvista.de/etf', isin))
    return result

if __name__ == '__main__':
    for entry in etf_data_list():
        print(entry)
