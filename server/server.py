from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from db import get_relationships  # Assuming this function is defined in db module
from db import Person

# Dummy registry
people = {
    "alice": Person("Alice", "@alice07", "1234"),
    "bob": Person("Bob", "@bobthebob", "5678")
}

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/get-person':
            name = query_params.get("name", [None])[0]
            if name and name.lower() in people:
                person = people[name.lower()]
                self.respond_json(200, person.jsonify())
            else:
                self.respond_json(404, {"error": "Person not found"})

        elif path == '/get-relationships':
            name = query_params.get("name", [None])[0]
            if name and name.lower() in people:
                person = people[name.lower()]
                rels = get_relationships(person)

                rel_json = [rel.jsonify(person.name) for rel in rels]

                self.respond_json(200, rel_json)
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