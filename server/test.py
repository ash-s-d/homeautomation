#!/usr/bin/python

import configparser
import json
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.dbmodel import Base, Camera, User, WifiBridge, Zone
from classes.milightcontroller import MilightController
from classes.milightcontroller import MilightControllerException

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()

settings.read("settings.ini")

engine = create_engine("sqlite:///" + settings.get("General", "DatabaseFile"))

Base.metadata.bind = engine
 
Session = sessionmaker(bind=engine)

session = Session()

for user in session.query(User):
    print user.password

bridge = session.query(WifiBridge).filter(Zone.id == "1").one()

print bridge.mac_address

# milight_controller = MilightController(
#     int(settings.get("MiLight", "Port")),
#     int(settings.get("MiLight", "AdminPort")),
#     json.loads(settings.get("MiLight", "DiscoveryMessages")),
#     int(settings.get("MiLight", "DiscoveryWaitTime")),
#     json.loads(settings.get("MiLight", "Commands"))
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
