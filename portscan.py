#!/usr/bin/env python3
################################################################
# portscan.py
#               - Simple Python port scanner -
################################################################
import sys
import socket
import argparse
import time
from contextlib import contextmanager
from termcolor import cprint
import logging


def test_port(ip: str, port: int, open_ports: list) -> None:
    try:
        sock: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout to limit runtime on slow connections.
        sock.settimeout(0.5)
        result: int = sock.connect_ex((ip, port))
        if result == 0:
            # Port is open, so append to list...
            open_ports.append(port)
        # Log the result. Note: For backward compatibility reasons let's not use fString notation.
        logging.debug('[i] (test_port) Result returned for port %s is %s .', port, result)
        sock.close()
    except socket.error:
        # only catching socket errors here is probably better practice!
        # Log it as exception and carry on.
        logging.exception('[E] (test_port) Returned socket an error: %s .', socket.error)
        pass
# === EMD def test_port ===


def port_scan(ip_address: str, ports: range) -> None:
    open_ports: list = []
    for port in ports:
        # Check all ports in range.
        sys.stdout.flush()
        test_port(ip_address, port, open_ports)

    if open_ports:
        cprint(f"[=O=] Open Ports in {ports} found:", 'green', attrs=['dark'])
        cprint(str(sorted(open_ports)), 'green', attrs=['bold'])
    else:
        cprint("[=X=] Looks like we found no open ports :(\n", 'red', attrs=['bold'])
# === EMD def port_scan ===


@contextmanager
def timer() -> None:
    # Save the start time.
    start_time: float = time.perf_counter()
    try:
        # Ensure the context manager can run.
        yield
    finally:
        # Save the end time and print out the duration.
        end_time: float = time.perf_counter()
        cprint(f"\n[=O=] Scan completed in about: {end_time - start_time:.2f} seconds.\n", 'yellow')
# === EMD def timer ===


def main() -> None:
    debug: bool = False
    # Set up a commandline parser and populate its arguments...
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Simple (TCP) port scanner written in Python."
    )
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
        help="Write additional (debugging) information to file: portscan.log."
    )

    # Parse arguments.
    parsed_args: argparse.Namespace = parser.parse_args()

    # If debug flag is set provide a logfile with more information:
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            filename='portscan.log',
            encoding='utf-8',
            # Overwrite logfile by default. Use 'a' for append mode.
            filemode='w',
            # Beautify the logfile entries with custom formatting and date.
            format='%(levelname)s (%(asctime)s: %(message)s',
            datefmt='%d-%m-%Y %I:%M:%S'
        )

    print("\033c")
    cprint(' Simple TCP port scanner', 'green', attrs=['bold'])
    cprint("=================================", 'green')
    # Set up port range...
    ports: range = range(1, parsed_args.max_port)
    # ...and work the magic:
    with timer():
        port_scan(parsed_args.ip_address, ports)
# === END def main ===


if __name__ == '__main__':
    main()
