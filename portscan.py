#!/usr/bin/env python3
################################################################
# portscan.py
#               - Simple Python port scanner -
################################################################
import sys
import socket
import argparse
import time


def test_port(ip: str, port: int, open_ports: list):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            # Port is open, so append to list...
            open_ports.append(port)
        sock.close()
    except socket.error:
        # only catching socket errors here is probably better practice!
        pass
# === EMD def test_port ===


def main():
    open_ports = []

    # Set up a parser and populate the arguments...
    parser = argparse.ArgumentParser(description="Simple Portscanner Version 0.1")
    parser.add_argument(
        "ip_address",
        type=str,
        help="Target IP address to scan."
    )
    parser.add_argument(
        "max_port",
        type=int,
        help="Scan ports from 1 to max_port."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        dest="debug",
        help="Print additional information useful for performance testing."
    )
    # Parse arguments.
    parsed_args = parser.parse_args()
    # Set up port range.
    ports = range(1, parsed_args.max_port)
    # Save start time.
    time_start = time.perf_counter()

    for port in ports:
        # Check all ports in range.
        sys.stdout.flush()
        test_port(parsed_args.ip_address, port, open_ports)

    if open_ports:
        print(f"Open Ports in {ports} found: ")
        print(sorted(open_ports))
    else:
        print("Looks like we found no open ports :(")

    # Save end time.
    time_end = time.perf_counter()
    if parsed_args.debug:
        # DEBUG? Print out the time difference between end and start in seconds.
        print(f"\n[+] Execution time was about: {round(time_end - time_start, 2)} seconds.")
# === END def main ===


if __name__ == '__main__':
    main()
