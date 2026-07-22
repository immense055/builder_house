import os
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BTCRECOVER = os.path.join(BASE_DIR, "btcrecover", "btcrecover.py")
LOG_FILE = os.path.join(BASE_DIR, "logs", "recovery.log")


def run_recovery(args):
    cmd = ["python", BTCRECOVER] + args

    with open(LOG_FILE, "a") as log:
        log.write(
            f"\n[{datetime.now()}] START\n"
        )

        process = subprocess.Popen(
            cmd,
            stdout=log,
            stderr=log
        )

    return {
        "status": "started",
        "pid": process.pid
    }

