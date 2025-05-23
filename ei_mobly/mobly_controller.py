from .utils import *
from .controller import *
from mobly_controllers.mobly_wifi_controller import WiFiController
from mobly_controllers.mobly_bluetooth_controller import BluetoothController
from mobly_controllers.mobly_quick_settings_controller import QuickSettingsController
from mobly_controllers.mobly_element_interactions_controller import ElementInteractionsController
from mobly_controllers.mobly_element_state_controller import ElementStateController


class MoblyController(WiFiController, BluetoothController, QuickSettingsController, ElementInteractionsController, ElementStateController):
    def __init__(self):
        WiFiController.__init__(self)
        BluetoothController.__init__(self)
        QuickSettingsController.__init__(self)
        ElementInteractionsController.__init__(self)
        ElementStateController.__init__(self)

    """ALL THE METHODS RELATED TO OPERATION WITH THE DEVICES"""

    def get_device_object(self, device_id):
        return get_device_object(device_id)

    def return_devices(self):
        return return_devices()

    def is_device_emulator(self, device):
        return is_device_emulator(device)

    """ALL THE METHODS RELATED TO INTERACTIONS WITH APPLICATION"""

    def open_application(self, device, app_package, app_activity, no_reset=True):
        open_application(device, app_package, app_activity, no_reset)
