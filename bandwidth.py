#!/usr/bin/env python3

import subprocess
from time import sleep

### Configuration

refresh_interval = 500  # in milliseconds
rx_min = 200 * 1024  # 200 KB, the min download speed
rx_max = 12 * 1024**2  # 12 MB, the max download speed
tx_min = 200 * 1024  # 200 KB, the min upload speed
tx_max = 5 * 1024**2  # 5 MB, the max upload speed
rx_color = "#0080c0"  # blue, the color for download speed
tx_color = "#fa7070"  # red, the color for upload speed

### End Configuration


def default_interface():
    process = subprocess.run(
        ["ip", "route"], check=True, text=True, capture_output=True
    )
    for line in process.stdout.splitlines():
        if line.startswith("default via"):
            return line.split()[4]
    raise RuntimeError("No default interface found")


def get_rx_tx_bytes(iface):
    with open("/proc/net/dev") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(f"{iface}:"):
                continue
            rx_bytes = int(line.split()[1])
            tx_bytes = int(line.split()[9])
            return rx_bytes, tx_bytes
    raise RuntimeError("Interface not found")


def bar(current, min, max, color):
    # don't show anything if the current value is less than `min`
    if current < min:
        return " "

    levels = 7

    labels = [
        "▁",  # 0
        "▂",  # 1
        "▄",  # 2
        "▅",  # 3
        "▆",  # 4
        "▇",  # 5
        "█",  # 6
    ]

    level_size = max // levels
    level = current // level_size
    if level >= levels:
        level = levels - 1

    label = labels[level]

    return f"<span color='{color}'>{label}</span>"  # blue


def main():
    iface = default_interface()

    rx_bytes, tx_bytes = get_rx_tx_bytes(iface)

    while True:
        prev_rx_bytes, prev_tx_bytes = rx_bytes, tx_bytes
        rx_bytes, tx_bytes = get_rx_tx_bytes(iface)
        rx_current = (rx_bytes - prev_rx_bytes) * 1000 // refresh_interval
        tx_current = (tx_bytes - prev_tx_bytes) * 1000 // refresh_interval

        rx_bar = bar(rx_current, rx_min, rx_max, rx_color)
        tx_bar = bar(tx_current, tx_min, tx_max, tx_color)
        line = f"{rx_bar} {tx_bar}"
        print(line, flush=True)
        sleep(refresh_interval / 1000)  # Convert ms to seconds


if __name__ == "__main__":
    main()
