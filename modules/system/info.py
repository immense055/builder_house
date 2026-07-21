import os
import platform
import socket
import subprocess
import time


def get_system_info():

    info = {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "uptime": get_uptime()
    }

    info["cpu"] = get_cpu_info()
    info["memory"] = get_memory_info()
    info["termux"] = check_termux()

    return info


def get_cpu_info():

    try:
        cpu = subprocess.check_output(
            ["getprop", "ro.product.cpu.abi"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        return cpu

    except Exception:
        return platform.processor()


def get_memory_info():

    try:
        with open("/proc/meminfo") as f:
            data = f.readlines()

        memory = {}

        for line in data:
            if "MemTotal" in line:
                memory["total"] = line.split(":")[1].strip()

            if "MemAvailable" in line:
                memory["available"] = line.split(":")[1].strip()

        return memory

    except Exception:
        return {}


def get_uptime():

    try:
        with open("/proc/uptime") as f:
            seconds = float(f.readline().split()[0])

        return str(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(seconds)
            )
        )

    except Exception:
        return "unknown"


def check_termux():

    return {
        "is_termux": bool(
            os.environ.get("TERMUX_VERSION")
        ),
        "termux_version": os.environ.get(
            "TERMUX_VERSION",
            "unknown"
        )
    }
