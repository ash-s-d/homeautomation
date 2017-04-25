"""picameralistener.py: Class implementing a the Pi Camera server socket listener"""

import socket
import threading
import time

from classes.netutils import NetUtils

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeListener(threading.Thread):
    _DISCOVER_CMD = "LINK_NODE"
    _STOP_CMD = "STOP_NODE"

    def __init__(self, name, port):
        threading.Thread.__init__(self)

        self.daemon = False

        self._stopped_flag = threading.Event()

        self._name = name
        self._port = port

        self._ip_address = NetUtils.get_ip_address()
        self._mac_address = NetUtils.get_mac_address()

    def stopped(self):
        return self._stopped_flag.is_set()

    def _get_info(self):
        return self._ip_address + "," + self._mac_address + "," + self._name
