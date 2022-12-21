"""Service for creating a user"""
from models.user import User
from request_exception import RequestException


class CreateUserService:
    """Service for creating a user"""
    @staticmethod
    def create_user(user_repository, username):
        """Create a user in the repository
        @:param user_repository: Repository to create user in
        @:param username: Username of new user
        @:returns: user ID of newly-created user
        @:raises: RequestException if request is invalid
        """
        if username is None or username == "":
            raise RequestException('Missing username')
        user = User(user_id=0, username=username)
        user_repository.create(user)
        return user.user_id
