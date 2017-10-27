# crawler
This is a distributed web crawler application in Python that crawls shopping sites and collects information about the selling products.

It can either run in standalone mode in a single computer or in a cluster as a distributed application on multiple computers within a network. In cluster mode, the site information collected and stored in a database is available for processing of every job running in the nodes of the cluster. In case of an interruption, the process can be resumed at any time without loss of data.

The URL of the site to visit are passed as an argument or, instead, a list of URLs are passed in a file as a command-line option. The links followed in every page visited are stored as distinct entries in a database table so that they are not revisited. The stored links can be processed in parallel for any of the jobs in the cluster. Once selected, a link will not be available for the other jobs of the cluster, although the processing job can crawl and store new links of the visited page and then these links will be available for those other jobs. If the visited page corresponds to that of a selling product then its information will be stored in another database table. A link will be considered visited when all the collected information of the visited page is successfully collected and stored, including those of an eventual selling product. The application jobs in the cluster finish execution when there is no further links to visit.

A .csv file with a list of the found products can be generated at the end.

### Installation

**Attention:** In case of Windows installation, refer to dispy/README.md.

* Install latest version of Python which has a MySQL Connector/Python available for it. Please check MySQL Connector/Python download (https://dev.mysql.com/downloads/connector/python/) for available versions.

    Python 3.4.4 - 2015-12-21 for Windows (https://www.python.org/downloads/windows/)

* Install dispy framework for distributed and parallel computing:
    http://dispy.sourceforge.net/index.html

	    pip install dispy
	
* Download and install pywin32 in order for pycos to use efficient polling notifier IOCP in Windows:
	https://sourceforge.net/projects/pywin32/files/pywin32/	
	
* Install netifaces for IPv4 and IPv6.

        pip install netifaces

* Install psutil on all nodes in order for the availability status (CPU, memory and disk) be sent in status messages, and shown in web browser so cluster/application performance can be monitored.

	    pip install psutil

* Install beautifulsoup4 for pulling data out of HTML and XML files.

	    pip install beautifulsoup4

* Install requests for sending all kinds of HTTP requests (certifi-2017.7.27.1 chardet-3.0.4 idna-2.6 requests-2.18.4 urllib3-1.22)

        pip install requests

* Install MySQL database with mysql-connector-python (https://www.mysql.com/downloads/)

* Install SQLAlchemy ORM, a comprehensive set of tools for working with databases.

	    pip install SQLAlchemy

* Install SQLAlchemy-Enum34 that provides a SQLAlchemy type to store values of standard enum.Enum

	    pip install SQLAlchemy-Enum34

* Disable VirtualBox adapter or any other virtual machine network adapter so that dispy will not select it for connection.

### Execution

**crawler.py** can either run in standalone mode or in cluster mode. To run in cluster mode, install the above python packages in the cluster nodes as well and then invoke **dispynode.py --clean** in every node. Please refer to **dispynode (Server)** (http://dispy.sourceforge.net/dispynode.html) for more options.

Launch **crawler.py** with the following options:

e.g. **crawler.py -U crawler -p abc123 'http://www.example.com/'**

In the above example, the database user 'crawler' must have privileges to create and drop schemas and tables.

    Usage: crawler.py [options]

    Options:
      -h, --help            show this help message and exit
      -u URLFILE, --urlfile=URLFILE
                            File with URL list to crawl
      -c CSVFILE, --csvfile=CSVFILE
                            CSV File to write product list
      -U DBUSER, --dbuser=DBUSER
                            Database user
      -p DBPASS, --dbpass=DBPASS
                            Database password
      -H DBHOST, --dbhost=DBHOST
                            Database host name
      -P DBPORT, --dbport=DBPORT
                            Database port
      -s DBSCHEMA, --dbschema=DBSCHEMA
                            Database schema
      -d DEPTH, --depth=DEPTH
                            Maximum depth to traverse
      -r, --resume          Resume previous crawl after an interruption
      -j CLUSTER_JOBS, --cluster-jobs=CLUSTER_JOBS
                            Number of jobs to run in cluster nodes
