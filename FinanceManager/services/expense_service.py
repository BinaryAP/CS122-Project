from models.expense import Expense
from repositories.expense_db import ExpenseDB

class ExpenseService:

    @staticmethod
    def add_expense(name, description, amount, category_name, date_purchased, user_id):
        new_expense = Expense(name, description, amount, category_name, date_purchased, user_id)
        new_expense = ExpenseDB.add_new_expense(new_expense)
        return new_expense

    @staticmethod
    def view_expenses(user_id, start_date, end_date):
        expenses = ExpenseDB.view_specific_user_expense(user_id, start_date, end_date)
        return expenses