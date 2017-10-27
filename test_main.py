from test_dbhandler import DBHandler

from crawler import *
from crawler_db import (Status, Link, Product)

import csv
import shutil
import tempfile
from os import path


class TestMain(DBHandler):

    # overload __init__
    def __init__(self, *args, **kwargs):
        # generate temporary directory
        self.test_dir = tempfile.mkdtemp()
        DBHandler.init_engine(self)
        DBHandler.__init__(self, *args, **kwargs)

    def __del__(self):
        # remove temporary directory
        shutil.rmtree(self.test_dir)
        DBHandler.del_engine(self)

    def test_main_connect_db_pass(self):
        dbschema = "test_main_connect_db_pass"
        url = 'http://www.example.com/'
        exit_code = main(['-U', 'crawler', '-p', 'abc123', '-s', dbschema, url])
        self.assertEqual(exit_code, 0)

    def test_main_connect_db_fail(self):
        dbschema = "test_main_connect_db_fail"
        url = 'http://www.example.com/'
        exit_code = main(['-U', 'xxx', '-p', 'yyy', '-s', dbschema, url])
        self.assertEqual(exit_code, 1)

    def test_main_args_pass(self):
        dbschema = "test_main_args_pass"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://zero.webappsecurity.com/'
        url_list = ['http://zero.webappsecurity.com/', 'http://zero.webappsecurity.com/index.html']

        exit_code = main(['-U', 'crawler', '-p', 'abc123', '-s', dbschema, url])

        link_list = session.query(Link)
        session.close()

        self.assertEqual(exit_code, 0)
        self.assertEqual(len([l for l in link_list]), len(url_list))
        for link in link_list:
            self.assertTrue(link.url in url_list)
            self.assertEqual(link.status, Status.visited)

    def test_main_urlfile_pass(self):
        dbschema = "test_main_urlfile_pass"
        self.setup_db(dbschema)
        session = self.Session()

        url = 'http://zero.webappsecurity.com/'
        url_list = ['http://zero.webappsecurity.com/', 'http://zero.webappsecurity.com/index.html']

        urlfile = 'urlfile.txt'
        urlfile_path = path.join(self.test_dir, urlfile)
        with open(urlfile_path, 'w') as f:
            f.write(url)

        exit_code = main(['-U', 'crawler', '-p', 'abc123', '-s', dbschema, '-u', urlfile_path])

        link_list = session.query(Link)
        session.close()

        self.assertEqual(exit_code, 0)
        self.assertEqual(len([l for l in link_list]), len(url_list))
        for link in link_list:
            self.assertTrue(link.url in url_list)
            self.assertEqual(link.status, Status.visited)

    def test_main_urlfile_fail(self):
        dbschema = "test_main_urlfile_fail"
        self.setup_db(dbschema)
        session = self.Session()

        urlfile_path = 'urlfile.txt'
        exit_code = main(['-U', 'crawler', '-p', 'abc123', '-s', dbschema, '-u', urlfile_path])

        link_list = session.query(Link)
        session.close()

        self.assertEqual(exit_code, 1)
        self.assertEqual(len([l for l in link_list]), 0)

    def test_main_resume_pass(self):
        dbschema = "test_main_resume_pass"
        self.setup_db(dbschema)
        session = self.Session()

        url_list = ['http://zero.webappsecurity.com/', 'http://zero.webappsecurity.com/index.html']
        links = []
        for url in url_list:
            links.append(Link(url, status=Status.new))
        session.add_all(links)
        session.commit()

        exit_code = main(['-r', '-U', 'crawler', '-p', 'abc123', '-s', dbschema])

        link_list = session.query(Link)
        session.close()

        self.assertEqual(exit_code, 0)
        self.assertEqual(len([l for l in link_list]), len(url_list))
        for link in link_list:
            self.assertTrue(link.url in url_list)
            self.assertEqual(link.status, Status.visited)

    def test_main_csvfile_pass(self):
        dbschema = "test_main_csvfile_pass"
        self.setup_db(dbschema)
        session = self.Session()

        product_data = [['http://www.epocacosmeticos.com.br/acqua-di-gio-homme-eau-de-toilette-giorgio-armani-perfume-masculino/p',
         'Perfume Acqua Di Giò Homme Giorgio Armani Masculino - Época Cosméticos',
         'Acqua Di Giò Homme Giorgio Armani - Perfume Masculino - Eau de Toilette'],
        ['http://www.epocacosmeticos.com.br/amor-amor-l-eu-flamingo-cacharel-perfume-feminino-eau-de-toilette/p',
         'Perfume - Amor Amor L’eau Flamingo Cacharel Feminino - Época Cosméticos',
         'Amor Amor L’eau Flamingo Cacharel - Perfume Feminino Eau de Toilette - 50ml'],
        ['http://www.epocacosmeticos.com.br/amplexe-antiqueda-ada-tina-tratamento-antiqueda/p',
         'Amplexe Loção Antiqueda Ada Tina - Época Cosméticos',
         'Amplexe Antiqueda Ada Tina - Tratamento Antiqueda - 50ml']]

        products = []
        for product in product_data:
            products.append(Product(product[0], product[1], product[2]))
        session.add_all(products)
        session.commit()
        session.close()

        csvfile = 'outfile.csv'
        csvfile_path = path.join(self.test_dir, csvfile)

        exit_code = main(['-r', '-U', 'crawler', '-p', 'abc123', '-s', dbschema, '-c', csvfile_path])

        product_list = []
        with open(csvfile_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                product_list.append(row)

        self.assertEqual(exit_code, 0)
        self.assertEqual(product_data, product_list)
