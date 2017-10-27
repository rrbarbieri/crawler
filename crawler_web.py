class OpaqueDataException(Exception):
    def __init__(self, message, mimetype, url):
        Exception.__init__(self, message)
        self.mimetype = mimetype
        self.url = url


class Webpage(object):
    # retrieves and interprets web pages
    def __init__(self, url=''):
        self.url = url
        self.product_name = None
        self.title = None
        self.out_urls = []

    def _open(self):
        import urllib.request

        url = self.url
        try:
            request = urllib.request.Request(url)
            handle = urllib.request.build_opener()
        except IOError:
            return None
        return request, handle

    def fetch(self):
        import re
        import urllib.parse
        import urllib.error
        from html import escape
        from bs4 import BeautifulSoup

        request, handle = self._open()
        if handle:
            try:
                data = handle.open(request)
                mime_type = data.info().get_content_type()
                url = data.geturl()
                if mime_type != "text/html":
                    raise OpaqueDataException("Not interested in files of type %s" % mime_type,
                                              mime_type, url)
                content = str(data.read(), "utf-8", errors="replace")
                soup = BeautifulSoup(content, "html.parser")

                product_name = soup.find("div", {"class": re.compile(r"(?i)product(?:name|title)")})
                if product_name is not None:
                    self.product_name = product_name.renderContents().decode('utf-8')

                title = soup('title')[0]
                if title is not None:
                    self.title = title.renderContents().decode('utf-8')

                tags = soup('a')

            except urllib.error.HTTPError as error:
                if error.code == 404:
                    print("ERROR: %s -> %s" % (error, error.url))
                else:
                    print("ERROR: %s" % error)
                return False
            except urllib.error.URLError as error:
                print("ERROR: %s" % error)
                return False
            except OpaqueDataException:
                return False

            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urllib.parse.urljoin(self.url, escape(href))
                    if url not in self.url and bool(urllib.parse.urlparse(url).netloc):
                        self.out_urls.append(url)
            return True
