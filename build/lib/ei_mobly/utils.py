from .controller import return_devices
from .wifi import *
from .globals import *


def get_device_object(udid):
    devices = return_devices()
    for device in devices:
        device_udid = str(device)
        device_udid = device_udid.split('|')[1][:-1]
        if device_udid == udid:
            return device
    else:
        raise DeviceError(f"Device with udid {udid} has not been found")


def is_device_emulator(device=None):
    if device is None:
        raise DeviceError("No device has been provided")
    return device.is_emulator


def switch_to_api_snippet(device=None):
    if device is None:
        raise DeviceError("No device has been provided")
    device.unload_snippet('ui')
    device.load_snippet('api', 'com.google.android.mobly.snippet.bundled')
    set_last_snippet_ui(device, False)


def switch_to_ui_snippet(device=None):
    if device is None:
        raise DeviceError("No device has been provided")
    device.unload_snippet('api')
    device.load_snippet('ui', 'com.google.android.mobly.snippet.uiautomator')
    set_last_snippet_ui(device, True)


def open_application(device, app_package, app_activity, no_reset=True):
    if not no_reset:
        print('Clearing app data...')
        args = ['adb', '-s', device.adb.serial, 'shell', 'pm clear', app_package]
        result = device.adb._exec_cmd(args, shell=True, timeout=10, stderr=None)
        print(result.decode('utf-8').strip())

    print('Starting the app...')
    args = ['adb', '-s', device.adb.serial, 'shell', 'am start -n', app_package + '/' + app_activity]
    result = device.adb._exec_cmd(args, shell=True, timeout=10, stderr=None)
    print(result.decode('utf-8').strip())
