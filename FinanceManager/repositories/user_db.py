from db import get_connection
from models.user import User

class UserDB:
    @staticmethod
    def get_user_details(userID):
        conn = get_connection()
        print (f"In UserDB.get_user_details, conn: {conn}, userID: {userID}")
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM User WHERE user_id=%s", (userID,))
        user = cursor.fetchone()
        print (f"In UserDB.get_user_details, user: {user}")
        cursor.close()
        conn.close()

        return user

