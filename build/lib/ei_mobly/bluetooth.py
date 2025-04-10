from .wifi import DeviceError, EmulatorError
from .globals import *
from .utils import switch_to_api_snippet


class BleError(Exception):
    def __init__(self, message="There is some issue in Bluetooth"):
        self.message = message
        super().__init__(self.message)


class Bluetooth:

    def turn_on_bluetooth(self, device=None):
        if device is None:
            raise DeviceError("No device has been provided")
        if get_last_snippet_ui(device):
            switch_to_api_snippet(device)
        device.api.btEnable()

    def turn_on_bluetooth_on_devices(self, *args):
        for device in args:
            self.turn_on_bluetooth(device)

    def turn_on_bluetooth_on_all_devices(self, devices):
        for device in devices:
            self.turn_on_bluetooth(device)

    def turn_off_bluetooth(self, device=None):
        if device is None:
            raise DeviceError("No device has been provided")
        if get_last_snippet_ui(device):
            switch_to_api_snippet(device)
        device.api.btDisable()

    def turn_off_bluetooth_on_devices(self, *args):
        for device in args:
            self.turn_off_bluetooth(device)

    def turn_off_bluetooth_on_all_devices(self, devices):
        for device in devices:
            self.turn_off_bluetooth(device)

    def get_bluetooth_scan_result(self, device=None):
        scan_result = dict()
        if device is None:
            raise DeviceError("No device has been provided")
        if device.is_emulator:
            raise EmulatorError("Bluetooth scan is not possible on Emulator devices")
        if get_last_snippet_ui(device):
            switch_to_api_snippet(device)
        result = device.api.btDiscoverAndGetResults()
        device_name = str(device).split('|')[1].replace('>', '')
        scan_result[device_name] = result
        return scan_result

    def get_bluetooth_scan_result_on_devices(self, *args):
        scan_result = list()
        for device in args:
            scan_result.append(self.get_bluetooth_scan_result(device))
        return scan_result

    def get_bluetooth_scan_result_on_all_devices(self, devices):
        scan_result = list()
        for device in devices:
            scan_result.append(self.get_bluetooth_scan_result(device))
        return scan_result
