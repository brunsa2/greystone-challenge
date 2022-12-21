"""Memory-based user repository"""
from models.user import User


class UserRepository:
    """Memory-based user repository"""
    def __init__(self):
        self.users = {}
        self.next_id = 1

    def create(self, user: User):
        """Create a new user

        Autoincrement ID will be assigned to the user object.

        @:param user: User object to create
        """
        next_id = self.next_id
        self.next_id += 1
        user.user_id = next_id
        self.users[next_id] = user

    def read(self, user_id: int):
        """Read user from the repository.
        @:param user_id: ID of user to read
        @:returns: User object
        """
        return self.users.get(user_id)
