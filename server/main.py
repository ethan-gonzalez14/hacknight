class Bio:
    def __init__(self, name: str, bioPublic: str, bioPrivate: str, socials: str, friendCode: str):
        self.name = name
        self.bioPublic = bioPublic
        self.bioPrivate = bioPrivate
        self.socials = socials
        self.friendCode = friendCode
    def __repr__(self):
        return f"Bio({self.name}, {self.bioPublic}, {self.bioPrivate}, {self.socials})"
    def jsonify(self, base: str):
        return f"""{
            "person": {self.name},
            "time": {self.bioPublic},
            "location": {self.bioPrivate},
            "context": {self.socials},
            "friends": {"true" if self.friends else "false"}
        }"""



def setBio():

def getUserBio(): # from BioTable


def getRelationType():

def getClosestPath():

# hold to select new center of web
def toggleRoot():


def connect():

# connect() helpers
def setLocation():

# def setRelation():
