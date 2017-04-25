#!/usr/bin/python

import configparser
import json
import sys
import time

from classes.netutils import NetUtils
from classes.netudpcomm import NetUDPComm
from classes.milightcontroller import MilightController
from classes.milightcontroller import MilightControllerException
from classes.nodedaemon import NodeDaemon
from classes.homeautomationdatastore import HomeAutomationDataStore

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()

settings.read("settings.ini")

# data_store = HomeAutomationDataStore(
#     settings.get("General", "DatabaseFile"))

# milight_controller = MilightController(
#     int(settings.get("MiLight", "Port")),
#     int(settings.get("MiLight", "AdminPort")),
#     json.loads(settings.get("MiLight", "DiscoveryMessages")),
#     int(settings.get("MiLight", "DiscoveryWaitTime")),
#     json.loads(settings.get("MiLight", "Commands")),
#     data_store
# )

# try:
#     if len(sys.argv) > 2:
#         milight_controller.send_command(1, sys.argv[1], sys.argv[2])
#     else:
#         if sys.argv[1].upper() == "DISCOVER":
#             milight_controller.discover_wifi_bridges()
#         else:
#             milight_controller.send_command(1, sys.argv[1])

# except MilightControllerException as error:
#     print error

node_daemon = NodeDaemon("Pi Camera 1", int(settings.get(
    "Camera", "Port")), int(settings.get("Camera", "AdminPort")))
node_daemon.start_up()
