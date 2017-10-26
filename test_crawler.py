from unittest import TestCase

import os
from sqlalchemy import (create_engine)
from crawler import Crawler
from crawler_db import (Base, Status, Link, Product)
from crawler_web import Webpage


class TestCrawler(TestCase):

    # setup database for testing
    def setup_db(self):
        # get database connection URL from DBURL environment variable
        uri = os.environ['DBURL']
        self.engine = create_engine(uri)

        self.engine.execute("CREATE DATABASE IF NOT EXISTS crawler")
        self.engine.execute("USE crawler")

    # teardown of test database
    def teardown_db(self):
        self.drop_db()
        self.engine.dispose()

    # create database
    def create_db(self):
        Base.metadata.create_all(self.engine)

    # drop database
    def drop_db(self):
        Base.metadata.drop_all(self.engine)

    def test__pre_visit_url_condense_pass(self):
        c = Crawler()
        self.assertEqual(c._pre_visit_url_condense('http://www.example.com/path/file.html#test'),
                         'http://www.example.com/path/file.html')

    def test__same_host_pass(self):
        c = Crawler()
        c.host = 'www.example.com'
        self.assertTrue(bool(c._same_host('http://www.example.com/path/file.html')))

    def test__same_host_fail(self):
        c = Crawler()
        c.host = 'www.example.com'
        self.assertFalse(bool(c._same_host('http:/yourname.xyz/path/file.html')))

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
        # set DBURL environment variable with database connection URL
        self.setup_db()
        self.create_db()
        dbuser = 'crawler'
        dbpass = 'abc123'
        dbhost = 'localhost'
        dbport = 0
        c = Crawler(0, dbuser, dbpass, dbhost, dbport)
        c.crawl()
        self.teardown_db()

    def test_crawl_connect_db_fail(self):
        # set DBURL environment variable with database connection URL
        self.setup_db()
        self.create_db()
        dbuser = 'xxx'
        dbpass = 'yyy'
        dbhost = 'zzz'
        dbport = 0
        c = Crawler(0, dbuser, dbpass, dbhost, dbport)
        c.crawl()
        self.teardown_db()
