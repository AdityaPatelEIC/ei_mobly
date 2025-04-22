import datetime
import time

from .custom_logger import customLogger
from ei_mobly.globals import *
from ei_mobly.utils import switch_to_ui_snippet, switch_to_automator_snippet


def wait_for_element(device, locator_type, locator_value, timeout):
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
    locator_func = locator_map.get(locator_type.lower())

    if locator_func:
        element_exists = locator_func(locator_value).wait.exists(_WAIT_TIME)
        if element_exists:
            element = locator_func(locator_value)
            return element
        else:
            raise Exception(f"Element is not visible on the current window within {timeout}")
    else:
        log.error(f"Unsupported locator type: {locator_type}")
        return None


def wait_for_elements(device, locator_type, locator_value, timeout):
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
    else:
        log.error(f"Unsupported locator type: {locator_type}")
        return None
