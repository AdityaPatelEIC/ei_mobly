from ei_mobly.utils import switch_to_ui_snippet, switch_to_automator_snippet
from ei_mobly.globals import *
from .mobly_custom_logger import customLogger


class MoblyGestureAndTouch:
    def __init__(self):
        pass

    def swipe_up(self, device, strength_percent):
        """
        Swipes up a portion of the screen based on strength_percent.
        The value is scaled so that:
        - 50 maps to 70
        - Others scale proportionally using (strength_percent * 70 / 50)
        """
        assert 1 <= strength_percent <= 100, "strength_percent must be between 1 and 100"

        # Scale strength: 50 → 70 proportion
        scroll_percent = int((strength_percent * 100) / 50)

        if get_last_snippet(device) != 'automator':
            switch_to_automator_snippet(device)

        device.ui(scrollable=True).scroll().down(percent=scroll_percent)

    def swipe_down(self, device, strength_percent):
        """
        Swipes down a portion of the screen based on strength_percent.
        The value is scaled so that:
        - 50 maps to 70
        - Others scale proportionally using (strength_percent * 70 / 50)
        """
        assert 1 <= strength_percent <= 100, "strength_percent must be between 1 and 100"

        scroll_percent = int((strength_percent * 100) / 50)

        if get_last_snippet(device) != 'automator':
            switch_to_automator_snippet(device)

        device.ui(scrollable=True).scroll().up(percent=scroll_percent)

