import datetime
import re
import time

from .mobly_custom_logger import customLogger
from ei_mobly.globals import *
from ei_mobly.utils import switch_to_ui_snippet, switch_to_automator_snippet
from ei_mobly.xpath_converter import xpath_converter


class MoblyWaitAndSynchronization:

    def wait_for_element(self, device, locator_type, locator_value, timeout):
        _WAIT_TIME = datetime.timedelta(seconds=timeout)
        log = customLogger()
        locator_type = locator_type.lower()
        element = None
        if get_last_snippet(device) != 'automator':
            switch_to_automator_snippet(device)
        # Dictionary mapping locator types to their corresponding Mobly methods
        locator_map = {
            'id': lambda val: device.ui(resourceId=val),
            'class': lambda val: device.ui(clazz=val),
            'text': lambda val: device.ui(text=val),
            'desc': lambda val: device.ui(desc=val)
        }

        # Get the locator method based on the locator_type
        locator_func = locator_map.get(locator_type)

        if locator_func:
            element_exists = locator_func(locator_value).wait.exists(_WAIT_TIME)
            if element_exists:
                element = locator_func(locator_value)
                return element
            else:
                raise Exception(f"Element is not visible on the current window within {timeout}")
        elif locator_type == 'xpath':
            mobly_xpath = xpath_converter(locator_value)
            start = time.time()
            while time.time() - start < timeout:
                for selector in mobly_xpath:
                    selector_code = f"device.ui{selector}"
                    if eval(selector_code).exists:
                        element = eval(selector_code)
                        return element
                time.sleep(1)
            else:
                raise Exception(f"Element is not visible on the current window within {timeout}")
                return element
        else:
            log.error(f"Unsupported locator type: {locator_type}")
            return None

    def wait_for_elements(self, device, locator_type, locator_value, timeout):
        log = customLogger()
        locator_type = locator_type.lower()
        if get_last_snippet(device) != 'ui':
            switch_to_ui_snippet(device)

        # Dictionary mapping locator types to their corresponding Mobly methods
        locator_map = {
            'id': lambda val: device.ui.findObjects({'resourceId': val}),
            'class': lambda val: device.ui.findObjects({'clazz': val}),
            'text': lambda val: device.ui.findObjects({'text': val}),
            'desc': lambda val: device.ui.findObjects({'desc': val}),
        }

        # Dictionary mapping locator types to their corresponding Mobly methods
        locator_map_exists = {
            'id': lambda val: device.ui.exists({'resourceId': val}),
            'class': lambda val: device.ui.exists({'clazz': val}),
            'text': lambda val: device.ui.exists({'text': val}),
            'desc': lambda val: device.ui.exists({'desc': val}),
        }

        # Get the locator method based on the locator_type
        locator_func = locator_map.get(locator_type.lower())
        locator_func_exists = locator_map_exists.get(locator_type.lower())

        if locator_func:
            element_exists = False
            start_time = time.time()
            while time.time() - start_time < timeout:
                if locator_func_exists(locator_value):
                    element_exists = True
                    break
                time.sleep(1)

            if element_exists:
                elements = []
                elements_list = locator_func(locator_value)
                if get_last_snippet(device) != 'automator':
                    switch_to_automator_snippet(device)
                for element_data in elements_list:
                    if element_data['packageName'] != 'com.android.systemui':
                        keys_to_extract = [
                            'className', 'text', 'resourceId', 'packageName',
                            'enabled', 'clickable', 'checkable', 'checked',
                            'focusable', 'focused', 'longClickable', 'scrollable', 'selected'
                        ]
                        # Extract the required fields using dictionary comprehension
                        extracted_data = {key: element_data[key] for key in keys_to_extract}
                        element = device.ui(**extracted_data)
                        elements.append(element)
                return elements
            else:
                raise Exception(f"Elements are not visible on the current window within {timeout}")
        elif locator_type == 'xpath':
            if get_last_snippet(device) != 'automator':
                switch_to_automator_snippet(device)
            mobly_xpath = xpath_converter(locator_value)
            start = time.time()
            while time.time() - start < timeout:
                for original_selector in mobly_xpath:
                    selector = self.replace_last_child_with_find(original_selector)
                    if 'find' in selector:
                        selector_code = f"device.ui{selector}"
                        if eval(f"device.ui{original_selector}.exists"):
                            elements = []
                            elements_dict = eval(selector_code)
                            if elements_dict:
                                for element_data in elements_dict:
                                    if element_data['packageName'] != 'com.android.systemui':
                                        keys_to_extract = [
                                            'className', 'text', 'resourceId', 'packageName',
                                            'enabled', 'clickable', 'checkable', 'checked',
                                            'focusable', 'focused', 'longClickable', 'scrollable', 'selected'
                                        ]
                                        # Extract the required fields using dictionary comprehension
                                        extracted_data = {key: element_data[key] for key in keys_to_extract}
                                        element = device.ui(**extracted_data)
                                        elements.append(element)
                                return elements
                    else:
                        locator_type, locator_value = self.extract_locator_info(selector)
                        elements = self.wait_for_elements(device, locator_type, locator_value, timeout)
                        if elements:
                            return elements
                time.sleep(1)
            else:
                raise Exception(f"Element is not visible on the current window within {timeout}")
        else:
            log.error(f"Unsupported locator type: {locator_type}")
            return None

    def replace_last_child_with_find(self, xpath_string):
        index = xpath_string.rfind('.child')
        if index != -1:
            return xpath_string[:index] + '.find' + xpath_string[index + len('.child'):]
        return xpath_string

    def extract_locator_info(self, selector_string):
        match = re.search(r'\(\s*(\w+)\s*=\s*"([^"]+)"\s*\)', selector_string)
        if match:
            locator_type = match.group(1)
            if locator_type == 'resourceId':
                locator_type = 'id'
            elif locator_type == 'clazz':
                locator_type = 'class'
            locator_value = match.group(2)
            return locator_type, locator_value
        return None, None
