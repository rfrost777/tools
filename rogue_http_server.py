#!/usr/bin/env python3
#############################################################################
# Extended http.server module to capture post requests from indirect (blind)
# SSRF attacks and so on...
#############################################################################
from http.server import BaseHTTPRequestHandler, HTTPServer

# setup default configuration:
DEFAULT_PORT = 8080  # port to listen on
DEFAULT_HOSTNAME = ''  # bind to all interfaces, for local only use '127.0.0.1'


# Maybe this is better coding practice,
# at least it works, so lets extent http.server's RequestHandler:
class CustomRequestHandler(BaseHTTPRequestHandler):
    # add support for a few basic MIME content types in case we need them down the road...
    extensions_map = {
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg': 'image/svg+xml',
        '.css': 'text/css',
        '.js': 'application/x-javascript',
        '': 'application/octet-stream',  # Default
    }

    def end_headers(self) -> None:
        # set headers to allow requests from any origin:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'[+] GET request captured!')

    def do_POST(self) -> None:
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        self.send_response(200)
        self.end_headers()

        # log the captured POST data to saved_data.html for future reference...
        with open('saved_data.html', 'a') as file:
            file.write(post_data + '\n')
        response = f'[+] POST request captured! Received data: {post_data}'
        self.wfile.write(response.encode('utf-8'))


class RogueHTTPServer(HTTPServer):
    def __init__(self, host, port):
        server_address = (host, port)
        HTTPServer.__init__(self, server_address, CustomRequestHandler)


if __name__ == '__main__':
    httpd = RogueHTTPServer(DEFAULT_HOSTNAME, DEFAULT_PORT)
    print(f'[i] Rogue HTTP server started on port {DEFAULT_PORT}...')
    try:
        # run forever (a very long time):
        httpd.serve_forever()
    except Exception as error:
        # add some generic error handling...
        print(f'[e] Ooopsi, something went wrong: {error}\n')
    except KeyboardInterrupt:
        # maybe not that long, after all...
        httpd.server_close()
        print('[i] Rogue HTTP server stopped. Byebye.')
