from .mobly_wait_and_synchronization import MoblyWaitAndSynchronization
from .mobly_custom_logger import customLogger


class MoblyElementState:
    def __init__(self):
        self.wt_syn = MoblyWaitAndSynchronization()

    def get_element_attribute_state(self, device, locator_type, locator_value, attribute_name, timeout):
        log = customLogger()
        element = None
        attribute_name = attribute_name.lower()
        if attribute_name == 'displayed':
            log.warning(f'{attribute_name} is not supported by mobly')
            return element
        attribute_name_change = {
            'long-clickable': 'long_clickable',
            'package': 'package_name',
            'class': 'class_name',
            'content-desc': 'description',
            'resource-id': 'resource_id'
        }
        attribute_name = attribute_name_change.get(attribute_name, attribute_name)

        try:
            element = self.wt_syn.wait_for_element(device, locator_type, locator_value, timeout)
            if element:
                log.info(f"Element found with locator type {locator_type} and locator value {locator_value}")
                return eval(f'element.{attribute_name}')
            else:
                return element
        except Exception:
            log.error(f"Element not found with {locator_type} = {locator_value}")
        return element
