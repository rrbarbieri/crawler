# Changes in dispy package to allow multicast connection on Windows

It fixes IGMP issue that prevents multicast connection on Windows. Both **dispynode.py (Server)** and **dispy (Client)** fail with the following error message:

    OSError: [WinError 10049] O endereço solicitado não é válido no contexto

### Installation
In order to solve this issue, copy the files in this directory to dispy package installation directory:

    .\__init__.py       ->       %PY_HOME%\Lib\site-packages\dispy
    .\dispynode.py

#### References

* http://dispy.sourceforge.net/index.html
* https://pycos.sourceforge.io/dispycos.html
* https://rodrigoesilva.wordpress.com/2012/03/21/erros-codigos-de-erros-socket-tcp/
* https://msdn.microsoft.com/en-gb/library/windows/desktop/ms740668(v=vs.85).aspx
* http://www.nealc.com/blog/blog/2012/09/11/testing/
* https://memoria.rnp.br/newsgen/0111/mld5.html
* https://social.technet.microsoft.com/Forums/windows/pt-BR/0d0da348-3b8b-4790-8aa2-60740a02536f/windows-7-and-igmp-multicast?forum=w7itpronetworking
* https://technet.microsoft.com/pt-br/library/cc787891(v=ws.10).aspx
* https://www.cellstream.com/intranet/reference-reading/tipsandtricks/121-ipv6-windowslinux-command-line-examples.html
* http://colorconsole.de/cmd/en/Windows_7/netsh/interface/ipv6/set/global.htm

#### Changes implemented in dispy package

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
