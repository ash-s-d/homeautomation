"""nodedaemon.py: Class implementing the daemon logic for socket interactions with a node, e.g. a RPI Zero W"""

import socket
import threading
import time

from classes.netutils import NetUtils
from classes.nodetcplistener import NodeTCPListener
from classes.nodeudplistener import NodeUDPListener

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeDaemon(object):
    _name = None
    _ports = None
    _admin_port = None

    _listener_threads = None

    def __init__(self, name, port, admin_port):
        self._name = name
        self._port = port
        self._admin_port = admin_port

        self._listener_threads = []

    def start_up(self):
        tcp_listener = NodeTCPListener(self._name, self._port)
        admin_tcp_listener = NodeTCPListener(self._name, self._admin_port)
        udp_listener = NodeUDPListener(self._name, self._admin_port)

        self._listener_threads.append(tcp_listener)
        self._listener_threads.append(admin_tcp_listener)
        self._listener_threads.append(udp_listener)

        tcp_listener.start()
        admin_tcp_listener.start()
        udp_listener.start()

        # try:
        #     while True:
        #         time.sleep(.5)
        # except KeyboardInterrupt:
        #     self.shut_down()

    def shut_down(self):
        for listerner_thread in self._listener_threads:
            if not listerner_thread.stopped():
                listerner_thread.stop() 
            else:
                print "Thread already stopped"

            listerner_thread.join()