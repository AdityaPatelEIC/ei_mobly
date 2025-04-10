import time

from .wifi import DeviceError
from .globals import *
from .utils import switch_to_ui_snippet

class SelectorError(Exception):
    def __init__(self, message="There is something wrong with selector"):
        self.message = message
        super().__init__(self.message)


class ModeError(Exception):
    def __init__(self, message="There is something wrong with mode"):
        self.message = message
        super().__init__(self.message)


class QuickSettings:
    def switch_aeroplane_mode(self, device=None, selector=None, mode=None):
        if device is None or selector is None or mode is None:
            if device is None:
                raise DeviceError("No device has been provided")
            elif selector is None:
                raise SelectorError("No selector has been provided")
            else:
                raise ModeError("No mode has been provided")
        if not get_last_snippet_ui(device):
            switch_to_ui_snippet(device)
        device.ui.openQuickSettings()
        time.sleep(1)
        result = device.ui.clickObj(selector)
        return result
