#!/usr/bin/env python3
#############################################################################
# Extended http.server module to capture post requests from indirect (blind)
# SSRF attacks and so on, now with more SSL for better OpSec :O...
#
# You can generate  your own SSL certificate like this:
# openssl req -x509 -newkey rsa:4096 -keyout /tmp/key.pem -out /tmp/cert.pem -sha256 -days 365
#             -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"
#############################################################################
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# default configuration:
DEFAULT_PORT: int = 4443
# Someone suggested to use /tmp as storage.
# Makes kinda sense for throw-away certificates I guess, so there you go!
PRIVATE_KEY_FILE: str = "/tmp/key.pem"
CERTIFICATE_FILE: str = "/tmp/cert.pem"

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', DEFAULT_PORT), SimpleHTTPRequestHandler)
    # get the SSL socket wrapper ready, :
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.check_hostname = False  # Or else only the hostname that matches the certificate will be accepted!
    # load our throw-away certificate and private keyfile we generated above:
    ssl_context.load_cert_chain(
        certfile=CERTIFICATE_FILE,
        keyfile=PRIVATE_KEY_FILE
    )
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

    socket_info = httpd.socket.getsockname()
    print(f'[i] Rogue HTTPS server started on {socket_info[0]}, port: {socket_info[1]}...')
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
