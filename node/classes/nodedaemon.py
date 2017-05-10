"""nodedaemon.py: Class implementing the daemon logic for socket interactions with a node, e.g. a RPI Zero W"""

import signal
import socket
import threading
import time

from classes.daemon import Daemon
from classes.netutils import NetUtils
from classes.nodecamera import NodeCamera
from classes.nodetcplistener import NodeTCPListener
from classes.nodeudplistener import NodeUDPListener

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeDaemon(Daemon):
    _name = None
    _ports = None
    _admin_port = None
    _modules_settings = None

    _threads = None
    _resources = None

    _end = None

    def __init__(self, name, port, admin_port, path_to_pid_file, modules_settings):
        Daemon.__init__(self, path_to_pid_file)

        self._name = name
        self._port = port
        self._admin_port = admin_port
        self._modules_settings = modules_settings

        self._threads = []
        self._resources = {}

        self._end = False

        signal.signal(signal.SIGTERM, self.terminate)

    def run(self):
        if "CAMERA" in self._modules_settings:
            self._resources["CAMERA"] = NodeCamera(self._modules_settings["CAMERA"])

        tcp_listener = NodeTCPListener(self._name, self._port, self._resources)
        admin_tcp_listener = NodeTCPListener(
            self._name, self._admin_port, self._resources)
        udp_listener = NodeUDPListener(self._name, self._admin_port)

        self._threads.append(tcp_listener)
        self._threads.append(admin_tcp_listener)
        self._threads.append(udp_listener)

        tcp_listener.start()
        admin_tcp_listener.start()
        udp_listener.start()

        while True:
            time.sleep(.5)

            if self._end:
                break

    def terminate(self, signum, stack):
        for thread in self._threads:
            if not thread.stopped():
                thread.stop()

            thread.join()

        for resource_identifier in self._resources:
            self._resources[resource_identifier].close()

        self._end = True
