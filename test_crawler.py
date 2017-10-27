from test_dbhandler import DBHandler

from crawler import Crawler
from crawler_db import (Status, Link, Product)
from crawler_web import Webpage


class TestCrawler(DBHandler):

    # overload __init__
    def __init__(self, *args, **kwargs):
        DBHandler.init_engine(self)
        DBHandler.__init__(self, *args, **kwargs)

    def __del__(self):
        DBHandler.del_engine(self)

    def test__pre_visit_url_condense_pass(self):
        c = Crawler()
        self.assertEqual(c._pre_visit_url_condense('http://www.example.com/file.html#test'),
                         'http://www.example.com/file.html')

    def test__same_host_pass(self):
        c = Crawler()
        c.host = 'www.example.com'
        self.assertTrue(bool(c._same_host('http://www.example.com/file.html')))

    def test__same_host_fail(self):
        c = Crawler()
        c.host = 'www.example.com'
        self.assertFalse(bool(c._same_host('http:/yourname.xyz/file.html')))

    def test__has_product_pass(self):
        c = Crawler()
        p = Webpage()
        p.product_name = 'Perfume 212 VIP Rosé Carolina Herrera Feminino - Época Cosméticos'
        self.assertTrue(c._has_product(p))

    def test__has_product_fail(self):
        c = Crawler()
        p = Webpage()
        p.product_name = None
        self.assertFalse(c._has_product(p))

    def test_crawl_connect_db_pass(self):
        dbschema = "test_crawl_connect_db_pass"
        self.setup_db(dbschema)
        session = self.Session()
        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 0)
        result = c.crawl()
        session.close()
        self.assertEqual(result, 0)

    def test_crawl_connect_db_fail(self):
        dbschema = "test_crawl_connect_db_fail"
        c = Crawler(0, 'xxx', 'yyy', 'zzz', 0, dbschema, 0)
        result = c.crawl()
        self.assertEqual(result, 1)

    def test_crawl_process_link_pass(self):
        dbschema = "test_crawl_process_link_pass"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://www.example.com'
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 0)
        result = c.crawl()

        link_list = session.query(Link)
        session.close()

        self.assertEqual(result, 0)
        for link in link_list:
            self.assertEqual(link.url, url)
            self.assertEqual(link.status, Status.visited)

    def test_crawl_process_link_fail(self):
        dbschema = "test_crawl_process_link_fail"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://www.example.com/fail.html'
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 0)
        result = c.crawl()

        link_list = session.query(Link)
        session.close()

        self.assertEqual(result, 0)
        for link in link_list:
            self.assertEqual(link.url, url)
            self.assertEqual(link.status, Status.error)

    def test_crawl_follow_link(self):
        dbschema = "test_crawl_follow_link"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://zero.webappsecurity.com/'
        url_list = ['http://zero.webappsecurity.com/', 'http://zero.webappsecurity.com/index.html']
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 0)
        result = c.crawl()

        link_list = session.query(Link)
        session.close()

        self.assertEqual(result, 0)
        self.assertEqual(len([l for l in link_list]), len(url_list))
        for link in link_list:
            self.assertTrue(link.url in url_list)
            self.assertEqual(link.status, Status.visited)

    def test_crawl_no_follow_link(self):
        dbschema = "test_crawl_no_follow_link"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://www.example.com/'
        no_follow_url = 'http://www.iana.org/domains/example'
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 0)
        result = c.crawl()

        link_list = session.query(Link)
        session.close()

        self.assertEqual(result, 0)
        for link in link_list:
            self.assertNotEqual(link.url, no_follow_url)
            self.assertEqual(link.status, Status.visited)

    def test_crawl_max_depth(self):
        dbschema = "test_crawl_max_depth"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://zero.webappsecurity.com/'
        url_list = ['http://zero.webappsecurity.com/']
        link = Link(url)
        session.add(link)
        session.commit()

        max_depth = 1
        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, max_depth)
        result = c.crawl()

        link_list = session.query(Link)
        session.close()

        self.assertEqual(result, 0)
        self.assertEqual(len([l for l in link_list]), len(url_list))
        for link in link_list:
            self.assertTrue(link.url in url_list)
            self.assertEqual(link.status, Status.visited)

    def test_crawl_product_found(self):
        dbschema = "test_crawl_product_found"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://www.epocacosmeticos.com.br/212-vip-rose-eau-de-parfum-carolina-herrera-perfume-feminino/p'
        title = 'Perfume 212 VIP Rosé Carolina Herrera Feminino - Época Cosméticos'
        name = '212 VIP Rosé Carolina Herrera - Perfume Feminino - Eau de Parfum'
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 1)
        result = c.crawl()

        product_list = session.query(Product)
        session.close()

        self.assertEqual(result, 0)
        for product in product_list:
            self.assertEqual(product.url, url)
            self.assertEqual(product.title, title)
            self.assertEqual(product.name, name)

    def test_crawl_no_product(self):
        dbschema = "test_crawl_no_product"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://www.epocacosmeticos.com.br/perfumes'
        link = Link(url)
        session.add(link)
        session.commit()

        c = Crawler(0, 'crawler', 'abc123', 'localhost', 0, dbschema, 1)
        result = c.crawl()

        product_list = session.query(Product)
        session.close()

        self.assertEqual(result, 0)
        self.assertEqual(len([l for l in product_list]), 0)
