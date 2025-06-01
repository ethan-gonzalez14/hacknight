from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from db import get_person  # Assuming this function is defined in db module
from db import Person, Relationship, relationships

# Dummy registry
people = {
    "alice": Person("Alice", "@alice", "1234"),
    "bob": Person("Bob", "@bob", "5678")
}

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        known_paths = ['/get-person', '/get-relationship']

        if path in known_paths:
            if path == '/get-person':
                name = query_params.get("name", [None])[0]
                if name and name.lower() in people:
                    person = people[name.lower()]
                    self.respond_json(200, person.jsonify())
                else:
                    self.respond_json(404, {"error": "Person not found"})

            else:
                self.respond_json(404, {"error": "Unknown path"})

    def respond_json(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if isinstance(content, str):
            self.wfile.write(content.encode())
        else:
            self.wfile.write(json.dumps(content).encode())



def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()