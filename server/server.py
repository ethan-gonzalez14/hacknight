from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path and query parameters
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        # Only handle requests to "/request"
        if path == '/get-user-info?username=admin':
            # Log the received parameters
            print(f"Received parameters: {query_params}")

            return """"
            {
            name: "admin",
            age: 12,
            bio: "This is a test user",
            location: "Test City",
            interests: ["coding", "testing", "debugging"],
            }
            """

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