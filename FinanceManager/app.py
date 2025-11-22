from flask import Flask, request, jsonify

from services.user_service import UserService
from services.category_service import CategoryService
from services.expense_service import ExpenseService
from services.income_service import IncomeService
from services.budget_service import BudgetService
from waitress import serve

app = Flask(__name__)
user_service = UserService()
category_service = CategoryService()
expense_service = ExpenseService()
income_service = IncomeService()
budget_service = BudgetService()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.post("/api/login")
def login_api():
    data = request.get_json()
    userID = data.get("userID")
    password = data.get("password")
    print (f"userid:{userID}, password:{password}")

    # Call service
    user = user_service.login(userID, password)

    if not user:
        return jsonify({"success": False, "message": "Invalid User ID or Password"}), 401

    # Convert user object → JSON response
    return jsonify({
        "success": True,
        "user": {
            "id": user['user_id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email']
        }
    })

@app.get("/api/categories")
def category_api():

    # Call service
    category = category_service.categories()

    if not category:
        return jsonify({"success": False, "message": "Invalid Category Name"}), 401

    # Convert user object → JSON response
    return jsonify(category)

@app.post("/api/add_category")
def add_category_api():
    data = request.get_json()
    name = data.get("category_name")
    description = data.get("description")
    # Call service
    category = category_service.add_category(name, description)

    if not category:
        return jsonify({"success": False, "message": "Category could not be added"}), 401

    # Convert user object → JSON response
    return jsonify({"category_name": category.name, "description": category.description})

@app.post("/api/add_expense")
def add_expense_api():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    amount = data.get("amount")
    category_name = data.get("category_name")
    date_purchased = data.get("date_purchased")
    user_id = data.get("user_id")

    # Call service
    expense = expense_service.add_expense(name, description, amount, category_name, date_purchased, user_id)

    if not expense:
        return jsonify({"success": False, "message": "Expense could not be added"}), 401

    # Convert user object → JSON response
    return jsonify (
        {"name": expense.name,
         "description": expense.description,
         "amount": expense.amount,
         "category_name": expense.category_name,
         "date_purchased": expense.date_purchased,
         "user_id": expense.user_id
         }
    )

@app.post("/api/view_expenses")
def view_expense_api():
    data = request.get_json()
    user_id = data.get("user_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # print(f"user: {user_id}, start: {start_date}, end: {end_date}", )
    # Call service
    # expense = expense_service.view_expenses(userID, start_date, end_date)
    expense = expense_service.view_expenses(user_id, start_date, end_date)
    if not expense:
        return jsonify({"success": False, "message": "Invalid User or No expenses in that date range"}), 401

    # Convert user object → JSON response
    return jsonify(expense)

@app.post("/api/add_income")
def add_income_api():
    data = request.get_json()
    amount = data.get("amount")
    user_id = data.get("user_id")

    # Call service
    income = income_service.add_income(amount, user_id)

    if not income:
        return jsonify({"success": False, "message": "Income could not be added"}), 401

    # Convert user object → JSON response
    return jsonify (
        {"amount": income.amount,
         "user_id": income.user_id
         }
    )

@app.post("/api/view_income")
def view_income_api():
    data = request.get_json()
    user_id = data.get("user_id")

    # Call service
    income = income_service.view_income(user_id)
    if not income:
        return jsonify({"success": False, "message": "Invalid User"}), 401

    # Convert user object → JSON response
    return jsonify(income)

@app.post("/api/add_budget")
def add_budget_api():
    data = request.get_json()
    amount = data.get("amount")
    category_name = data.get("category_name")
    month = data.get("month")
    year = data.get("year")
    user_id = data.get("user_id")

    # Call service
    budget = budget_service.add_budget(amount, category_name, month, year, user_id)

    if not budget:
        return jsonify({"success": False, "message": "Budget could not be added"}), 401

    # Convert user object → JSON response
    return jsonify (
        {"amount": budget.amount,
         "category_name": budget.category_name,
         "month": budget.month,
         "year": budget.year,
         "user_id": budget.user_id
         }
    )

@app.post("/api/view_budgets")
def review_budget_api():
    data = request.get_json()
    user_id = data.get("user_id")
    month = data.get("month")
    year = data.get("year")

    # Call service
    budget = budget_service.view_budgets(user_id, month, year)
    if not budget:
        return jsonify({"success": False, "message": "No budgets align with select timeframe"}), 401

    # Convert user object → JSON response
    return jsonify(budget)


if __name__ == '__main__':
    serve(host="0.0.0.0", port=8000)
