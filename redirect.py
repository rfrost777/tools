#!/usr/bin/env python3
###############################################################
#  Sets up a simple http redirect using Python's own
#  HTTPServer module...
#  Useful in some CTF-Boxes.
###############################################################
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 2:
    # Wrong argument count? Let's print the usage message!
    print(f"Usage: {sys.argv[0]} <port_number> <url>")
    sys.exit()


class Redirect(BaseHTTPRequestHandler):
    def do_get(self):
        # send back a 302 http-header with <url> as new location...
        self.send_response(302)
        self.send_header('Location', sys.argv[2])
        self.end_headers()


# Redirect forever (a very long time)...
HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
