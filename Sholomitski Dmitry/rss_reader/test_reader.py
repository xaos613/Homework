from unittest import TestCase, main
from unittest.mock import patch, call

import settings
from rss_reader import RSSParser, RSSarchive
from rss_reader import rss_exceptions


class TestRSSParser(TestCase):
    settings = {
        'limit': 1,
        'json': False,
        'verbose': False,
        'source': 'https://test_url.com/xml',
        'date': None,
        'html': False,
        'pdf': False
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
        parser = settings.get_args(['--limit', '3', '--verbose', '--json', 'https://money.onliner.by/feed', '--to-html',
                                    '--to-pdf'])
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
        parser = settings.check_args(['--limit', '3', '--verbose', '--json', 'https://money.onliner.by/feed'])
        archive_parser = settings.check_args(['--date', '20220606', '--to-html', '--to-pdf', '-v', '--path', 'source'])
        self.assertEqual(parser['limit'], 3)
        self.assertTrue(parser['verbose'])
        self.assertTrue(archive_parser['verbose'])
        self.assertEqual(parser['source'], 'https://money.onliner.by/feed')
        self.assertTrue(parser['json'])
        self.assertIsNone(archive_parser['source'])
        self.assertEqual(archive_parser['date'], '20220606')
        self.assertTrue(archive_parser['pdf'])
        self.assertTrue(archive_parser['html'])
        self.assertEqual(archive_parser['path'], 'source')

    @patch.object(RSSParser, 'url_request')
    def test_parser_mock(self, mock_url_request):
        files_dict = {
            'Tests_files/tests_xmls/rss_1.xml': 'Tests_files/dict_files/dict_1.txt',
            'Tests_files/tests_xmls/rss_2.xml': 'Tests_files/dict_files/dict_2.txt',
            'Tests_files/tests_xmls/rss_3.xml': 'Tests_files/dict_files/dict_3.txt',
            'Tests_files/tests_xmls/rss_4.xml': 'Tests_files/dict_files/dict_4.txt',
            'Tests_files/tests_xmls/rss_5.xml': 'Tests_files/dict_files/dict_5.txt',
            'Tests_files/tests_xmls/rss_6.xml': 'Tests_files/dict_files/dict_6.txt',
            'Tests_files/tests_xmls/rss_7.xml': 'Tests_files/dict_files/dict_7.txt',
            'Tests_files/tests_xmls/rss_8.xml': 'Tests_files/dict_files/dict_8.txt',
            'Tests_files/tests_xmls/rss_9.xml': 'Tests_files/dict_files/dict_9.txt',
            'Tests_files/tests_xmls/rss_10.xml': 'Tests_files/dict_files/dict_10.txt',
            'Tests_files/tests_xmls/rss_11.xml': 'Tests_files/dict_files/dict_11.txt',
        }

        for xlm_file, res_file in files_dict.items():
            with open(xlm_file, 'r') as xlm_file1, open(res_file) as res_file1:
                test1_file_rss = xlm_file1.read()
                test1_file_result = eval(res_file1.read())
                mock_url_request.return_value = test1_file_rss
                self.assertEqual(RSSParser.parser(self, mock_url_request()), test1_file_result)

    @patch('builtins.print')
    def test_rss_print(self, mock_print):
        with open('Tests_files/dict_files/dict_1.txt', 'r') as rss_file1:
            list_of_items = eval(rss_file1.read())

            RSSParser.rss_print(list_of_items)

            self.assertEqual(mock_print.mock_calls, [call('channel title: ', 'Yahoo News - Latest News  Headlines'),
                                                     call('channel link: ', 'https://www.yahoo.com/news'),
                                                     call(
                                                         '*' * 120),
                                                     call(
                                                         "Title: Spit, 'disrespect' arrive at Wimbledon as tennis"
                                                         " turns ugly"),
                                                     call('Description: Description not provided'),
                                                     call('Published: 2022-06-28 22:01:51'),
                                                     call(
                                                         'Image: https://s.yimg.com/uu/api/res/1.2/Kn3F_'
                                                         'gIJwe0a3uIOU.Tb2w--~B/aD0yMzgxO3c9MzU3MTthcHBpZD15dGFjaHlvbg'
                                                         '--/https://media.zenfs.com/en/ap.org/4a35cff443aaabc2b49d94a'
                                                         '5e7672369'),
                                                     call(
                                                         'Read more: https://news.yahoo.com/spit-disrespect-arrive-'
                                                         'wimbledon-tennis-220151441.html'),
                                                     call(
                                                         '-' * 120)
                                                     ])

    @patch('builtins.print')
    def test_json_print(self, mock_print):
        with open('Tests_files/dict_files/dict_1.txt', 'r') as rss_file1:
            list_of_items = eval(rss_file1.read())

            RSSParser.json_print(list_of_items)

            self.assertEqual(mock_print.mock_calls,
                             [call('{\n    "channel_link": "https://www.yahoo.com/news",'
                                   '\n    "channel_title": "Yahoo News - Latest News  Headlines",'
                                   '\n    "item_description": "Description not provided",'
                                   '\n    "item_image": "https://s.yimg.com/uu/api/res/1.2/Kn3F_gIJwe0a3uIOU.Tb2w--~B'
                                   '/aD0yMzgxO3c9MzU3MTthcHBpZD15dGFjaHlvbg--/'
                                   'https://media.zenfs.com/en/ap.org/4a35cff443aaabc2b49d94a5e7672369",'
                                   '\n    "item_link": "https://news.yahoo.com/spit-disrespect-arrive-wimbledon-tennis-'
                                   '220151441.html",\n    "item_pubdate": "2022-06-28 22:01:51",'
                                   '\n    "item_title": "Spit, \'disrespect\' arrive at Wimbledon as'
                                   ' tennis turns ugly",\n    "rss_url": "https://test_url.com/xml"\n}')])

    def test_save_to_html(self):
        with open('Tests_files/dict_for_print.txt') as dict_1, open('Tests_files/html_file.html') as res_file1:
            html_content = RSSParser.save_to_html(self, eval(dict_1.read()))

            self.assertEqual(html_content, res_file1.read())


class TestRSSArchive(TestCase):

    def test_getarchive(self):
        with self.assertRaises(SystemExit):
            RSSarchive.getarchive('url')

        with open('Tests_files/test_archive_dict.txt') as dict_file:
            dict_result = eval(dict_file.read())
            self.assertEqual(RSSarchive.getarchive('Tests_files/.test_archive.pkl'), dict_result)

    def test_get_items_from_archive(self):
        pass


if __name__ == '__main__':
    main()
