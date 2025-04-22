import datetime

from .custom_logger import customLogger


def wait_for_element(device, locator_type, locator_value, timeout):
    _WAIT_TIME = datetime.timedelta(seconds=timeout)
    log = customLogger()
    locator_type = locator_type.lower()
    element = None

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
    # Still to implement
    _WAIT_TIME = datetime.timedelta(seconds=timeout)
    log = customLogger()
    locator_type = locator_type.lower()
    element = None

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
