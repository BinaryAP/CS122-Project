from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
from models import Database, User, Category, Transaction
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret key in production

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'budget_app'
}

def get_db():
    """Get database connection"""
    db = Database(**DB_CONFIG)
    db.connect()
    return db

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        db = get_db()
        user = User(username=username, email=email, password=password)
        
        if user.create(db):
            db.disconnect()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            db.disconnect()
            flash('Username or email already exists', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = get_db()
        user = User.authenticate(db, username, password)
        db.disconnect()
        
        if user:
            session['user_id'] = user.user_id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    db = get_db()
    user_id = session['user_id']
    
    # Get summary
    summary = Transaction.get_summary(db, user_id)
    
    # Get recent transactions
    recent_transactions = Transaction.get_by_user(db, user_id, limit=10)
    
    # Get monthly trend
    monthly_trend = Transaction.get_monthly_trend(db, user_id, months=6)
    
    # Get category breakdown
    expense_breakdown = Transaction.get_category_breakdown(db, user_id, 'expense')
    income_breakdown = Transaction.get_category_breakdown(db, user_id, 'income')
    
    db.disconnect()
    
    return render_template('dashboard.html',
                         summary=summary,
                         recent_transactions=recent_transactions,
                         monthly_trend=monthly_trend,
                         expense_breakdown=expense_breakdown,
                         income_breakdown=income_breakdown)

@app.route('/transactions')
@login_required
def transactions():
    """View all transactions"""
    db = get_db()
    user_id = session['user_id']
    
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    all_transactions = Transaction.get_by_user(db, user_id, 
                                              start_date=start_date, 
                                              end_date=end_date)
    categories = Category.get_by_user(db, user_id)
    
    db.disconnect()
    
    return render_template('transactions.html',
                         transactions=all_transactions,
                         categories=categories,
                         start_date=start_date,
                         end_date=end_date)

@app.route('/transaction/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add new transaction"""
    db = get_db()
    user_id = session['user_id']
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        transaction_date = request.form.get('transaction_date')
        trans_type = request.form.get('type')
        
        if not all([category_id, amount, transaction_date, trans_type]):
            flash('Please fill in all required fields', 'danger')
            categories = Category.get_by_user(db, user_id)
            db.disconnect()
            return render_template('add_transaction.html', categories=categories)
        
        transaction = Transaction(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            description=description,
            transaction_date=transaction_date,
            type=trans_type
        )
        
        if transaction.create(db):
            db.disconnect()
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('transactions'))
        else:
            db.disconnect()
            flash('Error adding transaction', 'danger')
    
    categories = Category.get_by_user(db, user_id)
    db.disconnect()
    
    return render_template('add_transaction.html', categories=categories)

@app.route('/transaction/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    """Edit transaction"""
    db = get_db()
    user_id = session['user_id']
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        amount = request.form.get('amount')
        description = request.form.get('description')
        transaction_date = request.form.get('transaction_date')
        trans_type = request.form.get('type')
        
        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            description=description,
            transaction_date=transaction_date,
            type=trans_type
        )
        
        if transaction.update(db):
            db.disconnect()
            flash('Transaction updated successfully!', 'success')
            return redirect(url_for('transactions'))
        else:
            db.disconnect()
            flash('Error updating transaction', 'danger')
    
    # Get transaction details
    all_transactions = Transaction.get_by_user(db, user_id)
    transaction = next((t for t in all_transactions if t.transaction_id == transaction_id), None)
    
    if not transaction:
        db.disconnect()
        flash('Transaction not found', 'danger')
        return redirect(url_for('transactions'))
    
    categories = Category.get_by_user(db, user_id)
    db.disconnect()
    
    return render_template('edit_transaction.html', 
                         transaction=transaction, 
                         categories=categories)

@app.route('/transaction/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Delete transaction"""
    db = get_db()
    user_id = session['user_id']
    
    transaction = Transaction(transaction_id=transaction_id, user_id=user_id)
    
    if transaction.delete(db):
        db.disconnect()
        flash('Transaction deleted successfully!', 'success')
    else:
        db.disconnect()
        flash('Error deleting transaction', 'danger')
    
    return redirect(url_for('transactions'))

@app.route('/categories')
@login_required
def categories():
    """View all categories"""
    db = get_db()
    user_id = session['user_id']
    
    all_categories = Category.get_by_user(db, user_id)
    db.disconnect()
    
    return render_template('categories.html', categories=all_categories)

@app.route('/category/add', methods=['POST'])
@login_required
def add_category():
    """Add new category"""
    db = get_db()
    user_id = session['user_id']
    
    name = request.form.get('name')
    cat_type = request.form.get('type')
    
    if not all([name, cat_type]):
        flash('Please fill in all fields', 'danger')
        return redirect(url_for('categories'))
    
    category = Category(user_id=user_id, name=name, type=cat_type)
    
    if category.create(db):
        db.disconnect()
        flash('Category added successfully!', 'success')
    else:
        db.disconnect()
        flash('Category already exists or error occurred', 'danger')
    
    return redirect(url_for('categories'))

@app.route('/category/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete category"""
    db = get_db()
    user_id = session['user_id']
    
    category = Category(category_id=category_id, user_id=user_id)
    
    if category.delete(db):
        db.disconnect()
        flash('Category deleted successfully!', 'success')
    else:
        db.disconnect()
        flash('Cannot delete category with existing transactions', 'danger')
    
    return redirect(url_for('categories'))

@app.route('/reports')
@login_required
def reports():
    """View reports and analytics"""
    db = get_db()
    user_id = session['user_id']
    
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get summary
    summary = Transaction.get_summary(db, user_id, start_date, end_date)
    
    # Get category breakdowns
    expense_breakdown = Transaction.get_category_breakdown(db, user_id, 'expense', start_date, end_date)
    income_breakdown = Transaction.get_category_breakdown(db, user_id, 'income', start_date, end_date)
    
    # Get monthly trend
    monthly_trend = Transaction.get_monthly_trend(db, user_id, months=12)
    
    db.disconnect()
    
    return render_template('reports.html',
                         summary=summary,
                         expense_breakdown=expense_breakdown,
                         income_breakdown=income_breakdown,
                         monthly_trend=monthly_trend,
                         start_date=start_date,
                         end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
