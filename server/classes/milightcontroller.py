#!/usr/bin/python

"""milightcontroller.py: Class implementing the object to interact with the Mi-light/Limitless wi-fi bridge"""

import binascii
import copy

from classes.homeautomationdatastore import HomeAutomationDataStore
from classes.netudpcomm import NetUDPComm
from classes.netutils import NetUtils

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class MilightController(object):
    _port = None
    _admin_port = None
    _discovery_msgs = None
    _discovery_wait_time = None
    _commands = None
    _data_store = None

    _net_udp_comm = None

    def __init__(self, port, admin_port, discovery_msgs, discovery_wait_time, commands, data_store):
        self._port = port
        self._admin_port = admin_port
        self._discovery_msgs = discovery_msgs
        self._discovery_wait_time = discovery_wait_time
        self._commands = commands
        self._data_store = data_store

        self._net_udp_comm = NetUDPComm()

    def list_commands(self):
        commands = copy.deepcopy(self._commands)

        for index, value in enumerate(commands):

            if type(value["HEX_SEQUENCE"][1]) == type({}):
                args = value["HEX_SEQUENCE"][1]

                commands[index]["ARGUMENT"] = args.keys()

            del value["HEX_SEQUENCE"]

        return commands

    def list_zones(self):
        return self._data_store.get_zones()

    def send_command(self, zone_identifier, command, argument=None):
        ip_address = None

        if zone_identifier < 0:
            ip_address = NetUtils.get_broadcast_address()
        else:
            bridge_info = self._data_store.get_wifi_bridge_in_zone(zone_identifier)

            if len(bridge_info) > 0:
                ip_address = bridge_info[0]["IP_ADDRESS"]
            else:
                raise MilightControllerException(
                        "No Wi-fi bridge in zone with identifier '" + str(zone_identifier) + "'.")

        message = None
        command_info = self._get_command_info(command)

        if command_info is None:
            raise MilightControllerException(
                "Command '" + command + "' unknown.")
        else:
            if type(command_info["HEX_SEQUENCE"][1]) == type({}):
                if argument is None:
                    raise MilightControllerException(
                        "Command '" + command + "' requires an argument, but none given.")
                elif argument.upper() not in map(lambda x: x.upper(), command_info["HEX_SEQUENCE"][1].keys()):
                    raise MilightControllerException(
                        "Argument '" + argument + "' passed to the '" + command + "' command is unknown.")
                else:
                    for key, value in command_info["HEX_SEQUENCE"][1].iteritems():
                        if argument.upper() == key.upper():
                            message = command_info["HEX_SEQUENCE"][
                                0] + value + command_info["HEX_SEQUENCE"][2]

                            break

            else:
                if argument is not None:
                    raise MilightControllerException(
                        "Command '" + command + "' requires no argument, but at least one given.")
                else:
                    message = "".join(command_info["HEX_SEQUENCE"])

        self._net_udp_comm.send_message(
            ip_address, self._port, binascii.unhexlify(message))

    def discover_wifi_bridges(self):
        broadcast_address = NetUtils.get_broadcast_address()

        net_udp_comm = NetUDPComm()

        for discovery_msg in self._discovery_msgs:
            net_udp_comm.send_message(
                broadcast_address, self._admin_port, discovery_msg)

        messages = net_udp_comm.read_messages(64, self._discovery_wait_time)

        bridges = {}

        for msg in messages:
            parts = msg.split(",")

            ip_address = parts[0]
            mac_address = ':'.join(s.encode('hex')
                                   for s in parts[1].decode('hex'))
            name = parts[2]

            bridges[mac_address.upper()] = (ip_address, name)

        self._data_store.update_wifi_bridges(bridges)

    def _get_command_info(self, command):
        for index, value in enumerate(self._commands):
            if value["COMMAND"].upper() == command.upper():
                return value

        return None


class MilightControllerException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
