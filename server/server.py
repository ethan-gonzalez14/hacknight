from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from db import get_user_info  # Assuming this function is defined in db module

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        known_paths = ['/get-user-info', '/get-...']

        if path in known_paths:
            print(f"Received request for {path} with parameters: {query_params}")

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = f"Handled {path} with parameters: {query_params}"
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')


def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()