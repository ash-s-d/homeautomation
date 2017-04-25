#!/usr/bin/python

"""netutils.py: Class exposing a number of static network utilities methods"""

import netifaces

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NetUtils(object):

    @staticmethod
    def get_ip_address():
        network_info = NetUtils._get_network_info()

        return network_info["addr"]

    @staticmethod
    def get_netmask_address():
        network_info = NetUtils._get_network_info()

        return network_info["netmask"]

    @staticmethod
    def get_broadcast_address():
        network_info = NetUtils._get_network_info()

        return network_info["broadcast"]

    @staticmethod
    def get_mac_address():
        network_info = NetUtils._get_network_info()

        return network_info["mac"]

    @staticmethod
    def _get_network_info():
        gateways = netifaces.gateways()

        active_interface = gateways["default"][netifaces.AF_INET][1]

        network_info = netifaces.ifaddresses(active_interface)[
            netifaces.AF_INET][0]

        network_info["mac"] = (netifaces.ifaddresses(active_interface)[
            netifaces.AF_LINK])[0]["addr"]

        return network_info
