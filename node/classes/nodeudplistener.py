"""nodeudplistener.py: Class implementing a node udp socket listener"""

import json
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


class NodeUDPListener(NodeListener):

    def __init__(self, name, port):
        NodeListener.__init__(self, name, port)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(("", self._port))

        while True:
            data, (src_addr, recv_port) = sock.recvfrom(1024)

            if data is not None:
                try:
                    data_json = json.loads(data)

                    if self.is_data_valid(data_json):
                        command = data_json["COMMAND"]

                        print "Received message from " + src_addr + " on UDP port " + str(self._port) + ": " + command

                        if command == self._DISCOVER_CMD:
                            print "Sending Pi Camera info to target client " + src_addr + " on UDP port " + str(recv_port)

                            sock.sendto(self.generate_response_message(
                                self._get_info(), ""), (src_addr, recv_port))
                        elif command == self._STOP_CMD:
                            if src_addr == self._ip_address:
                                print "Stopping Pi Camera on UDP port " + str(self._port)

                                self._stopped_flag.set()

                            break
                
                except ValueError:
                    None

        sock.close()

    def stop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.sendto("{\"COMMAND\": \"" + self._STOP_CMD + "\"}", (self._ip_address, self._port))

        sock.close()
