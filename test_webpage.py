from unittest import TestCase
from crawler_web import Webpage
import urllib.error


class TestWebpage(TestCase):
    def test__open_pass(self):
        url = 'https://httpstat.us/200'
        page = Webpage(url)
        request, handle = page._open()
        if handle:
            try:
                handle.open(request)
            except urllib.error.URLError:
                self.fail('URL error')
            except Exception as e:
                self.fail('Unexpected exception raised:\n' + str(e))
        else:
            self.fail('handle empty')

    def test__open_fail(self):
        url = 'https://httpstat.us/404'
        page = Webpage(url)
        request, handle = page._open()
        if handle:
            try:
                handle.open(request)
                self.fail('URL ok')
            except urllib.error.URLError:
                pass
            except Exception as e:
                self.fail('Unexpected exception raised:\n' + str(e))
        else:
            self.fail('handle empty')

    def test_fetch_pass(self):
        url = 'http://www.example.com/'
        out_urls = ['http://www.iana.org/domains/example']
        page = Webpage(url)
        if page.fetch():
            self.assertEqual(len([l for l in page.out_urls]), len(out_urls))
        else:
            self.fail('URL error')

    def test_fetch_fail(self):
        url = 'https://httpstat.us/404'
        page = Webpage(url)
        if page.fetch():
            self.fail('URL ok')
        else:
            pass
