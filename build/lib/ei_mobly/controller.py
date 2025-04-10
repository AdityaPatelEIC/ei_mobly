from mobly.controllers.android_device import create, destroy
from .globals import *

_ANDROID_DEVICES_LIST = None


def setup_ad():
    """Sets up the global ad variable for Android device controller."""
    global _ANDROID_DEVICES_LIST
    if _ANDROID_DEVICES_LIST is None:
        _ANDROID_DEVICES_LIST = create("*")
        for device in _ANDROID_DEVICES_LIST:
            # device.load_snippet('api', 'com.google.android.mobly.snippet.bundled')
            device.load_snippet('ui', 'com.google.android.mobly.snippet.uiautomator')
            set_last_snippet_ui(device, True)


def return_devices():
    if _ANDROID_DEVICES_LIST is not None:
        return _ANDROID_DEVICES_LIST
    else:
        return "Failed to Initialize the devices"


def close_device_connections():
    for device in _ANDROID_DEVICES_LIST:
        if get_last_snippet_ui(device):
            device.unload_snippet('ui')
        else:
            device.unload_snippet('api')
    destroy(_ANDROID_DEVICES_LIST)
