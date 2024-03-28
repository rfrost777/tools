#!/bin/python3
# You can generate  your own certificate like this:
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"
from http.server import HTTPServer, BaseHTTPRequestHandler 
import ssl
httpd = HTTPServer(('0.0.0.0', 8080), BaseHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    keyfile="key.pem",
    certfile='cert.pem',
    server_side=True)
httpd.serve_forever()
