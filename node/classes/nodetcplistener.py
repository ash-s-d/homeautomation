"""nodetcplistener.py: Class implementing a node socket listener"""

import base64
import json
import socket
import threading
import time

from io import BytesIO

from classes.nodecamera import NodeCamera
from classes.nodelistener import NodeListener

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeTCPListener(NodeListener):
    _CAMERA_GET_IMAGE_CMD = "CAMERA_IMG"
    _CAMERA_FLIP_IMAGE_VER_CMD = "CAMERA_VFLIP"
    _CAMERA_FLIP_IMAGE_HOR_CMD = "CAMERA_HFLIP"

    _resources = None

    def __init__(self, name, port, resources):
        NodeListener.__init__(self, name, port)

        self._resources = resources

        additional_commands = [self._CAMERA_GET_IMAGE_CMD,
                               self._CAMERA_FLIP_IMAGE_VER_CMD, self._CAMERA_FLIP_IMAGE_HOR_CMD]

        (self.request_schema["properties"]["COMMAND"]
         ["enum"]).extend(additional_commands)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(("", self._port))
        sock.listen(1)

        while True:
            conn, (src_addr, recv_port) = sock.accept()

            data = conn.recv(1024)

            try:
                data_json = json.loads(data)

                if self.is_data_valid(data_json):
                    command = data_json["COMMAND"]

                    print "Received message from " + src_addr + " on TCP port " + str(self._port) + ": " + command

                    if command == self._DISCOVER_CMD:
                        print "Sending Pi Camera info to target client " + src_addr + " on TCP port " + str(self._port)

                        conn.sendall(self.generate_response_message(
                            self._get_info(), ""))

                    elif command == self._STOP_CMD:
                        if src_addr == self._ip_address:
                            print "Stopping Pi Camera on TCP port " + str(self._port)

                            self._stopped_flag.set()

                            break

                    else:
                        command_split = command.split("_")

                        if command_split[0] in self._resources:
                            resource = self._resources[command_split[0]]

                            if command == self._CAMERA_GET_IMAGE_CMD:
                                print "Sending Pi Camera snapshot to target client " + src_addr + " on TCP port " + str(self._port)

                                try:
                                    stream = BytesIO()
                                    stream = resource.get_captured_stream(
                                        stream)

                                    stream.seek(0)

                                    conn.sendall(
                                        self.generate_response_message(
                                            {"IMAGE_BASE64": base64.b64encode(stream.getvalue())}, "")
                                    )

                                    stream.close()
                                except socket.error as error:
                                    None
                        else:
                            None
                else:
                    conn.sendall(self.generate_response_message(
                        "", "Invalid command"))

            except ValueError:
                conn.sendall(self.generate_response_message(
                    "", "Ill-formed request"))

            conn.close()

        sock.close()

    def stop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((self._ip_address, self._port))
            sock.sendall("{\"COMMAND\": \"" + self._STOP_CMD + "\"}")
        except socket.error as error:
            None

        sock.close()
