from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

from db import get_relationship, get_all_relationships, add_relationship, degrees_of_separation
from db import Person, Relationship

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver  import ThreadingMixIn
import random


# Dummy registry
people = {
    # "alice": Person("alice", "alice07", "1234"),
    # "bob": Person("bob", "bobthebob", "5678"),
    # "cecily": Person("cecily", "cecilythecutie", "1019")
}

def gen_random_code():
    return str(random.randint(100_000_000, 999_999_999))

class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _read_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(content_length)

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        body = self._read_body().decode('utf-8')

        if path == '/add-connection':
            print(f"BODY: {body}")
            name, code, level, *words = body.split(' ')
            name = name.lower()
            level = level.lower()
            context = ' '.join(words)

            if not name or not code:
                self.respond_json(400, {"error": "Missing name or friend parameter"})
                return
            if level.lower() not in ['best_friends', 'friends', 'family', 'work', 'married', 'romantic']:
                self.respond_json(400, {"error": "Invalid level"})
                return
            if name.lower() not in people:
                self.respond_json(404, {"error": "Person not found"})
                return

            name = name.strip()
            code = code.strip()

            otherPerson = None
            user = None
            for p in people.values():
                if user == None and p.name.lower() == name.lower():
                    if level == "best_friends" and p.best_friend is not None:
                        self.respond_json(400, {"error": "USER_ALREADY_HAS_BEST_FRIEND"})
                        return
                    user = p
                if p.friendCode == code:
                    otherPerson = p
                
                # If we've already found both in order to check for best friendship, we can exit the loop
                if user != None and otherPerson != None:
                    break
            if otherPerson == None:
                self.respond_json(200, {"error": "CODE_DOES_NOT_EXIST"})
                return
            
            # Can't have more than one best friend
            if level == "best_friend":
                if otherPerson.best_friend != None:
                    self.respond_json(400, {"error": "OTHER_ALREADY_HAS_BEST_FRIEND"})
                    return
            
            if get_relationship(name.lower(), otherPerson.name.lower()) is not None:
                self.respond_json(200, {"error": "ALREADY_CONNECTED"})
                return

            add_relationship(Relationship(name.lower(), otherPerson.name.lower(), 0, "Unknown", context, level.lower()))

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
            people[username] = new_person
            self.respond_json(200, {"message": "200 OK"})
            return
        elif path == '/update-private-bio':
            parts = body.split(' ')
            username = parts[0].strip().lower()
            bio = ' '.join(parts[1:]).strip()

            if not username:
                self.respond_json(400, {"error": "USERNAME_NOT_GIVEN"})
                return
            if username not in people:
                self.respond_json(404, {"error": "INVALID_USERNAME_GIVEN"})
                return

            people[username].private_bio = bio
            self.respond_json(200, {"message": "200 OK"})
            return
        elif path == '/update-public-bio':
            parts = body.split(' ')
            username = parts[0].strip().lower()
            bio = ' '.join(parts[1:]).strip()

            print("Updating that public biography: ", username, bio)

            if not username:
                self.respond_json(400, {"error": "USERNAME_NOT_GIVEN"})
                return
            if username not in people:
                self.respond_json(404, {"error": "INVALID_USERNAME_GIVEN"})
                return

            people[username].public_bio = bio
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
                print(person.jsonify())
                self.respond_json(200, person.jsonify())
                return
            else:
                self.respond_json(404, {"error": "Person not found"})
                return

        elif path == '/get-relationships':
            name = query_params.get("name", [None])[0].lower()
            print("NAME", name in people)
            if name in people:
                rels = get_all_relationships(name.lower())
                print(rels)

                new_rels = []

                # Add the relationships between the person's friends
                for x in range(len(rels)):
                    for y in range(x + 1, len(rels)):
                        if x == y: continue
                        print(x, y, rels[x], rels[y])
                        person1 = rels[x]['person1'] if rels[x]['person1'] != name else rels[x]['person2']
                        person2 = rels[y]['person1'] if rels[y]['person1'] != name else rels[y]['person2']

                        relationship = get_relationship(person1, person2)
                        if relationship is not None:
                            new_rels.append(relationship)

                for rel in new_rels:
                    rels.append(rel)

                print(rels)
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
        elif path == '/search-people':
            print(query_params)
            filter = query_params.get("filter", [None])[0].lower()
            # Username of person who searched, since we want to figure out their degrees of separation
            searcher = query_params.get("searcher", [None])[0].lower()

            if searcher not in people:
                self.respond_json(404, { "error": "INVALID_SEARCHER_USERNAME" })
                return

            for person in people.values():
                if person.name.lower().startswith(filter) or person.socials.lower().startswith(filter):
                    degrees = degrees_of_separation(searcher, person.name)
                    print("DEGREES")
                    print(degrees)
                    self.respond_json(200, {"name": person.name, "socials": person.socials, "degrees": degrees })
                    return
            self.respond_json(200, { "message": "NO_MATCH" })

        else:
            self.respond_json(404, {"error": "UNKNOWN_PATH"})
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

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8080):
    # server_address = ('', port)
    # httpd = server_class(server_address, handler_class)
    # print(f'Serving on port {port}...')
    # httpd.serve_forever()

    server = ThreadedHTTPServer(('0.0.0.0', 8080), SimpleRequestHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()


if __name__ == '__main__':
    run()