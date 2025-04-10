from .wifi import *
from .bluetooth import *
from .controller import *
from .globals import *
from .utils import *
from .quick_settings import *
from .mobly_controller import *
import atexit
atexit.register(close_device_connections)
setup_ad()