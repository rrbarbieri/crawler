#!/usr/bin/env python

class Crawler(object):
    def __init__(self, i, dbuser, dbpass, dbhost, dbport):

        self.i = i

        # database connection
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost
        self.dbport = dbport

        self.num_processed = 0  # Links processed

        # Pre-visit filters:  only visit a URL if it passes these tests
        self.pre_visit_filters = [self._same_host]

        # Product filters:  when examining a visited page, only process
        # links where the target matches these filters.
        self.product_filters = [self._has_product]

    def _pre_visit_url_condense(self, url):
        import urllib.parse

        base, frag = urllib.parse.urldefrag(url)
        return base

    # URL Filtering functions.  These all use information from the
    # state of the Crawler to evaluate whether a given URL should be
    # used in some context.  Return value of True indicates that the
    # URL should be used.

    def _same_host(self, url):
        import re
        import urllib.parse

        # pass if the URL is on the same host as the root URL
        try:
            host = urllib.parse.urlparse(url)[1]
            return re.match(".*%s" % self.host, host)
        except Exception as e:
            print("ERROR: Can't process url '%s' (%s)" % (url, e))
            return False

    def _has_product(self, page):
        # pass if the URL has a product
        return bool(page.product_name and page.product_name.strip())

    def crawl(self):
        # executed on node when running in cluster mode
        # variables declared below, including imported modules,
        # are available only in jobs running in cluster nodes
        import math
        import re
        import enum
        import time
        import urllib.error
        import urllib.parse
        import urllib.request
        from html import escape
        from bs4 import BeautifulSoup

        from sqlalchemy import (create_engine, Column, Integer, String, exc)
        from sqlalchemy.engine.url import URL
        from sqlalchemy.orm import Session
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy_enum34 import EnumType

        Base = declarative_base()

        class Status(enum.Enum):
            new = 'new'
            visited = 'visited'
            error = 'error'

        # declare Link database table
        class Link(Base):
            __tablename__ = 'link'

            depth = Column(Integer, primary_key=True)
            url = Column(String(1022), primary_key=True)
            status = Column(EnumType(Status, name='url_status'), nullable=False, default=Status.new, index=True)

            def __init__(self, url, depth=1, status=Status.new):
                self.url = url
                self.depth = depth
                self.status = status

        # declare Product database table
        class Product(Base):
            __tablename__ = 'product'
            url = Column(String(1022), primary_key=True)
            title = Column(String(256), nullable=False)
            name = Column(String(256), nullable=False)

            def __init__(self, url, title, name):
                self.url = url
                self.title = title
                self.name = name

        class OpaqueDataException(Exception):
            def __init__(self, message, mimetype, url):
                Exception.__init__(self, message)
                self.mimetype = mimetype
                self.url = url

        class Webpage(object):
            # retrieves and interprets web pages
            def __init__(self, url):
                self.url = url
                self.product_name = None
                self.title = None
                self.out_urls = []

            def _open(self):
                url = self.url
                try:
                    request = urllib.request.Request(url)
                    handle = urllib.request.build_opener()
                except IOError:
                    return None
                return (request, handle)

            def fetch(self):
                request, handle = self._open()
                # self._addHeaders(request)
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
                        tags = []
                    except urllib.error.URLError as error:
                        print("ERROR: %s" % error)
                        tags = []
                    except OpaqueDataException as error:
                        tags = []

                    for tag in tags:
                        href = tag.get("href")
                        if href is not None:
                            url = urllib.parse.urljoin(self.url, escape(href))
                            if url not in self.url and bool(urllib.parse.urlparse(url).netloc):
                                self.out_urls.append(url)

        # connect to database
        engine = create_engine(URL("mysql+mysqlconnector",
                                   username=self.dbuser,
                                   password=self.dbpass,
                                   host=self.dbhost,
                                   port=self.dbport
                                   ))

        engine.execute("USE crawler")  # select db
        session = Session(engine)

        sTime = time.time()

        # Process same site first
        link = session.query(Link).filter(Link.depth > 1, Link.status==Status.new).with_for_update().first()
        if not link:
            link = session.query(Link).filter_by(status=Status.new).with_for_update().first()

        while link:
            this_url = link.url
            link_depth = link.depth + 1
            self.num_processed += 1
            self.host = urllib.parse.urlparse(this_url)[1]

            status = Status.visited
            try:
                page = Webpage(this_url)
                page.fetch()
                for link_url in [self._pre_visit_url_condense(l) for l in page.out_urls]:
                    # apply pre-visit filters.
                    do_not_follow = [f for f in self.pre_visit_filters if not f(link_url)]

                    # if no filters failed, process URL
                    if [] == do_not_follow:
                        new_link = Link(link_url, depth=link_depth)
                        session.begin_nested() # establish a savepoint
                        session.add(new_link)
                        try:
                            session.flush()
                        except exc.IntegrityError: # rollback duplicated entry
                            session.rollback()
                            continue
                        except:
                            session.rollback()
                            raise
                        session.commit()

                # apply product filters.
                is_product = [f for f in self.product_filters if not f(page)]

                # if no filters failed, process product
                if [] == is_product:
                    product = Product(this_url, title=page.title, name=page.product_name)
                    session.begin_nested()  # establish a savepoint
                    session.add(product)
                    try:
                        session.flush()
                    except:
                        session.rollback()
                        raise
                    session.commit()


            except Exception as e:
                print("ERROR: Can't process url '%s' (%s)" % (this_url, e))
                status = Status.error

            link.status = status
            session.commit()

            # process same site first
            link = session.query(Link).filter(Link.depth > 1, Link.status == Status.new).with_for_update().first()
            if not link:
                link = session.query(Link).filter_by(status=Status.new).with_for_update().first()

        eTime = time.time()
        tTime = eTime - sTime

        print("\tProcessed:    %d" % self.num_processed)
        print("\tStats:        %d/s after %0.2fs" % (
            int(math.ceil(float(self.num_processed) / tTime)), tTime))

        session.close()
        engine.dispose()


def parse_options():
    import optparse
    import sys

    # parse any given command-line options returning
    # both the parsed options and arguments.
    parser = optparse.OptionParser()

    parser.add_option("-u", "--urlfile",
                      action="store", type="string", dest="urlfile",
                      help="File with URL list to crawl")

    parser.add_option("-c", "--csvfile",
                      action="store", type="string", dest="csvfile",
                      help="CSV File to write product list")

    parser.add_option("-U", "--dbuser",
                      action="store", type="string", dest="dbuser",
                      help="Database user"),

    parser.add_option("-p", "--dbpass",
                      action="store", type="string", dest="dbpass",
                      help="Database password"),

    parser.add_option("-H", "--dbhost",
                      action="store", type="string", dest="dbhost",
                      default="localhost", help="Database host name"),

    parser.add_option("-P", "--dbport",
                      action="store", type="string", dest="dbport",
                      help="Database port"),

    parser.add_option("-r", "--resume", action="store_true", dest="resume",
                      default=False, help="Resume previous crawl after an interruption")

    parser.add_option("-j", "--cluster-jobs",
                      action="store", type="int", dest="cluster_jobs",
                      default=0, help="Number of jobs to run in cluster nodes")

    opts, args = parser.parse_args()

    if not opts.resume and ((len(args) < 1 and not opts.urlfile) or (len(args) > 0 and opts.urlfile)):
        parser.print_help(sys.stderr)
        parser.error("pass an URL as an argument or use option -f")
        raise SystemExit(1)

    if  opts.resume and (len(args) > 0 or opts.urlfile):
        parser.print_help(sys.stderr)
        parser.error("option -r cannot be used with option -f nor with an argument")
        raise SystemExit(1)

    return opts, args


# function 'compute' is distributed and executed with arguments
# supplied with 'cluster.submit' below
def compute(obj):
    # obj is an instance of Crawler
    obj.crawl()  # the output is stored in job.stdout


def main():
    # executed on client only
    # variables declared below, including imported modules,
    # are not available in jobs running in cluster nodes
    import dispy
    import sys
    import enum
    import csv

    from sqlalchemy import (create_engine, Column, Integer, String, exc)
    from sqlalchemy.engine.url import URL
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy_enum34 import EnumType

    Base = declarative_base()

    class Status(enum.Enum):
        new = 'new'
        visited = 'visited'
        error = 'error'

    # declare Link database table
    class Link(Base):
        __tablename__ = 'link'

        depth = Column(Integer, primary_key=True)
        url = Column(String(1022), primary_key=True)
        status = Column(EnumType(Status, name='url_status'), nullable=False, default=Status.new, index=True)

        def __init__(self, url, depth=1, status=Status.new):
            self.url = url
            self.depth = depth
            self.status = status

    # declare Product database table
    class Product(Base):
        __tablename__ = 'product'
        url = Column(String(1022), primary_key=True)
        title = Column(String(256), nullable=False)
        name = Column(String(256), nullable=False)

        def __init__(self, url, title, name):
            self.url = url
            self.title = title
            self.name = name

    # parse command line options
    opts, args = parse_options()

    urlfile = opts.urlfile
    csvfile = opts.csvfile
    dbuser = opts.dbuser
    dbpass = opts.dbpass
    dbhost = opts.dbhost
    dbport = opts.dbport
    resume = opts.resume
    cluster_jobs = opts.cluster_jobs

    # connect to database
    engine = create_engine(URL("mysql+mysqlconnector",
        username=dbuser,
        password=dbpass,
        host=dbhost,
        port=dbport
        ))

    # create database schema
    engine.execute("CREATE DATABASE IF NOT EXISTS crawler")
    engine.execute("USE crawler")

    # if resume previous crawl, do not clean database
    if not resume:
        # read file with URL list
        if urlfile:
            try:
                with open(urlfile, 'r') as file:
                    url_list = [line.strip() for line in file.readlines()]
                if not url_list:
                    print ("No data in file %s" % urlfile)
                    raise SystemExit(1)
                print("Read file %s" % urlfile)
            except IOError as error:
                print("I/O error({0}): {1}".format(error.errno, error.strerror))
                raise SystemExit(1)
            except: # handle other exceptions such as attribute errors
                print("Unexpected error:", sys.exc_info()[0])
                raise SystemExit(1)
        else:
            # URL in command line argument
            url_list=[args[0]]

        # clean database
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        session = Session(engine)

        # insert URL list into database
        links = []
        for url in url_list:
            links.append(Link(url))
        session.add_all(links)
        session.commit()

        session.close()

    # run in cluster mode
    if cluster_jobs > 0:
        # 'compute' needs definition of class Crawler
        cluster = dispy.JobCluster(compute, depends=[Crawler])
        jobs = []
        for i in range(cluster_jobs):
            crawler = Crawler(i, dbuser, dbpass, dbhost, dbport)  # create object of Crawler
            job = cluster.submit(crawler) # it is sent to a node for executing 'compute'
            job.id = crawler # store this object for later use
            jobs.append(job)

        # waits until all jobs finish
        for job in jobs:
            job() # wait for job to finish
            print('Job %s:\n%s' % (job.id.i, job.stdout))
    else: # run in standalone mode
        crawler = Crawler(0, dbuser, dbpass, dbhost, dbport)
        crawler.crawl()

    # write product list to .csv file
    if csvfile:
        if not csvfile.lower().endswith('.csv'):
            csvfile += '.csv'
        try:
            with open(csvfile, 'w', newline='') as outfile:
                writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

                session = Session(engine)
                # paginate results
                rows_per_page = 50
                page_number = 0
                dbquery = session.query(Product)

                products = dbquery.limit(rows_per_page).offset(page_number * rows_per_page).all()
                while products:
                    for product in products:
                        writer.writerow([product.url, product.title, product.name])

                    page_number += 1
                    products = dbquery.limit(rows_per_page).offset(page_number * rows_per_page).all()

            print("Write file %s" % csvfile)
        except IOError as error:
            print("I/O error({0}): {1}".format(error.errno, error.strerror))
            raise SystemExit(1)
        except: # handle other exceptions such as attribute errors
            print("Unexpected error:", sys.exc_info()[0])
            raise SystemExit(1)

        session.close()

    engine.dispose()


if __name__ == "__main__":
    main()
