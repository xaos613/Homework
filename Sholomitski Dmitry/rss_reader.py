import html
import json
import re

import requests
from bs4 import BeautifulSoup
from dateparser import parse

from settings import logger_info


class RSSParser:
    def __init__(self, settings):
        self.settings = settings
        self.news_dict = RSSParser.parser(self.settings['source'])
        self.rss_print(self.settings['limit'])

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
        converted_date = parse(date).strftime('%Y-%m-%d %H:%M:%S')
        return converted_date

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

    @staticmethod
    def url_request(url):
        headers_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/102.0.5005.62 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;'
                                  'q=0.9,image/avif,image/webp,image/apng,*/*;'
                                  'q=0.8,application/signed-exchange;v=b3;q=0.9',
                        }

        logger_info.info(f'Making a request to {url} ')

        with requests.get(url, headers=headers_dict) as response:
            logger_info.info('Connected to URL, reading data')
            rss_content = response.content

        logger_info.info('Rss data successfully decoded')

        return rss_content

    @staticmethod
    def parser(rss_url):

        rss_content = RSSParser.url_request(rss_url)
        logger_info.info(f'Fetching RSS')
        soup = BeautifulSoup(rss_content, 'xml')

        chanel_title = soup.find("title").text

        if soup.find('link').text != '':
            chanel_link = soup.find('link').text
        else:
            chanel_link = soup.find('atom:link').get('href')

        temp_dict = {rss_url: {}}
        for item in soup.find_all('item'):

            item_title = RSSParser.text_cleaner(
                item.title.text) if item.text is not None else 'Title not provided'
            item_pubdate = RSSParser.time_parser(
                item.pubDate.text) if item.pubDate is not None else 'Date is not provided'
            item_description = RSSParser.text_cleaner(
                item.description.text) if item.description is not None else 'Description not provided'
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

            temp_dict[rss_url][item_pubdate] = {
                'chanel_title': chanel_title,
                'chanel_link': chanel_link,
                'item_title': item_title,
                'item_pubdate': item_pubdate,
                'item_description': item_description,
                'item_link': item_link,
                'item_image': item_image
            }

        return temp_dict

    def rss_print(self, limit=None):
        logger_info.info(f' printing in needed format')
        items_for_print = sorted(list(self.news_dict[self.settings['source']].keys())[:limit])

        if self.settings['json']:
            for item in items_for_print:
                json_formatted_text = json.dumps(self.news_dict[self.settings['source']][item], indent=4,
                                                 ensure_ascii=False)
                print(json_formatted_text)
        else:
            feed_title = self.news_dict[self.settings['source']][items_for_print[0]]['chanel_title']
            chanel_link = self.news_dict[self.settings['source']][items_for_print[0]]['chanel_link']
            print(feed_title, chanel_link, '=' * 120, sep='\n')

            for item in items_for_print:
                print(RSSParser.convert_to_text_format(self.news_dict[settings['source']][item]))
                print('-' * 120)


if __name__ == '__main__':
    # settings = check_args()

    settings = {
        'limit': 1,
        'json': True,
        'verbose': True,
        'source': 'https://money.onliner.by/feed'

    }
    RSSParser(settings)

    # RSSParser('https://www.yahoo.com/news/rss', settings)
    # RSSParser('https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml', settings)
    # RSSParser('https://moxie.foxnews.com/feedburner/latest.xml', settings)
    # RSSParser('https://feeds.simplecast.com/54nAGcIl', settings)
    # RSSParser('http://news.rambler.ru/rss/politics/', settings)
    # RSSParser('https://www.goha.ru/rss/mmorpg', settings)
    # RSSParser('https://money.onliner.by/feed', settings)
    # RSSParser('http://www.gazeta.ru/export/gazeta_rss.xml', settings)
    # RSSParser('https://vse.sale/news/rss', settings)
    # RSSParser('https://news.google.com/rss/', settings)
    # RSSParser('https://www.nytimes.com/section/world/rss.xml', settings)
    # RSSParser('https://www.cnbc.com/id/100727362/device/rss/rss.html', settings)
    # RSSParser('https://www.cbsnews.com/latest/rss/world', settings)
    # RSSParser('https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', settings)
    # RSSParser('https://auto.onliner.by/feed', settings)
    # RSSParser('http://feeds.bbci.co.uk/news/world/rss.xml', settings)
    # RSSParser('https://www.buzzfeed.com/world.xml', settings)
    # RSSParser('https://www.kommersant.ru/RSS/news.xml', settings)
    # RSSParser('https://www.latimes.com/local/rss2.0.xml', settings)
