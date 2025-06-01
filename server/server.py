from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from db import get_relationships, add_relationship  # Assuming this function is defined in db module
from db import Person, Relationship

# Dummy registry
people = {
    "alice": Person("alice", "@alice07", "1234"),
    "bob": Person("bob", "@bobthebob", "5678"),
    "cecily": Person("cecily", "@cecilythecutie", "1019")
}

def gen_random_code():
    return "10293210"

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        print("POST PATH: " + path)

        body = self._read_body().decode('utf-8')

        if path == '/add-connection':
            (name, code) = body.split(' ')

            print(name, code)

            if not name or not code:
                self.respond_json(400, {"error": "Missing name or friend parameter"})
                return

            name = name.strip()
            code = code.strip()

            person = None
            for p in people.values():
                if p.friendCode == code:
                    person = p
                    break
            if person == None:
                self.respond_json(404, {"error": "CODE_DOES_NOT_EXIST"})
                return

            add_relationship(Relationship(name.lower(), person.name.lower(), 0, "Unknown", "Unknown", False))

            self.respond_json(200, {"message": "200 OK"})
            return
        elif path == '/create-user':
            parts = body.lower().split(' ')
            username = parts[0].strip().lower()
            handle = '' if len(parts) < 2 else parts[1].strip()

            print(username, handle, username in people)

            if not username:
                self.respond_json(400, {"error": "Missing username"})
                return
            if username in people:
                self.respond_json(400, {"error": "Username already exists"})
                return
            new_person = Person(username, f"{handle}", gen_random_code())
            self.respond_json(200, {"message": "200 OK"})
            return

        else:
            self.respond_json(404, {"error": "Unknown path"})
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)


        if path == '/get-person':
            name = query_params.get("name", [None])[0]
            if name.lower() in people:
                person = people[name.lower()]
                self.respond_json(200, person.jsonify())
                return
            else:
                self.respond_json(404, {"error": "Person not found"})
                return

        elif path == '/get-relationships':
            name = query_params.get("name", [None])[0]
            if name.lower() in people:
                rels = get_relationships(name.lower())

                self.respond_json(200, { "relationships": rels })
                return
            else:
                self.respond_json(404, {"error": "Person not found"})
                return
        elif path == '/get-user-code':
            name = query_params.get("name", [None])[0]
            if name.lower() in people:
                return self.respond_json(200, {"friendCode": people[name.lower()].friendCode})
            else:
                self.respond_json(404, {"error": "Person not found"})
                return
        elif path == '/username-found':
            name = query_params.get("name", [None])[0].lower()
            if name in people:
                self.respond_json(200, { "found": True })
                return
            else:
                self.respond_json(200, { "found": False })
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