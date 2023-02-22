#!/usr/bin/env python3
################################################################
# portscan.py
#               - Simple python port scanner -
################################################################
import sys
import socket
import argparse
from time import time


def test_port(ip: str, probe_port: int, result=1) -> int:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((ip, probe_port))
        if r == 0:
            result = r
        sock.close()
    except socket.error:
        # only catching socket errors here is probably better practice!
        pass
    return result


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

    if parsed_args.debug:
        # DEBUG flag set? Remember start time.
        time_start = time()

    for port in ports:
        # Check all ports in range.
        sys.stdout.flush()
        response = test_port(parsed_args.ip_address, port)
        if response == 0:
            open_ports.append(port)

    if open_ports:
        print(f"Open Ports in {ports} are: ")
        print(sorted(open_ports))
    else:
        print("Looks like no ports are open :(")

    if parsed_args.debug:
        # DEBUG? Print out the time difference between now and start.
        print(f"\n[+] Execution time was about: {time() - time_start} seconds.")


if __name__ == '__main__':
    main()
