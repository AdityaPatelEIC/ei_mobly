from ei_mobly.wifi import WiFi


class WiFiController:
    def __init__(self):
        self.wifi = WiFi()

    def turn_on_wifi(self, device):
        self.wifi.turn_on_wifi(device)

    def turn_on_wifi_on_devices(self, *args):
        self.wifi.turn_on_wifi_on_devices(*args)

    def turn_on_wifi_on_all_devices(self, devices):
        self.wifi.turn_on_wifi_on_all_devices(devices)

    def turn_off_wifi(self, device):
        self.wifi.turn_off_wifi(device)

    def turn_off_wifi_on_devices(self, *args):
        self.wifi.turn_off_wifi_on_devices(*args)

    def turn_off_wifi_on_all_devices(self, devices):
        self.wifi.turn_off_wifi_on_all_devices(devices)

    def connect_to_wifi(self, device, wifi_name, wifi_password):
        self.wifi.connect_to_wifi(device, wifi_name, wifi_password)

    def connect_to_wifi_on_devices(self, *args, wifi_name, wifi_password):
        self.wifi.connect_to_wifi_on_devices(*args, wifi_name=wifi_name, wifi_password=wifi_password)

    def connect_to_wifi_on_all_devices(self, devices, wifi_name, wifi_password):
        self.wifi.connect_to_wifi_on_all_devices(devices, wifi_name=wifi_name, wifi_password=wifi_password)

    def is_wifi_connected(self, device):
        return self.wifi.is_wifi_connected(device)

    def is_wifi_connected_on_devices(self, *args):
        return self.wifi.is_wifi_connected_on_devices(*args)

    def is_wifi_connected_on_all_devices(self, devices):
        return self.wifi.is_wifi_connected_on_all_devices(devices)

    def is_wifi_connected_to(self, device, wifi_name):
        return self.wifi.is_wifi_connected_to(device, wifi_name=wifi_name)

    def is_wifi_connected_to_on_devices(self, *args, wifi_name):
        return self.wifi.is_wifi_connected_to_on_devices(*args, wifi_name=wifi_name)

    def is_wifi_connected_to_all_devices(self, devices, wifi_name):
        return self.wifi.is_wifi_connected_to_all_devices(devices, wifi_name=wifi_name)
