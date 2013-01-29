# -*- coding: utf-8 -*-

"""
MicroSAN Network Module
"""

import socket, traceback

IPADDR_BROADCAST = '<broadcast>'
IPADDR_ANY = ''
SOCK_BUF_SIZE = 8192
SOCK_TIMEOUT = 1

MICROSAN_PORT = 20001
APP_PORT = 51000

class UDPSocket(object):

    def __init__(self, addr = None, reuse_addr = False):
        """
        Create socket for use
        """
        self.buf = []

        if addr is None:
            addr = (IPADDR_ANY, APP_PORT)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if reuse_addr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if addr[0] == IPADDR_ANY:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.sock.settimeout(SOCK_TIMEOUT)

        self.sock.bind(addr)

    def send_data(self, data, addr):
        """
        Sends data
        """
        self.sock.sendto(data, addr)

    def recv_data(self):
        """
        Wait for data
        """
        try:
            message, address = self.sock.recvfrom(SOCK_BUF_SIZE)
            self.buf.append((message, address))
        except (KeyboardInterrupt, SystemExit):
            raise
#        except:
#            traceback.print_exc()

    def get_next_buf(self):
        """
        Return data from buffer
        """
        return self.buf.pop(0)

    def close(self):
        """
        Closes socket
        """
        self.sock.close()

    def clear_buf(self):
        """
        Clears buffer
        """
        self.buf = []

class BroadcastSocket(UDPSocket):

    def __init__(self, addr = None, reuse_addr = True):
        """
        Create socket for use
        """
        super(BroadcastSocket, self).__init__(addr = addr, reuse_addr = reuse_addr)

    def send_data(self, data, addr = None):
        """
        Sends broadcast
        """
        if addr is None:
            addr = (IPADDR_BROADCAST, MICROSAN_PORT)

        super(BroadcastSocket, self).send_data(data, addr)

