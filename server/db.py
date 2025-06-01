def run(query: str):
    """
    Executes a SQL query against the database.
    This function should be implemented to connect to your database and execute the query.
    """
    raise NotImplementedError("This function should be implemented to run SQL queries against your database.")


def insert_relationship(person1: str, person2: str, time: int, location: str, context: str, friends: bool):
    """
    Inserts a relationship between person1 and person2, made at the time and location, into the database.
    An optional context about how they met can also be provided.
    """
