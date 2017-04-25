#!/usr/bin/python

"""netudpcomm.py: Class implementing the object to send and receive UDP messages"""

import socket
import time

from classes.netutils import NetUtils

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NetUDPComm(object):
    _sock = None

    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self._sock.bind(("", 0))

    def send_message(self, dest_ip_address, dest_port, message):
        if dest_ip_address == NetUtils.get_broadcast_address():
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else:
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)

        self._sock.sendto(message, (dest_ip_address, dest_port))

    def read_messages(self, message_length, wait_time):
        messages = []

        self._sock.settimeout(wait_time)

        while True:
            try:
                data, addr = self._sock.recvfrom(message_length)

                if data is not None:
                    messages.append(data)

            except socket.timeout:
                return messages
