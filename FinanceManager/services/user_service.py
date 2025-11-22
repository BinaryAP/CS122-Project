from models.user import User
from repositories.user_db import UserDB

class UserService:

    @staticmethod
    def login(userID, password_input):
        user = UserDB.get_user_details(userID)
        print (f"In UserService.login: {user}")
        if user and (user['password'] == password_input):
            return user
        return None

