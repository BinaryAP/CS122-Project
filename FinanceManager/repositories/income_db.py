from db import get_connection
from models.income import Income

class IncomeDB:

    @staticmethod
    def add_recent_income(income: Income):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = ("INSERT INTO Income (amount, user_id) VALUES (%s, %s)")
        cursor.execute(sql, (
            income.amount,
            income.user_id
        ))
        conn.commit()

        cursor.close()
        conn.close()

        return income

    @staticmethod
    def view_income(user_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT income.amount FROM Income WHERE user_id=%s"
        cursor.execute(sql, (user_id,))
        income = cursor.fetchone()
        cursor.close()
        conn.close()

        return income