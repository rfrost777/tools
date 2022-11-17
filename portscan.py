################################################################
# portscan.py
#               - Simple python port scanner -
################################################################
import sys
import socket
from time import time

# Setup target IP and port range here:
ip_address = '127.0.0.1'
ports = range(1, 1000)


def test_port(ip: str, probe_port: int, result=1) -> int:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((ip, probe_port))
        if r == 0:
            result = r
        sock.close()
    except Exception as e:
        pass
    return result


def main():
    open_ports = []
    time_start = time()

    for port in ports:
        sys.stdout.flush()
        response = test_port(ip_address, port)
        if response == 0:
            open_ports.append(port)

    if open_ports:
        print(f"Open Ports in {ports} are: ")
        print(sorted(open_ports))
    else:
        print("Looks like no ports are open :(")

    print(f"\n*DEBUG* Execution time was: {time() - time_start} seconds.")


if __name__ == '__main__':
    main()
