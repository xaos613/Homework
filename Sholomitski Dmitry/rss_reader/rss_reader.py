import html
import json
import os
import pickle
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dateparser import parse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT

import rss_exceptions
from settings import logger_info, check_args


class RSSParser:
    """
    RSSparser base class. Takes a dictionary with settings as input and outputs needed information in the required form
    """

    def __init__(self, settings):
        self.settings = settings
        self.rss_content = self.url_request(settings['source'])
        self.list_of_items = self.parser(self.rss_content)
        self.items_for_print = sorted(self.list_of_items, key=lambda x: x['item_pubdate'], reverse=True)[
                               :settings['limit']]

        if self.settings['json']:
            RSSParser.json_print(self.items_for_print)
        else:
            RSSParser.rss_print(self.items_for_print)

        if self.settings['pdf']:
            self.save_to_pdf(self.items_for_print)
        if self.settings['html']:
            self.save_to_html(self.items_for_print)

    @staticmethod
    def load_to_archive(new_from_reader):
        """
        RSSparser base class. Takes a dictionary with settings as input and outputs needed information in the required form
        :param new_from_reader: list of dictionaries of news items
        :return: Nothing
        """
        if os.path.exists(os.getcwd() + '/.test_archive.pkl'):
            with open(os.getcwd() + '/.test_archive.pkl', 'rb') as pkl:
                unpickler = pickle.Unpickler(pkl)
                archive = unpickler.load()
                for item in new_from_reader:
                    if item in archive:
                        pass
                    else:
                        archive.append(item)

        else:
            archive = new_from_reader

        with open(os.getcwd() + '/.test_archive.pkl', 'wb') as pkl:
            pickle.dump(archive, pkl)

    @staticmethod
    def convert_to_text_format(dict_for_print: dict):
        """
        Print all the attributes of a news item
        :param dict_for_print: Dictionary of news attributes
        :return: print parametres
        """
        print(f"Title: {dict_for_print['item_title']}")
        print(f"Description: {dict_for_print['item_description']}")
        print(f"Published: {dict_for_print['item_pubdate']}")
        print(f"Image: {dict_for_print['item_image']}")
        print(f"Read more: {dict_for_print['item_link']}")

    @staticmethod
    def time_parser(date):
        """
        Takes the date and returns it in the single format

        :param date: date in any format
        :return: date in format  '%Y-%m-%d %H:%M:%S'
        """
        try:
            converted_date = parse(date).strftime('%Y-%m-%d %H:%M:%S')
            return converted_date

        except AttributeError:
            raise rss_exceptions.DateTimeError(f'unsupported pubDate format in feed')

    @staticmethod
    def check_url(url='') -> bool:
        """
        :param url: url from settings
        :return: True if url is valid
        """

        logger_info.info(f'Validating URL: {url}')

        if url is None:
            raise rss_exceptions.EmptyUrlError('Empty argument passed, please add an URL to proceed')
        url = url.strip()
        result = urlparse(url)
        if all([result.netloc, result.scheme]):
            logger_info.info('URL validated successfully')
            return True
        else:
            raise rss_exceptions.BadUrlError(
                'Invalid URL: URL must contain scheme and network location, try to add https://')

    @staticmethod
    def text_cleaner(string):
        """
        Clears the string of unnecessary characters

        :param string: virgin string
        :return: clean string
        """
        string = re.sub('<[^<]+>', '', html.unescape(string))
        string = re.sub('\xa0', ' ', string).strip()
        return string

    def url_request(self, url):
        """

        :param url: link to rss source
        :return: content of url in string format
        """
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

    def parser(self, rss_content):
        """
        Parses the received information of each news item and saves it in the archive
        :param rss_content:  content of rss in string format
        :return: list of dictionary with next parametres: 'rss_url','channel_title','channel_link','item_title',
        'item_pubdate','item_description','item_link','item_image'
        """

        list_of_items = []
        logger_info.info(f'Fetching RSS')
        soup = BeautifulSoup(rss_content, 'xml')

        if soup.find_all('item') == []:
            raise rss_exceptions.RssURLError('Incorrect ULR, cann\'t fetch RSS. Probably it\'s HTML link')

        channel_title = soup.find("title").text

        if soup.find('link').text != '':
            channel_link = soup.find('link').text
        elif soup.find('atom:link').get('href') != '':
            channel_link = soup.find('atom:link').get('href')
        else:
            channel_link = ''

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
                'rss_url': self.settings['source'],
                'channel_title': channel_title,
                'channel_link': channel_link,
                'item_title': item_title,
                'item_pubdate': item_pubdate,
                'item_description': item_description,
                'item_link': item_link,
                'item_image': item_image
            })

        RSSParser.load_to_archive(list_of_items)
        return list_of_items

    @staticmethod
    def rss_print(items_for_print):
        """

        :param items_for_print: list of news items to print
        :return: print news items in stdout
        """
        logger_info.info(f' printing in needed format')

        print_header = True

        for number_item in range(len(items_for_print)):
            if items_for_print[number_item]['channel_title'] != items_for_print[number_item - 1]['channel_title']:
                print_header = True
            if print_header:
                print('channel title: ', items_for_print[number_item]['channel_title'])
                print('channel link: ', items_for_print[number_item]['channel_link'])
                print('*' * 120)
                print_header = False
            RSSParser.convert_to_text_format(items_for_print[number_item])
            print('-' * 120)

    @staticmethod
    def json_print(items_for_print):
        """
        :param items_for_print: list of dictionaries of news items to print
        :return: print news items  in stdout in json format
        """
        for item in items_for_print:
            json_formatted_text = json.dumps(item, indent=4, ensure_ascii=False)
            print(json_formatted_text)

    def save_to_html(self, items_for_print):
        """
        saves the needed news to an HTML page
        :param items_for_print: items_for_print: list of dictionaries of news items
        :return: save in HTML page
        """

        logger_info.info('saving to HTML file')

        html_content = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n' \
                       '<title>Formatted RSS News</title>\n<style>\n' \
                       'h1,h2,h3,h4{margin: 0;}\n' \
                       'h2 {font-size: 18px;text-align: center;margin-bottom: 15px;}\n' \
                       'h3 {font-size: 16px;margin-bottom: 15px;font-weight: bolder;}\n' \
                       'h4 {font-weight: 100;font-size: 14px;    margin-bottom: 5px;}\n' \
                       '.wrapper {display: flex;}\n' \
                       '.layer1 img {border-radius: 5px;}\n' \
                       '.layer1 a {display: flex;}\n' \
                       '.layer2 {padding-left: 15px}\n' \
                       '.layer2 a {text-transform: uppercase;font-weight: bold;}</style><body>\n'

        print_header = True

        for number_item in range(len(items_for_print)):

            if items_for_print[number_item]['channel_title'] != items_for_print[number_item - 1]['channel_title']:
                print_header = True

            if print_header:
                html_content += f"<h2>Channel\'s title: <a href=\"{items_for_print[number_item]['channel_link']}" \
                                f"\">{items_for_print[number_item]['channel_title']}</a></h2>\n"
                html_content += f"<h2>Link to channel: <a href=\"{items_for_print[number_item]['channel_link']}\"" \
                                f">{items_for_print[number_item]['channel_link']}</a></h2>\n"

                print_header = False
            html_content += '<div class = "wrapper"><div class="layer1">'
            if items_for_print[number_item]['item_image'] == 'image is not provided':
                items_for_print[number_item]['item_image'] = 'https://user-images.githubusercontent.com/' \
                                                        '10515204/56117400-9a911800-5f85-11e9-878b-3f998609a6c8.jpg'

            html_content += f"""<a href=\"{items_for_print[number_item]['item_link']}\"><img class=\"alignleft\"
            src=\"{items_for_print[number_item]['item_image']}\" alt=\"\" width=\"300\"/></a>\n
            </div><div class="layer2">
            <h3>{items_for_print[number_item]['item_title']}</h3>\n
            <h4> {items_for_print[number_item]['item_description']}</h4>\n
            <h4>Published at: {items_for_print[number_item]['item_pubdate']}</h4>\n
            <h4><a href=\"{items_for_print[number_item]['item_link']}\">Read more</a></h4></div></div>\n</br>"""
        html_content += '</body></html>'
        if self.settings['html']:
            output = open("export.html", "w", encoding='utf-8')
            output.write(html_content)
            output.close()
        return html_content

    def save_to_pdf(self, items_for_print):
        """

        saves the needed news to an PDF file (with using save_to_html funktion makes html and convert to PDF file)
        :param items_for_print: list of dictionaries of news items to save
        :return: convert HTML to PDF
        """
        # open output file for writing (truncated binary)
        with open('export.pdf', "w+b") as result_file:
            font_path = os.path.dirname(__file__) + r'/Fonts/calibri.ttf'
            pdfmetrics.registerFont(TTFont('Calibri', font_path))
            DEFAULT_FONT["helvetica"] = "Calibri"
            # convert HTML to PDF
            source_html = self.save_to_html(items_for_print)
            pisa_status = pisa.CreatePDF(source_html, dest=result_file, encoding='utf-8')

        # return False on success and True on errors
        return pisa_status.err


class RSSarchive(RSSParser):
    """
    If the date is given, it downloads the archive, checks it with the required settings and prints it out
    """

    def __init__(self, settings):
        archive_path = os.getcwd() + '/.test_archive.pkl'
        self.settings = settings
        archive = RSSarchive.getarchive(archive_path)

        try:
            settings['date'] = str(settings['date'])
            datetime.strptime(settings['date'], '%Y%m%d')

            list_from_archive = RSSarchive.get_items_from_archive(archive, settings)
            items_for_print = sorted(list_from_archive, key=lambda x: x['item_pubdate'])[:settings['limit']]

            if settings['json']:
                RSSParser.json_print(items_for_print)
            else:
                RSSParser.rss_print(items_for_print)

            if self.settings['pdf']:
                self.save_to_pdf(items_for_print)
            if self.settings['html']:
                self.save_to_html(items_for_print)

        except ValueError:
            print(f'Entered date "{settings["date"]}" not in needed format, use this template:YYYYMMDD')
            sys.exit()

    @staticmethod
    def getarchive(archive_path):
        """

        :param archive_path: path to archive
        :return: list of dictionaries with news items
        """
        logger_info.info(f'Getting new from local Archive')
        try:
            with open(archive_path, 'rb') as pkl:
                unpickler = pickle.Unpickler(pkl)
                archive = unpickler.load()

                return archive
        except (FileNotFoundError, TypeError):
            print('There no any news in cache')
            sys.exit(1)

    @staticmethod
    def get_items_from_archive(archive, settings):
        """

        :param archive: list of dictionaries of news items
        :param settings: required settings given by user
        :return: news checked with settings
        """
        logger_info.info(f'Filtering new new in archive with provided settings')
        return_list = []
        for item in archive:
            if item['item_pubdate'][:10].replace('-', '') == settings['date']:
                if settings['source'] in (item['rss_url'], None):
                    return_list.append(item)
        if return_list == []:
            if settings['source'] is not None:
                in_source = f"at {settings['source']}"
            else:
                in_source = ''
            print(f'There no any news in cache with your date ({settings["date"]}) {in_source}')
        return return_list


def main():
    settings = check_args()

    if settings['date'] is None:
        RSSParser(settings)

    else:
        RSSarchive(settings)


if __name__ == '__main__':

    try:
        main()
    except Exception as e:
        print(f'Something goes wrong: {e}')
