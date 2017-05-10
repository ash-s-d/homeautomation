#!/usr/bin/python

import base64
import json
import socket
import time


for x in range(1, 11):
    s = socket.socket()

    s.connect(("192.168.100.3", 3103))

    s.sendall("{\"COMMAND\": \"CAMERA_IMG\"}")

    response = ""
    response_json = None

    finish = False

    while not finish:
        response = response + s.recv(1024)

        try:
            response_json = json.loads(response)

            finish = True
        except ValueError:
            None

    f = open("./images/capture_" + str(x) + ".jpeg", 'wb')

    f.write(base64.b64decode(response_json["PAYLOAD"]["IMAGE_BASE64"]))
    f.close()

    s.close()

    time.sleep(1)
