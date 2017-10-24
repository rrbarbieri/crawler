# crawler
Distributed web crawler in Python

# Installation

Install Python latest version in Windows:
	#python 3.6.3 - 2017-10-03
	Python 3.4.4 - 2015-12-21
	https://www.python.org/downloads/windows/
	

Install dispy framework for distributed and parallel computing:
	http://dispy.sourceforge.net/index.html

	pip install dispy
	
Install pywin32 in order for pycos to use efficient polling notifier IOCP in Windows:
	https://sourceforge.net/projects/pywin32/files/pywin32/	
	
Install netifaces for IPv4 and IPv6.

	pip install netifaces
	
	tar xvzf netifaces-0.10.6.tar.gz
	cd netifaces-0.10.6
	python setup.py install

Install psutil on all nodes in order for the availability status (CPU, memory and disk) be sent in status messages, and shown in web browser so cluster/application performance can be monitored.

	pip install psutil


Install beautifulsoup4 for pulling data out of HTML and XML files.

	pip install beautifulsoup4

Install requests for sending all kinds of HTTP requests.

	pip install requests
	certifi-2017.7.27.1 chardet-3.0.4 idna-2.6 requests-2.18.4 urllib3-1.22


Install MySQL database with mysql-connector-python.


Install SQLAlchemy ORM, a comprehensive set of tools for working with databases.

	pip install SQLAlchemy

Install SQLAlchemy-Enum34 that provides a SQLAlchemy type to store values of standard enum.Enum

	pip install SQLAlchemy-Enum34 

Disable VirtualBox or any other virtual machine network adapter.



Changes in dispy package in order to work in Windows:
%PY_HOME%\Lib\site-packages\dispy\__init__.py

    369,373c369,374
    <         if not broadcast:
    <             broadcast = 'ff05::1'
    <    else:
    <         if not broadcast:
    <             broadcast = '<broadcast>'
    ---
    >         # CHANGED
    >         #if not broadcast:
    >         broadcast = 'ff05::1'
    <    else:
    >         #if not broadcast:
    >         broadcast = '<broadcast>'

    804,807c805,809
    <                     if addrinfo.broadcast == '<broadcast>':  # or addrinfo.broadcast == 'ff05::1'
    <                         bind_addr = ''
    <                     else:
    <                         bind_addr = addrinfo.broadcast
    ---
    >                     # CHANGED
    >                     #if addrinfo.broadcast == '<broadcast>':  # or addrinfo.broadcast == 'ff05::1'
    >                     bind_addr = ''
    >                     #else:
    >                     #    bind_addr = addrinfo.broadcast

    836c838,839
    <             udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
    ---
    >             # CHANGED
    >             #udp_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)


%PY_HOME%\Lib\site-packages\dispy\dispynode.py

    363,366c363,367
    <             if addrinfo.broadcast == '<broadcast>':  # or addrinfo.broadcast == 'ff05::1'
    <                 bind_addr = ''
    <             else:
    <                 bind_addr = addrinfo.broadcast
    ---
    >             # CHANGED
    >             #if addrinfo.broadcast == '<broadcast>':  # or addrinfo.broadcast == 'ff05::1'
    >             bind_addr = ''
    >             #else:
    >             #    bind_addr = addrinfo.broadcast
