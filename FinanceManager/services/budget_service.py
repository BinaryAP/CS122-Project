from models.budget import Budget
from repositories.budget_db import BudgetDB

class BudgetService:

    @staticmethod
    def add_budget(amount, category_name, month, year, user_id):
        new_budget = Budget(amount, category_name, month, year, user_id)
        new_budget = BudgetDB.add_new_budget(new_budget)
        return new_budget

    @staticmethod
    def view_budgets(user_id, month, year):
        budgets = BudgetDB.review_budget(user_id, month, year)
        return budgets