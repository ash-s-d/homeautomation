"""nodecamera.py: A simple Pi Camera wrapper class"""

import time

from picamera import PiCamera

__author__ = "Ashvin Domah"
__copyright__ = "Copyright 2017"
__maintainer__ = "Ashvin Domah"
__email__ = "ashvindomah@gmail.com"
__status__ = "Production"
__version__ = "1.0"


class NodeCamera(object):
    _camera = None

    def __init__(self, settings):
        self._camera = PiCamera()

        if "RESOLUTION" in settings:
            self.set_resolution(
                int(settings["RESOLUTION"]["WIDTH"]),
                int(settings["RESOLUTION"]["HEIGHT"])
            )

        if "FLIP_IMAGE" in settings:
            self.set_orientation(
                bool(settings["FLIP_IMAGE"]["HORIZONTAL"]),
                bool(settings["FLIP_IMAGE"]["VERTICAL"])
            )

    def set_resolution(self, width, height):
        self._camera.resolution = (
            width,
            height
        )

    def set_orientation(self, h_flip, v_flip):
        self._camera.hflip = h_flip
        self._camera.vflip = v_flip

    def get_captured_stream(self, stream):
        self._camera.capture(stream, format="jpeg")

        return stream

    def close(self):
        self._camera.close()
