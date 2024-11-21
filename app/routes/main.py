from flask import Blueprint, render_template, current_app, redirect, url_for, flash, session
import pandas as pd
from app.forms.forms import AccountForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes.login_required import login_required

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def index():
    db = current_app.db
    df_sales = pd.DataFrame(list(db.sales.find()))
    total_sales = df_sales['total'].sum()

    total_products = db.products.count_documents({})
    total_sales = df_sales['total'].sum()

    sales_url = '/sales/sales'
    users_url = '/users/users'
    products_url = '/products/products'
    return render_template("dashboard.html", 
                           title="Dashboard", 
                           total_sales=total_sales, 
                           total_products=total_products,
                           sales_url=sales_url,
                           products_url=products_url,
                           users_url=users_url)

@main.route('/login', methods=['GET', 'POST'])
def login():
    db = current_app.db
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Check the MongoDB 'accounts' collection for the user
        user = db['users'].find_one({'username': username})
        if user is None:
            flash("option 1")
            user = db['accounts'].find_one({'username': username})
            if user and check_password_hash(user['password'], password):
                flash("option 2")
                session['user_id'] = None
                session['is_admin'] = True
                session['account_id'] = user['account_id']
                flash("Login successful!", "success")
                return redirect(url_for('main.index'))
        elif user and check_password_hash(user['password'], password):
            flash("option 3")
            session['user_id'] = user['user_id']
            session['is_admin'] = user['is_admin']
            session['account_id'] = user['account_id']
            flash("Login successful!", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid password. Please try again.", "danger")
    else:
        flash("Invalid username. Please check your credentials.", "danger")

    return render_template('login.html', form=form, is_admin = True)

@main.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('main.index'))  # Redirect to the login page


@main.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    db = current_app.db

    form = AccountForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = db.accounts.find_one({'username': form.username.data})   
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('main.signup'))
        
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        count_docs = db.accounts.count_documents({})
        # Save the new account to MongoDB
        db.accounts.insert_one({
            'account_id': count_docs, 
            'username': form.username.data.strip(),
            'password': hashed_password,
            'name': form.name.data.strip().title(),
            'email': form.email.data.strip().lower(),
            'subscription': form.subscription.data,
            'is_admin': True
        })

        flash("Account created successfully!", "success")
        return redirect(url_for('main.index'))

    return render_template('admin_signup.html', form=form)
