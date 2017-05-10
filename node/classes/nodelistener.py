"""nodelistener.py: Class implementing a node socket listener"""

import json
import jsonschema
import socket
import threading
import time

from classes.netutils import NetUtils

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeListener(threading.Thread):
    _DISCOVER_CMD = "LINK"
    _STOP_CMD = "STOP"

    request_schema = None

    def __init__(self, name, port):
        threading.Thread.__init__(self)

        self.daemon = True

        self._stopped_flag = threading.Event()

        self._name = name
        self._port = port

        self._ip_address = NetUtils.get_ip_address()
        self._mac_address = NetUtils.get_mac_address()

        self.request_schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "description": "Schema for a node request message",
            "type": "object",
            "required": ["COMMAND"],
            "properties": {
                "COMMAND": {
                    "enum": [self._DISCOVER_CMD, self._STOP_CMD]
                }
            }
        }

    def is_data_valid(self, data_json):
        try:
            jsonschema.validate(data_json, self.request_schema)
        except jsonschema.exceptions.ValidationError:
            return False

        return True

    def generate_response_message(self, payload, error):
        return json.dumps(
            {
                "PAYLOAD": payload,
                "ERROR": error
            }
        )

    def stopped(self):
        return self._stopped_flag.is_set()

    def _get_info(self):
        return {
            "NAME": self._name,
            "IP_ADDRESS": self._ip_address,
            "MAC_ADDRESS": self._mac_address
        }
