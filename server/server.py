from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from db import get_relationships, add_relationship  # Assuming this function is defined in db module
from db import Person, Relationship

# Dummy registry
people = {
    "alice": Person("Alice", "@alice07", "1234"),
    "bob": Person("Bob", "@bobthebob", "5678")
}

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        print(path)

        body = self._read_body().decode('utf-8')

        if path == '/add-connection':
            (name, friend) = body.split(' ')

            print(name, friend)

            if not name or not friend:
                self.respond_json(400, {"error": "Missing name or friend parameter"})
                return

            name = name.strip()
            friend = friend.strip()

            add_relationship(Relationship(name.lower(), friend.lower(), 0, "Unknown", "Unknown", False))

            self.respond_json(200, {"message": "200 OK"})
            return

        self.respond_json(404, {"error": "Unknown path"})
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)


        if path == '/get-person':
            name = query_params.get("name", [None])[0]
            if name.lower() in people:
                person = people[name.lower()]
                # self.respond_json(200, person.jsonify())
                self.respond_json(200, {})
                return
            else:
                self.respond_json(404, {"error": "Person not found"})
                return

        elif path == '/get-relationships':
            name = query_params.get("name", [None])[0]
            if name.lower() in people:
                rels = get_relationships(name.lower())

                print("about to respond correctly!!!")
                self.respond_json(200, { "relationships": rels })
                return
            else:
                self.respond_json(404, {"error": "Person not found"})
                return

        else:
            self.respond_json(404, {"error": "Unknown path"})
            return

    def respond_json(self, status_code, content):
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Connection', 'Close')
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