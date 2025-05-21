import datetime
import re
import time

from .mobly_custom_logger import customLogger
from ei_mobly.globals import *
from ei_mobly.utils import switch_to_ui_snippet, switch_to_automator_snippet
from ei_mobly.xpath_converter import xpath_converter


class MoblyWaitAndSynchronization:

    def __init__(self):
        self.log = customLogger()

    def _get_automator_element(self, device, locator_type, locator_value):
        locator_map = {
            'id': lambda val: device.ui(resourceId=val),
            'class': lambda val: device.ui(clazz=val),
            'text': lambda val: device.ui(text=val),
            'desc': lambda val: device.ui(desc=val)
        }
        return locator_map.get(locator_type, lambda val: None)(locator_value)

    def _get_ui_elements(self, device, locator_type, locator_value):
        locator_map = {
            'id': lambda val: device.ui.findObjects({'resourceId': val}),
            'class': lambda val: device.ui.findObjects({'clazz': val}),
            'text': lambda val: device.ui.findObjects({'text': val}),
            'desc': lambda val: device.ui.findObjects({'desc': val})
        }
        return locator_map.get(locator_type, lambda val: None)(locator_value)

    def _ui_element_exists(self, device, locator_type, locator_value):
        locator_map = {
            'id': lambda val: device.ui.exists({'resourceId': val}),
            'class': lambda val: device.ui.exists({'clazz': val}),
            'text': lambda val: device.ui.exists({'text': val}),
            'desc': lambda val: device.ui.exists({'desc': val})
        }
        return locator_map.get(locator_type, lambda val: False)(locator_value)

    def _extract_fields(self, element_data):
        keys = [
            'className', 'text', 'resourceId', 'packageName',
            'enabled', 'clickable', 'checkable', 'checked',
            'focusable', 'focused', 'longClickable', 'scrollable', 'selected'
        ]
        return {key: element_data[key] for key in keys}

    def _process_xpath_elements(self, device, mobly_xpath, timeout):
        start = time.time()
        while time.time() - start < timeout:
            for selector in mobly_xpath:
                selector_code = f"device.ui{selector}"
                if eval(selector_code).exists:
                    return eval(selector_code)
            time.sleep(1)
        raise Exception(f"Element is not visible on the current window within {timeout}")

    def wait_for_element(self, device, locator_type, locator_value, timeout):
        _WAIT_TIME = datetime.timedelta(seconds=timeout)
        locator_type = locator_type.lower()
        element = None

        if get_last_snippet(device) != 'automator':
            switch_to_automator_snippet(device)

        if locator_type in ['id', 'class', 'text', 'desc']:
            element_obj = self._get_automator_element(device, locator_type, locator_value)
            if element_obj.wait.exists(_WAIT_TIME):
                return element_obj
            else:
                raise Exception(f"Element is not visible on the current window within {timeout}")

        elif locator_type == 'xpath':
            mobly_xpath = xpath_converter(locator_value)
            return self._process_xpath_elements(device, mobly_xpath, timeout)

        else:
            self.log.error(f"Unsupported locator type: {locator_type}")
            return None

    def wait_for_elements(self, device, locator_type, locator_value, timeout):
        locator_type = locator_type.lower()

        if get_last_snippet(device) != 'ui':
            switch_to_ui_snippet(device)

        if locator_type in ['id', 'class', 'text', 'desc']:
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self._ui_element_exists(device, locator_type, locator_value):
                    elements_list = self._get_ui_elements(device, locator_type, locator_value)
                    elements = []
                    if get_last_snippet(device) != 'automator':
                        switch_to_automator_snippet(device)
                    for data in elements_list:
                        if data['packageName'] != 'com.android.systemui':
                            element = device.ui(**self._extract_fields(data))
                            elements.append(element)
                    return elements
                time.sleep(1)
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
                            elements_dict = eval(selector_code)
                            elements = []
                            for data in elements_dict:
                                if data['packageName'] != 'com.android.systemui':
                                    element = device.ui(**self._extract_fields(data))
                                    elements.append(element)
                            return elements
                    else:
                        alt_locator_type, alt_locator_value = self.extract_locator_info(selector)
                        return self.wait_for_elements(device, alt_locator_type, alt_locator_value, timeout)
                time.sleep(1)
            raise Exception(f"Element is not visible on the current window within {timeout}")

        else:
            self.log.error(f"Unsupported locator type: {locator_type}")
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
