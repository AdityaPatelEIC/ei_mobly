from .wait_and_synchronization import *
from .custom_logger import customLogger


def get_element(device, locator_type, locator_value, timeout):
    log = customLogger()
    element = None
    try:
        element = wait_for_element(device, locator_type, locator_value, timeout)
        if element is None:
            return element
        log.info(f"Element found with locator type {locator_type} and locator value {locator_value}")
    except Exception as e:
        log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")
    return element


def get_elements(device, locator_type, locator_value, timeout):
    log = customLogger()
    elements = None
    try:
        elements = wait_for_elements(device, locator_type, locator_value, timeout)
        if elements is None:
            return elements
        log.info(f"Element found with locator type {locator_type} and locator value {locator_value}")
    except Exception as e:
        log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")
    return elements


def click_element(device, locator_type, locator_value, timeout):
    log = customLogger()
    try:
        element = wait_for_element(device, locator_type, locator_value, timeout)
        if element is not None:
            if element.click():
                log.info(f"Clicked on element with locator type {locator_type} and locator value {locator_value}")
            else:
                log.error(
                    f"Failed to click on element with locator type {locator_type} and locator value {locator_value}")
    except Exception as e:
        log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")


def long_click_element(device, locator_type, locator_value, timeout):
    log = customLogger()
    try:
        element = wait_for_element(device, locator_type, locator_value, timeout)
        if element is not None:
            if element.long_click():
                log.info(f"Long clicked on element with locator type {locator_type} and locator value {locator_value}")
            else:
                log.error(
                    f"Failed to long click on element with locator type {locator_type} and locator value {locator_value}")
    except Exception as e:
        log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")


def click_and_hold_element(device, locator_type, locator_value, hold_time, timeout):
    _HOLD_WAIT_TIME = datetime.timedelta(seconds=hold_time)
    log = customLogger()
    try:
        element = wait_for_element(device, locator_type, locator_value, timeout)
        if element is not None:
            if element.click(_WAIT_TIME = datetime.timedelta(seconds=timeout)):
                log.info(f"Clicked on element with locator type {locator_type} and locator value {locator_value} for {hold_time} seconds")
            else:
                log.error(f"Failed to click on element with locator type {locator_type} and locator value {locator_value}")
    except Exception as e:
        log.error(f"Element not found with {locator_type} = {locator_value}. :Error-{e}")
