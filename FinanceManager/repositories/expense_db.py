from db import get_connection
from models.expense import Expense

class ExpenseDB:

    @staticmethod
    def add_new_expense(expense: Expense):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = ("INSERT INTO Expense (name, description, amount, category_name, date_purchased, user_id)"
               "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (
            expense.name,
            expense.description,
            expense.amount,
            expense.category_name,
            expense.date_purchased,
            expense.user_id
        ))
        conn.commit()

        cursor.close()
        conn.close()

        return expense

    @staticmethod
    def view_specific_user_expense(user_id, start_date, end_date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Expense WHERE user_id=%s AND date_purchased >= %s AND date_purchased <= %s",
                       (user_id, start_date, end_date))
        expense = cursor.fetchall()
        cursor.close()
        conn.close()

        return expense