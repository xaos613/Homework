'''
посмореть как отключается verbose
помотриеть названия ошибок

'''
from audioop import reverse

import rss_exceptions


import html
import json
import re

import requests
from bs4 import BeautifulSoup
from dateparser import parse
from urllib.parse import urlparse

from settings import logger_info, check_args


class RSSParser:
    def __init__(self, settings):
        self.settings = settings
        self.rss_content = self.url_request(settings['source'])
        self.list_of_items = self.parser(self.rss_content)
        self.rss_print(self.list_of_items, self.settings['limit'])


    @staticmethod
    def convert_to_text_format(dict_for_print: dict):

        return "".join(
            [f"Title: {dict_for_print['item_title']}\n"
             f"Description: {dict_for_print['item_description']}\n"
             f"Published: {dict_for_print['item_pubdate']}\n"
             f"Image: {dict_for_print['item_image']}\n"
             f"Read more: {dict_for_print['item_link']}\n"
             ]
        )

    @staticmethod
    def time_parser(date):
        """
        принимает дату возвращает в одном формате

        :param date: дата из å любом формате
        :return: дата в формате '%Y-%m-%d %H:%M:%S'
        """
        try:
            converted_date = parse(date).strftime('%Y-%m-%d %H:%M:%S')
            return converted_date

        except AttributeError:
            raise rss_exceptions.DateTimeError(f'unsupported pubDate format in feed')

    @staticmethod
    def check_url(url= '') -> bool:

        logger_info.info(f'Validating URL: {url}')
        url = url.strip()
        if not url:
            raise rss_exceptions.EmptyUrlError('Empty argument passed, please pass an URL to proceed')

        result = urlparse(url)
        if all([result.netloc, result.scheme]):
            logger_info.info('URL validated successfully')
            return True
        else:
            raise rss_exceptions.BadUrlError('Invalid URL: URL must contain scheme and network location')

    @staticmethod
    def text_cleaner(string):
        """
        очищает строку от ненужных символов

        :param string: virgin string
        :return: clean string
        """
        string = re.sub('<[^<]+>', '', html.unescape(string))
        string = re.sub('\xa0', ' ', string).strip()
        return string

    def url_request(self, url):
        headers_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/102.0.5005.62 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                  'q=0.9,image/avif,image/webp,image/apng,*/*;'
                                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
                        }

        logger_info.info(f'Making a request to {url} ')
        if RSSParser.check_url(url):
            with requests.get(url, headers=headers_dict) as response:
                logger_info.info('Connect to URL, reading data')
                rss_content = response.content

        logger_info.info('Rss data successfully decoded')

        return rss_content

    def rss_print(self, list_of_items, limit=None):
        logger_info.info(f' printing in needed format')

        items_for_print = sorted(list_of_items, key=lambda x: x['item_pubdate'], reverse =True)[:limit]

        if self.settings['json']:
            for item in items_for_print:
                json_formatted_text = json.dumps(item, indent=4, ensure_ascii=False)
                print(json_formatted_text)
        else:
            items_for_print = sorted(items_for_print, key=lambda x: x['chanel_title'])

            print_header = True

            for number_item in range(len(items_for_print)):
                if items_for_print[number_item]['chanel_title'] != items_for_print[number_item-1]['chanel_title']:
                    print_header = True
                if print_header:
                    print(items_for_print[number_item]['chanel_title'], items_for_print[number_item]['chanel_link'], '=' * 120, sep='\n')
                    print_header= False
                print(RSSParser.convert_to_text_format(items_for_print[number_item]))
                print('-' * 120)

    def parser(self, rss_content):
        list_of_items = []

        logger_info.info(f'Fetching RSS')
        soup = BeautifulSoup(rss_content, 'xml')

        chanel_title = soup.find("title").text

        if soup.find('link').text != '':
            chanel_link = soup.find('link').text
        else:
            chanel_link = soup.find('atom:link').get('href')

        for item in soup.find_all('item'):

            item_title = RSSParser.text_cleaner(
                item.title.text) if item.title.text is not None else 'Title not provided'
            item_pubdate = RSSParser.time_parser(
                item.pubDate.text) if item.pubDate is not None else 'Date is not provided'
            item_description = RSSParser.text_cleaner(
                item.description.text) if item.description is not None else 'Description not provided'
            if item_description == '':
                item_description = 'Description not provided'
            item_link = item.link.text if item.link is not None else 'link is not provided'

            image_template = ('media:content', 'media:thumbnail', 'enclosure', "image")

            for template in image_template:
                if item.find(template) is not None:

                    if item.find(template).get("url") is not None:
                        item_image = item.find(template).get("url")
                    elif item.find(template).text != '':
                        item_image = item.find(template).text
                    break
                else:
                    item_image = 'image is not provided'

            list_of_items.append({
                'chanel_title': chanel_title,
                'chanel_link': chanel_link,
                'item_title': item_title,
                'item_pubdate': item_pubdate,
                'item_description': item_description,
                'item_link': item_link,
                'item_image': item_image
            })

        return list_of_items


if __name__ == '__main__':


    # settings = check_args()
    settings = {
        'limit': 4,
        'json': False,
        'verbose': False,
        'source': 'https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml'
    }
    RSSParser(settings)
