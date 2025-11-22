from models.category import Category
from repositories.category_db import CategoryDB

class CategoryService:

    @staticmethod
    def categories():
        all_categories = CategoryDB.get_all_categories()
        return all_categories

    @staticmethod
    def add_category(name, desc):
        new_category = Category(name, desc)
        new_category = CategoryDB.create_new_category(new_category)
        return new_category