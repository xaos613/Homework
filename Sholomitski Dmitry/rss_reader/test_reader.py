import json
from unittest import TestCase, main
from unittest.mock import patch, call

from rss_reader import rss_exceptions
import settings
from rss_reader import RSSParser


class TestRSSParser(TestCase):
    settings = {
        'limit': 1,
        'json': False,
        'verbose': False,
        'source': 'https://test_url.com/xml'
    }

    def test_process_string(self):
        """
        Tests for process_string method of RssReader class
        :return: None
        """
        self.assertEqual(RSSParser.text_cleaner('Suzy &amp; John'), 'Suzy & John')

        self.assertEqual(RSSParser.text_cleaner('&quot;,&gt;,&lt;'), '",>,<')
        self.assertEqual(
            RSSParser.text_cleaner('<p><strong>May 25, 2022</strong> – In its ... shortage.</p>'),
            'May 25, 2022 – In its ... shortage.')
        self.assertEqual(
            RSSParser.text_cleaner('<p><strong>May 25,\xa02022</strong> – In its ... shortage.</p>'),
            'May 25, 2022 – In its ... shortage.')

    def test_pubdate(self):
        """
        Tests for unify_pubdate method of RssReader class
        :return: None
        """
        self.assertEqual(RSSParser.time_parser('Tue, 24 May 2022 23:45:43 GMT'), '2022-05-24 23:45:43')
        self.assertEqual(RSSParser.time_parser('2022-05-30T22:22:05Z'), '2022-05-30 22:22:05')
        self.assertEqual(RSSParser.time_parser('Fri, 13 May 2022 17:15:00 -0400'), '2022-05-13 17:15:00')
        self.assertEqual(RSSParser.time_parser('2022-06-04T01:00:00+04:00'), '2022-06-04 01:00:00')
        with self.assertRaises(rss_exceptions.DateTimeError):
            RSSParser.time_parser('')

    def test_validate_url(self):
        """
        Tests for validate_url method of RssReader class
        :return: None
        """
        self.assertTrue(RSSParser.check_url('https://news.google.com/rss/'))
        self.assertTrue(RSSParser.check_url('https://www.nytimes.com/section/world/rss.xml'))
        with self.assertRaises(rss_exceptions.BadUrlError):
            RSSParser.check_url('url')
        with self.assertRaises(rss_exceptions.BadUrlError):
            RSSParser.check_url('news.google.com/rss/')
        with self.assertRaises(rss_exceptions.BadUrlError):
            RSSParser.check_url('https://')
        with self.assertRaises(rss_exceptions.EmptyUrlError):
            RSSParser.check_url(None)

    def test_parse_args(self):
        parser = settings.get_args(['--limit', '3', '--verbose', '--json', 'https://money.onliner.by/feed', '--to-html', '--to-pdf'])
        self.assertTrue(parser.limit)
        self.assertTrue(parser.verbose)
        self.assertTrue(parser.json)
        self.assertTrue(parser.source)
        self.assertTrue(parser.to_pdf)
        self.assertTrue(parser.to_html)

        with patch('builtins.input', return_value='--version'):
            self.assertRaises(SystemExit)
        with patch('builtins.input', return_value='--help'):
            self.assertRaises(SystemExit)

    def test_check_args(self):
        parser = settings.check_args(['--limit', '3', '--verbose','--json', 'https://money.onliner.by/feed'])
        archive_parser = settings.check_args(['--date', '20220606', '--to-html', '--to-pdf'])
        self.assertEqual(parser['limit'], 3)
        self.assertTrue(parser['verbose'])
        self.assertEqual(parser['source'], 'https://money.onliner.by/feed')
        self.assertTrue(parser['json'])
        self.assertIsNone(archive_parser['source'])
        self.assertEqual(archive_parser['date'], '20220606')
        self.assertTrue(archive_parser['pdf'])
        self.assertTrue(archive_parser['html'])

    @patch.object(RSSParser, 'url_request')
    def test_parser_mock(self, mock_url_request):
        with open('Tests/test_files/text1_rss.xml', 'rb') as xlm_file1, open('Tests/test_files/test1_rss.txt') as res_file1:
            test1_file_rss = xlm_file1.read()
            test1_file_result = eval(res_file1.read())
            mock_url_request.return_value = test1_file_rss
            self.assertEqual(RSSParser.parser(self, mock_url_request()), test1_file_result)


    @patch('builtins.print')
    def test_rss_print(self, mock_print):
        with open('Tests/test_files/test_print1.txt', 'r') as rss_file1:
            list_of_items = eval(rss_file1.read())


            RSSParser.rss_print(list_of_items)

            self.assertEqual(mock_print.mock_calls, [
                call('Chanel title: ', 'Yahoo News - Latest News & Headlines'),
                 call('Chanel link: ', 'https://www.yahoo.com/news'),
                 call('*'*120),
                 call('Title: Biden takes spill while getting off bike after beach ride'),
                 call('Description: Description not provided'),
                 call('Published: 2022-06-18 14:37:24'),
                 call(
                     'Image: https://s.yimg.com/uu/api/res/1.2/P2jnufkdwScKbL6Nlq5KwA--~B/aD0zNDQxO3c9NTE2MTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/917004c60ab9effc69660f0537591e24'),
                 call('Read more: https://news.yahoo.com/biden-takes-spill-while-getting-143724765.html'),
                 call('------------------------------------------------------------------------------------------------------------------------')
                ])

    @patch('builtins.print')
    def test_json_print(self, mock_print):
        with open('Tests/test_files/test_print1.txt', 'r') as rss_file1:
            list_of_items = eval(rss_file1.read())

            RSSParser.json_print(list_of_items)

            self.assertEqual(mock_print.mock_calls, [
                call('{\n    "chanel_title": "Yahoo News - Latest News & Headlines",'
                     '\n    "chanel_link": "https://www.yahoo.com/news",'
                     '\n    "item_title": "Biden takes spill while getting off bike after beach ride",'
                     '\n    "item_pubdate": "2022-06-18 14:37:24",'
                     '\n    "item_description": "Description not provided",'
                     '\n    "item_link": "https://news.yahoo.com/biden-takes-spill-while-getting-143724765.html",'
                     '\n    "item_image": "https://s.yimg.com/uu/api/res/1.2/P2jnufkdwScKbL6Nlq5KwA--~B/aD0zNDQxO3c9NTE2MTthcHBpZD15dGFjaHlvbg--/https://media.zenfs.com/en/ap.org/917004c60ab9effc69660f0537591e24"\n}')],
                )


if __name__ == '__main__':
    main()
