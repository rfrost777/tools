#!/usr/bin/env python3
#############################################################################
# Extended http.server module to capture post requests from indirect (blind)
# SSRF attacks and so on, now with more SSL for better OpSec :O...
#
# You can generate  your own SSL certificate like this:
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
#             -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"
#############################################################################
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# default configuration:
DEFAULT_PORT: int = 4443

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', DEFAULT_PORT), SimpleHTTPRequestHandler)
    # get the SSL socket wrapper ready, :
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.check_hostname = False  # Or else only the hostname that matches the certificate will be accepted!
    # load our throw-away certificate and private keyfile we generated above:
    ssl_context.load_cert_chain(
        certfile='cert.pem',
        keyfile='key.pem'
    )
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    print(f'[i] Rogue HTTPS server started on port: {DEFAULT_PORT}...')
    try:
        # run forever (a very long time!):
        httpd.serve_forever()
    except Exception as error:
        # pretend to add some generic error handling ;..;
        print(f'[e] Ewwww, something went wrong: {error}\n')
    except KeyboardInterrupt:
        # ... maybe not _that_ long, after all...
        httpd.server_close()
        print('[i] Rogue HTTPS server stopped. Byebye!')
