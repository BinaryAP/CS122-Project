class User:
    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, password=None):
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.created_at = None
