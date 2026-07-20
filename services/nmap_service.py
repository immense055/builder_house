import subprocess
import re

def scan_network(network="192.168.0.0/24"):

    result = subprocess.check_output(
        ["nmap", "-sn", "-PR", network],
        text=True
    )

    devices = []

    ips = re.findall(
        r"Nmap scan report for ([0-9.]+)",
        result
    )

    for ip in ips:
        devices.append({
            "ip_address": ip,
            "status": "online"
        })

    return devices
