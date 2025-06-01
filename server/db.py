import json

class Person:
    def __init__(self, name: str, socials: str, friendCode: str):
        self.name = name
        self.public_bio = self.private_bio = ''  # [[public-personal, public-professional], [private-personal, private-professional]]
        self.socials = socials
        self.friendCode = friendCode
        self.best_friend = None
        self.locations = {} # {'location': 'tally'}
    def __repr__(self):
        return f"Person({self.name}, {self.bios}, {self.socials})"
    def jsonify(self):
        return json.dumps({
            "name": self.name,
            "privateBio": self.public_bio,
            "publicBio": self.private_bio,
            "socials": self.socials,
            "friendCode": self.friendCode,
            "locations": self.locations
        })


def setBio(person: Person, bio: str, visibility: int, nature: int): # visibility: [public, private]; nature: [personal, professional]
    person.bios[visibility][nature] = bio

def setSocials(person: Person, socials: str):
    person.socials = socials

relationships = []

class Relationship:
    def __init__(self,
                 person1: str,
                 person2: str,
                 time: int,
                 location: str,
                 context: str,
                 # "friend" or "work" "married" or "family" or "romantic"
                 level: str):
        self.person1 = person1
        self.person2 = person2
        self.time = time
        self.location = location
        self.context = context
        self.level = level
    def __repr__(self):
        return f"Relationship({self.person1}, {self.person2}, {self.time}, {self.location}, {self.context}, {self.level})"
    def jsonify(self):
        return {
            "person1": self.person1,
            "person2": self.person2,
            "time": self.time,
            "location": self.location,
            "context": self.context,
            "level": self.level
        }


def run(query: str):
    """
    Executes a SQL query against the database.
    This function should be implemented to connect to your database and execute the query.
    """
    raise NotImplementedError("This function should be implemented to run SQL queries against your database.")


def insert_relationship(person1: Person, person2: Person, time: int, location: str, context: str, friends: bool):
    """
    Inserts a relationship between person1 and person2, made at the time and location, into the database.
    An optional context about how they met can also be provided.
    """
    relationships.append(Relationship(person1, person2, time, location, context, friends))

def get_all_relationships(person: str) -> list[Relationship]:
    """
    Returns a list of relationships involving the specified person.
    """
    print(relationships, person)
    return [rel.jsonify() for rel in relationships if rel.person1 == person or rel.person2 == person]
def get_relationship(person1: str, person2: str) -> Relationship | None:
    """
    Returns the relationship between person1 and person2 if it exists, otherwise returns None.
    """
    for rel in relationships:
        if (rel.person1 == person1 and rel.person2 == person2) or (rel.person1 == person2 and rel.person2 == person1):
            return rel.jsonify()
    return None

def add_relationship(relationship: Relationship):
    """
    Adds a relationship to the database.
    """
    relationships.append(relationship)


def degrees_of_separation(person1: str, person2: str) -> tuple[int, list[Relationship]]:
    """
    Returns the minimum number of relationships between person1 and person2.
    """

    visited = set()
    queue = [(person1, 0)]  # (current person, current degree)
    
    while queue:
        current_person, degree = queue.pop(0)
        
        if current_person == person2:
            # degree += 1
            # queue.append((current_person, degree))  # Add current person to the queue to collect all people at this degree
            # people = []
            # for item in queue: people.append(item[0])
            return (degree, queue)
        
        if current_person in visited:
            continue
        
        visited.add(current_person)
        
        print(current_person, )
        for rel in get_all_relationships(current_person):
            next_person = rel['person1'] if rel['person2'] == current_person else rel['person2']
            print(next_person)
            if next_person not in visited:
                queue.append((next_person, degree + 1))
    
    return (-1, [])  # If no relationship found

def degrees_of_separation(person1: str, person2: str) -> int:
    """
    Returns the minimum number of relationships between person1 and person2.
    """

    visited = set()
    queue = [(person1, 0)]  # (current person, current degree)
    
    while queue:
        current_person, degree = queue.pop(0)
        
        if current_person == person2:
            return degree
        
        if current_person in visited:
            continue
        
        visited.add(current_person)
        
        for rel in get_all_relationships(current_person):
            next_person = rel['person1'] if rel['person2'] == current_person else rel['person2']
            if next_person not in visited:
                queue.append((next_person, degree + 1))
    
    return -1  # If no relationship found