from models.income import Income
from repositories.income_db import IncomeDB

class IncomeService:

    @staticmethod
    def add_income(amount, user_id):
        new_income = Income(amount, user_id)
        new_income = IncomeDB.add_recent_income(new_income)
        return new_income

    @staticmethod
    def view_income(user_id):
        income = IncomeDB.view_income(user_id)
        return income