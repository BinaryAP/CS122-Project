class Expense:
    def __init__(self, name=None, description=None, amount=None, category_name=None, date_purchased=None, user_id=None):
        self.name = name
        self.description = description
        self.amount = amount
        self.category_name = category_name
        self.date_purchased = date_purchased
        self.user_id = user_id