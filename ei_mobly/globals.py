# A dictionary to store device-specific variables
device_snippet_state = {}


def get_last_snippet_ui(device):
    device_udid = str(device)
    device_udid = device_udid.split('|')[1][:-1]
    """Returns the last snippet UI value for a specific device."""
    return device_snippet_state.get(device_udid, True)  # Default to True if not set


def set_last_snippet_ui(device, val):
    device_udid = str(device)
    device_udid = device_udid.split('|')[1][:-1]
    """Sets the last snippet UI value for a specific device."""
    device_snippet_state[device_udid] = val
