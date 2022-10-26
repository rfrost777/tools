import sys
import socket


ip_address = '10.10.146.215'
open_ports = []

ports = range(1, 65535)


def test_port(ip, probe_port, result=1):
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


for port in ports: 
    sys.stdout.flush() 
    response = test_port(ip_address, port)
    if response == 0: 
        open_ports.append(port) 
    

if open_ports: 
    print ("Open Ports are: ")
    print (sorted(open_ports))
else: 
    print ("Looks like no ports are open :(")
