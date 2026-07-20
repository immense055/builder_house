import os
import platform

def get_system_info():
    return {
        "platform": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "termux_home": os.environ.get("HOME"),
        "prefix": os.environ.get("PREFIX")
    }
