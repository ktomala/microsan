#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *

host = '192.168.2.255'
#host = '192.168.2.103'
port = 20001

dstaddr = (host, port)
#srcaddr = ('127.0.0.1', 1234)
srcaddr = ('192.168.2.5', 0)

#myhost = gethostbyname(

s = socket(AF_INET, SOCK_DGRAM)
s.bind(srcaddr)
#s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#s.connect(srcaddr)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

data = '\x0d\x00\x00\x00'
#s.send(data)

#msg, srv = s.recvfrom(255)
#s.sendall(data)
#s.shutdown(1)

while 1:
    s.sendto(data, dstaddr)
    msg, srv = s.recvfrom(255)
    print '%s: %s' % (srv, msg)

s.close()

#while 1:
#    if not len(buf):
#	break
#    print "Received: %s" % buf
