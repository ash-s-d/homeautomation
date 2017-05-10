#!/usr/bin/python

"""noded.py: 'Main', or point of entry, code for the home automation node daemon"""


import argparse
import configparser
import json

from classes.nodedaemon import NodeDaemon

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


def main():
    argument_parser = argparse.ArgumentParser(
        description="Launcher for the home automation node daemon")

    argument_parser.add_argument(
        "--start", action='store_true', help="Start node daemon")
    argument_parser.add_argument("--stop", action='store_true',
                                 help="Abort/stop node daemon")
    argument_parser.add_argument(
        "--restart", action='store_true', help="Restart node daemon")

    args = argument_parser.parse_args()

    if not (args.start or args.stop or args.restart):
        argument_parser.error("At least one argument is expected.")
    else:
        settings = configparser.ConfigParser()

        settings.read("settings.ini")

        node_daemon = NodeDaemon(settings.get("General", "Name"), int(settings.get("General", "Port")), int(
            settings.get("General", "AdminPort")), settings.get("General", "PidFile"), json.loads(settings.get("General", "Modules")))

        if (args.start):
            node_daemon.start()
        elif (args.stop):
            node_daemon.stop()
        else:
            node_daemon.restart()

if __name__ == "__main__":
    main()
