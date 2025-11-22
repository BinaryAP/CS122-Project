from db import get_connection
from models.category import Category

class CategoryDB:

    @staticmethod
    def get_all_categories():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT category_name FROM Category")
        categories = cursor.fetchall()
        print (f"In Category_DB.get_all categories, catetogy: {categories}")
        cursor.close()
        conn.close()

        return categories

    @staticmethod
    def create_new_category(category: Category):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "INSERT INTO Category (category_name, description) VALUES (%s, %s)"
        cursor.execute(sql, (
            category.name,
            category.description
        ))
        conn.commit()

        cursor.close()
        conn.close()

        return category