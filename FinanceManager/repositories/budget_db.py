from db import get_connection
from models.budget import Budget

class BudgetDB:

    @staticmethod
    def add_new_budget(budget: Budget):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = ("INSERT INTO Budget (amount, category_name, month, year, user_id)"
               "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(sql, (
            budget.amount,
            budget.category_name,
            budget.month,
            budget.year,
            budget.user_id
        ))
        conn.commit()

        cursor.close()
        conn.close()

        return budget

    @staticmethod
    def review_budget(user_id, month, year):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Budget WHERE user_id=%s AND month=%s AND year=%s", (user_id, month, year))
        budget = cursor.fetchall()
        cursor.close()
        conn.close()

        return budget


