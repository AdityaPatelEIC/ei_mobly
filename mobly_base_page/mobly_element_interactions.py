from .mobly_wait_and_synchronization import *
from .mobly_custom_logger import customLogger


class MoblyElementInteractions:
    def __init__(self):
        self.wt_syn = MoblyWaitAndSynchronization()

    def get_element(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        element = None
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is None:
                return element
            log.info(f"Element found with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")
        return element

    def get_elements(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        elements = None
        try:
            elements = self.wt_syn.wait_for_elements(device, locator_type, locator_value, timeout)
            if elements is None:
                return elements
            log.info(f"Element found with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")
        return elements

    def click_element(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is not None:
                if element.click():
                    log.info(f"Clicked on element with locator type {locator_type} and locator value {locator_value}")
                else:
                    log.error(f"Failed to click on element with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")

    def click_element_on_devices(self, *args, locator_type, locator_value, timeout):
        for device in args:
            self.click_element(device, locator_type, locator_value, timeout)

    def click_element_on_all_devices(self, devices, locator_type, locator_value, timeout):
        for device in devices:
            self.click_element(device, locator_type, locator_value, timeout)

    def long_click_element(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is not None:
                if element.long_click():
                    log.info(f"Long clicked on element with locator type {locator_type} and locator value {locator_value}")
                else:
                    log.error(f"Failed to long click on element with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")

    def long_click_element_on_devices(self, *args, locator_type, locator_value, timeout):
        for device in args:
            self.long_click_element(device, locator_type, locator_value, timeout)

    def long_click_element_on_all_devices(self, devices, locator_type, locator_value, timeout):
        for device in devices:
            self.long_click_element(device, locator_type, locator_value, timeout)

    def click_and_hold_element(self, device, locator_type, locator_value, hold_time, timeout):
        _HOLD_WAIT_TIME = datetime.timedelta(seconds=hold_time)
        log = customLogger()
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is not None:
                if element.click(_HOLD_WAIT_TIME):
                    log.info(f"Clicked on element with locator type {locator_type} and locator value {locator_value} for {hold_time} seconds")
                else:
                    log.error(f"Failed to click on element with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")

    def click_and_hold_element_on_devices(self, *args, locator_type, locator_value, hold_time,  timeout):
        for device in args:
            self.click_and_hold_element(device, locator_type, locator_value, hold_time,  timeout)

    def click_and_hold_element_on_all_devices(self, devices, locator_type, locator_value, hold_time, timeout):
        for device in devices:
            self.click_and_hold_element(device, locator_type, locator_value, hold_time, timeout)

    def set_element_text(self, device, locator_type, locator_value, text, timeout):
        log = customLogger()
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is not None:
                if element.set_text(text):
                    log.info(f"Set text = \"{text}\" on element with locator type {locator_type} and locator value {locator_value}")
                else:
                    log.error(f"Failed to set text \"{text}\" on element with locator type {locator_type} and locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")

    def set_element_text_on_devices(self, *args, locator_type, locator_value, text, timeout):
        for device in args:
            self.set_element_text(device, locator_type, locator_value, text, timeout)

    def set_element_text_on_all_devices(self, devices, locator_type, locator_value, text, timeout):
        for device in devices:
            self.set_element_text(device, locator_type, locator_value, text, timeout)

    def clear_element_text(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element is not None:
                if element.clear_text():
                    log.info(f"Cleared existing text from the element with locator type {locator_type} and locator "
                             f"value {locator_value}")
                else:
                    log.error(f"Failed to clear existing text from the element with locator type {locator_type} and "
                              f"locator value {locator_value}")
        except Exception as e:
            log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")

    def clear_element_text_on_devices(self, *args, locator_type, locator_value, timeout):
        for device in args:
            self.clear_element_text(device, locator_type, locator_value, timeout)

    def clear_element_text_on_all_devices(self, devices, locator_type, locator_value, timeout):
        for device in devices:
            self.clear_element_text(device, locator_type, locator_value, timeout)