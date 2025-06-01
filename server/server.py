from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from db import get_user_info  # Assuming this function is defined in db module

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path and query parameters
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/get-user-info':
            # Log the received parameters
            print(f"Received parameters: {query_params}")

            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = f"Handled /request with parameters: {query_params}"
            self.wfile.write(response.encode('utf-8'))
            
        else:
            # Handle unknown paths
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