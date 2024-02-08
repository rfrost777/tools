#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
# from urllib.parse import unquote


# On a second thought: this _might_ not be the ideal way to go about this, as I think
# this actually overwrites HTTPRequestHandler instead of overloading its methods...
# at least it works, so lets extent http.server's RequestHandler:
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    # add support for a few basic MIME types in case we need them down the road...
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

    def end_headers(self):
        # allow requests from any origin:
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


if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'[i] Rogue HTTP server started on port {server_address[1]}...')
    try:
        # run forever (a very long time):
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    # maybe not that long, after all...
    httpd.server_close()
    print('[i] Rogue HTTP server stopped.')
