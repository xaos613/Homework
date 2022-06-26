"""
написать тестовые можели для  всех вариантов RSS
написать тесты для json

если нет новостей - напечатать "новостей нет"
если все тэги пустые - поднять ошибку не та разметка (или попсотреть как проверить разметку html или xml)

"""

import html
import json
import os
import pickle
import re
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dateparser import parse

import rss_exceptions
from settings import logger_info, check_args


class RSSParser:
    def __init__(self, settings):
        self.settings = settings
        self.rss_content = self.url_request(settings['source'])
        self.list_of_items = self.parser(self.rss_content)
        items_for_print = sorted(self.list_of_items, key=lambda x: x['item_pubdate'], reverse=True)[:settings['limit']]

        if self.settings['json']:
            RSSParser.json_print(items_for_print)
        else:
            RSSParser.rss_print(items_for_print)

    @staticmethod
    def load_to_archive(new_from_reader):
        if os.path.exists(os.getcwd() + '/.archive.pkl'):
            with open(os.getcwd() + '/.archive.pkl', 'rb') as pkl:
                unpickler = pickle.Unpickler(pkl)
                archive = unpickler.load()
                for item in new_from_reader:
                    if item in archive:
                        pass
                    else:
                        archive.append(item)

        else:
            archive = new_from_reader

        with open(os.getcwd() + '/.archive.pkl', 'wb') as pkl:
            pickle.dump(archive, pkl)


    @staticmethod
    def convert_to_text_format(dict_for_print: dict):
        print(f"Title: {dict_for_print['item_title']}")
        print(f"Description: {dict_for_print['item_description']}")
        print(f"Published: {dict_for_print['item_pubdate']}")
        print(f"Image: {dict_for_print['item_image']}")
        print(f"Read more: {dict_for_print['item_link']}")

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
    def check_url(url='') -> bool:

        logger_info.info(f'Validating URL: {url}')

        if url is None:
            raise rss_exceptions.EmptyUrlError('Empty argument passed, please add an URL to proceed')
        url = url.strip()
        result = urlparse(url)
        if all([result.netloc, result.scheme]):
            logger_info.info('URL validated successfully')
            return True
        else:
            raise rss_exceptions.BadUrlError('Invalid URL: URL must contain scheme and network location, try to add http://')

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
            try:
                with requests.get(url, headers=headers_dict, timeout=2) as response:
                    logger_info.info('Connecting to URL')
                    if response.status_code == 200:
                        logger_info.info('Successfully connected to URL, reading data')

                    rss_content = response.content
            except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                print('Bad URL, cann\'t connect')
                sys.exit()

        logger_info.info('Rss data successfully decoded')

        return rss_content

    @staticmethod
    def rss_print(items_for_print):
        logger_info.info(f' printing in needed format')

        print_header = True

        for number_item in range(len(items_for_print)):
            if items_for_print[number_item]['chanel_title'] != items_for_print[number_item - 1]['chanel_title']:
                print_header = True
            if print_header:
                print(items_for_print[number_item]['chanel_title'])
                print(items_for_print[number_item]['chanel_link'])
                print('=' * 120)
                print_header = False
            RSSParser.convert_to_text_format(items_for_print[number_item])
            print('-' * 120)

    @staticmethod
    def json_print(items_for_print):
        for item in items_for_print:
            json_formatted_text = json.dumps(item, indent=4, ensure_ascii=False)
            print(json_formatted_text)

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
                'rss_url':self.settings['source'],
                'chanel_title': chanel_title,
                'chanel_link': chanel_link,
                'item_title': item_title,
                'item_pubdate': item_pubdate,
                'item_description': item_description,
                'item_link': item_link,
                'item_image': item_image
            })

        RSSParser.load_to_archive(list_of_items)
        return list_of_items


class RSSarchive(RSSParser):
    def __init__(self,settings):
        archive = RSSarchive.getarchive()
        list_from_archive = RSSarchive.get_items_from_archive(archive,settings)
        items_for_print = sorted(list_from_archive, key=lambda x: x['item_pubdate'])[:settings['limit']]

        if settings['json']:
            RSSParser.json_print(items_for_print)
        else:
            RSSParser.rss_print(items_for_print)


    @staticmethod
    def getarchive():
        with open(os.getcwd() + '/.archive.pkl', 'rb') as pkl:
            unpickler = pickle.Unpickler(pkl)
            archive = unpickler.load()
        return archive

    @staticmethod
    def get_items_from_archive(archive,settings):
        return_list = []
        for item in archive:
            if item['item_pubdate'][:10].replace('-', '') == settings['date']:
                if item['rss_url'] == settings['source'] or settings['source'] == None:
                    return_list.append(item)
        return return_list

def main():
    settings = check_args()

    settings = {
        'limit': None,
        'json': True,
        'verbose': False,
        'source': None,
        # 'date':'20220625'

    }
    try:
        if settings['date']:
            RSSarchive(settings)
    except KeyError:
        RSSParser(settings)




if __name__ == '__main__':
    main()




