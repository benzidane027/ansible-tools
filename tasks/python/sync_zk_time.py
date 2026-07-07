"""
Sync a ZKTeco device's clock to Algerian (Africa/Algiers) time.
Usage: python3 sync_zk_time.py <ip> <port> <password>
"""

import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from zk import ZK

ALGERIA_TZ = ZoneInfo("Africa/Algiers")  # UTC+1, no DST


def get_algeria_time():
    return datetime.now(ALGERIA_TZ).replace(tzinfo=None)


def sync_device_time(ip, port=4370, password=0, timeout=5):
    zk = ZK(ip, port=port, timeout=timeout, password=password, force_udp=False, ommit_ping=False)
    conn = None
    try:
        conn = zk.connect()
        old_time = conn.get_time()
        algeria_now = get_algeria_time()

        conn.disable_device()
        conn.set_time(algeria_now)
        conn.enable_device()

        new_time = conn.get_time()
        print(f"OK {ip} old={old_time} new={new_time}")
        return 0
    except Exception as e:
        print(f"FAIL {ip} error={e}")
        return 1
    finally:
        if conn:
            conn.disconnect()


if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4370
    password = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    sys.exit(sync_device_time(ip, port, password))