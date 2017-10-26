from unittest import TestCase
from crawler import Crawler

class TestCrawler(TestCase):
    def test__pre_visit_url_condense_pass(self):
        c = Crawler
        self.assertEqual(c._pre_visit_url_condense(c, 'http://www.example.com/path/file.html#test'), 'http://www.example.com/path/file.html')

    def test__same_host_pass(self):
        import urllib.parse

        c = Crawler
        c.host = urllib.parse.urlparse('http://www.example.com')[1]
        self.assertTrue(bool(c._same_host(c, 'http://www.example.com/path/file.html')))

    def test__same_host_fail(self):
        import urllib.parse

        c = Crawler
        c.host = urllib.parse.urlparse('http://www.example.com')[1]
        self.assertFalse(bool(c._same_host(c, 'http:/yourname.xyz/path/file.html')))

    def test__has_product_pass(self):
        c = Crawler
        p = c.Webpage
        p.product_name = 'Perfume 212 VIP Rosé Carolina Herrera Feminino - Época Cosméticos'
        self.assertTrue(c._has_product(c, p))

    def test__has_product_fail(self):
        c = Crawler
        p = c.Webpage
        p.product_name = None
        self.assertFalse(c._has_product(c, p))

    def test_crawl(self):
        self.fail()
