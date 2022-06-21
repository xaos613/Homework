from unittest import TestCase, main
from unittest.mock import Mock, patch, MagicMock

import settings
import json

from rss_reader import RSSParser
import rss_exceptions



class  TestRSSParser(TestCase):


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



    def test_unify_pubdate(self):
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
            RSSParser.check_url()
        with self.assertRaises(rss_exceptions.EmptyUrlError):
            RSSParser.check_url(' ')

    def test_convert_to_text_format(self):
        with open('test_files/conv_dict.txt') as inp_file, open('test_files/conv_dict_res.txt') as out_file:
            in_data = json.load(inp_file)
            out_data = out_file.read()
            self.assertEqual(RSSParser.convert_to_text_format(in_data),out_data)

    def test_parse_args(self):

        parser = settings.get_args(['--limit', '3', '--verbose', '--json', 'https://money.onliner.by/feed'])
        self.assertTrue(parser.limit)
        self.assertTrue(parser.verbose)
        self.assertTrue(parser.json)
        self.assertTrue(parser.source)
        with patch('builtins.input', return_value='--version'):
            self.assertRaises(SystemExit)
        with patch('builtins.input', return_value='--help'):
            self.assertRaises(SystemExit)

    def test_check_args(self):
        parser = settings.check_args(['--limit', '3', '--verbose', '--json', 'https://money.onliner.by/feed'])
        self.assertEqual(parser['limit'],3)
        self.assertEqual(parser['source'],'https://money.onliner.by/feed')
        self.assertTrue(parser['verbose'])
        self.assertTrue(parser['json'])


    @patch.object(RSSParser,'url_request')
    def test_parser_mock(self, mock_url_request):

        with open('test_files/text1_rss.xml', 'rb') as xlm_file1, open('test_files/test1_rss.txt') as res_file1:
            test1_file_rss =xlm_file1.read()
            test1_file_result = res_file1.read()


            mock_url_request.return_value = test1_file_rss
            # ТУТ СТРОКОВОЕ ПРЕДСТАВЛЕНИЕ
            #
            self.assertEqual(str(RSSParser.parser(self,mock_url_request())), test1_file_result)

    # @patch.object(RSSParser, 'rss_print')
    # def test_rss_print_mock(self, mock_url_request):
    #
    #     with open('test_files/text1_rss.xml', 'rb') as xlm_file1, open('test_files/test1_rss.txt') as res_file1:
    #         test1_file_rss =xlm_file1.read()
    #         test1_file_result = res_file1.read()
    #
    #
    #         mock_url_request.return_value = test1_file_rss
    #
    #
    #         mock_resut = RSSParser.rss_print(self, mock_url_request())
    #
    #
    #
    #         self.assertEqual((mock_resut), test1_file_result)




if __name__ == '__main__':
    main()


