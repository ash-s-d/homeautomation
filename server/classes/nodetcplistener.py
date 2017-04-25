"""picameratcplistener.py: Class implementing a the Pi Camera server socket listener"""

import socket
import threading
import time

from classes.nodelistener import NodeListener

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeTCPListener(NodeListener):
    _IMAGE_CMD = "IMAGE_NODE"

    def __init__(self, name, port):
        NodeListener.__init__(self, name, port)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(("", self._port))
        sock.listen(1)

        while True:
            conn, (src_addr, recv_port) = sock.accept()
            data = conn.recv(1024)

            print "Received message from " + src_addr + " on TCP port " + str(self._port) + ": " + data

            if data == self._DISCOVER_CMD:
                print "Sending Pi Camera info to target client " + src_addr + " on TCP port " + str(self._port)

                conn.send(self._get_info())
            if data == self._IMAGE_CMD:
                print "Sending Pi Camera snapshot to target client " + src_addr + " on TCP port " + str(self._port)

                conn.send("IMAGE_SENDING")
                # To implement
            elif data == self._STOP_CMD:
                if src_addr == self._ip_address:
                    print "Stopping Pi Camera on TCP port " + str(self._port)

                    conn.close()

                    self._stopped_flag.set()

                    break

        sock.close()

    def stop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self._ip_address, self._port))
            sock.send(self._STOP_CMD)
        except socket.error as error:
            None

        sock.close()
