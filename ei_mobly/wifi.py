from .globals import *
from .utils import switch_to_api_snippet

class WiFiError(Exception):
    def __init__(self, message="There is some issue in WiFi"):
        self.message = message
        super().__init__(self.message)


class EmulatorError(Exception):
    def __init__(self, message="Operation in emulator in not possible"):
        self.message = message
        super().__init__(self.message)


class DeviceError(Exception):
    def __init__(self, message="Device is missing"):
        self.message = message
        super().__init__(self.message)


class WiFi:
    _CONNECTION_STATUS = '<unknown ssid>'

    def turn_on_wifi(self, device=None):
        if device is None:
            raise DeviceError("No device has been provided")
        if get_last_snippet(device) != 'api':
            switch_to_api_snippet(device)
        device.api.wifiEnable()

    def turn_on_wifi_on_devices(self, *args):
        for device in args:
            self.turn_on_wifi(device)

    def turn_on_wifi_on_all_devices(self, devices):
        for device in devices:
            self.turn_on_wifi(device)

    def turn_off_wifi(self, device=None):
        if device is None:
            raise DeviceError("No device has been provided")
        if get_last_snippet(device) != 'api':
            switch_to_api_snippet(device)
        device.api.wifiDisable()

    def turn_off_wifi_on_devices(self, *args):
        for device in args:
            self.turn_off_wifi(device)

    def turn_off_wifi_on_all_devices(self, devices):
        for device in devices:
            self.turn_off_wifi(device)

    def connect_to_wifi(self, device, wifi_name=None, wifi_password=None):
        if device.is_emulator:
            raise EmulatorError("Emulator devices could not be connect with real wifi network")
        if wifi_name and wifi_password:
            if get_last_snippet(device) != 'api':
                switch_to_api_snippet(device)
            device.api.wifiConnectSimple(wifi_name, wifi_password)
        else:
            if wifi_name is None and wifi_password is None:
                raise WiFiError("WiFi Name and Password must be provided")
            elif wifi_name is None:
                raise WiFiError("WiFi Name must be provided")
            else:
                raise WiFiError("WiFi Password must be provided")

    def connect_to_wifi_on_devices(self, *args, **kwargs):
        for device in args:
            self.connect_to_wifi(device, wifi_name=kwargs['wifi_name'], wifi_password=kwargs['wifi_password'])

    def connect_to_wifi_on_all_devices(self, devices, wifi_name=None, wifi_password=None):
        for device in devices:
            self.connect_to_wifi(device, wifi_name=wifi_name, wifi_password=wifi_password)

    def is_wifi_connected(self, device=None):
        if device is None:
            raise DeviceError("No device has been provided")
        if get_last_snippet(device) != 'api':
            switch_to_api_snippet(device)
        device.api.isWifiConnected()
        return device.api.isWifiConnected()

    def is_wifi_connected_on_devices(self, *args):
        for device in args:
            if not self.is_wifi_connected(device):
                return False
        else:
            return True

    def is_wifi_connected_on_all_devices(self, devices):
        for device in devices:
            if not self.is_wifi_connected(device):
                return False
        else:
            return True

    def is_wifi_connected_to(self, device=None, wifi_name=None):
        if wifi_name is None or device is None:
            if device is None:
                raise DeviceError("No device has been provided")
            else:
                raise WiFiError("WiFi Name has not been provided")
        if device.is_emulator:
            raise EmulatorError("Emulator devices could not be connect with real wifi network")
        if get_last_snippet(device) != 'api':
            switch_to_api_snippet(device)
        conn_info = device.api.wifiGetConnectionInfo()
        if conn_info['SSID'] == wifi_name:
            return True
        else:
            return False

    def is_wifi_connected_to_on_devices(self, *args, **kwargs):
        for device in args:
            if not self.is_wifi_connected_to(device, kwargs['wifi_name']):
                return False
        else:
            return True

    def is_wifi_connected_to_all_devices(self, devices, wifi_name=None):
        for device in devices:
            if not self.is_wifi_connected_to(device, wifi_name):
                return False
        else:
            return True
