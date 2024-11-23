from flask import Blueprint, render_template, current_app, redirect, url_for, flash, session, request
import pandas as pd
from app.forms.forms import AccountForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes.login_required import login_required

main = Blueprint('main', __name__)

def authenticate_user(username, password, db):
    """
    Authenticate user credentials.
    Returns the user document if valid, else None.
    """
    user = db['users'].find_one({'username': username}) or db['accounts'].find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return user
    return None

@main.route("/")
@login_required
def index():
    db = current_app.db
    # total_sales = db.sales.aggregate([{'$group': {'_id': None, 'total': {'$sum': '$total'}}}]).next().get('total', 0)
    total_sales = None
    total_cards = db.cards.count_documents({})

    return render_template("dashboard.html", title="Dashboard", cards_blueprint={"cards": True}, total_cards=total_cards)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db = current_app.db
        username = form.username.data.strip()
        password = form.password.data.strip()
        
        user = authenticate_user(username, password, db)
        if user:
            session['user_id'] = user.get('user_id') or None
            session['is_admin'] = user.get('is_admin', False)
            session['account_id'] = user.get('account_id', None)

            flash("Login successful!", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Invalid username or password. Please try again.", "danger")
    
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash("You have been logged out.", "info")
    return redirect(url_for('main.login'))  # Redirect to login page

@main.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    form = AccountForm()
    db = current_app.db

    if form.validate_on_submit():
        if db.accounts.find_one({'username': form.username.data}):
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('main.admin_signup'))
        
        hashed_password = generate_password_hash(form.password.data)
        count_docs = db.accounts.count_documents({})
        
        db.accounts.insert_one({
            'account_id': count_docs,
            'username': form.username.data.strip(),
            'password': hashed_password,
            'name': form.name.data.strip().title(),
            'email': form.email.data.strip().lower(),
            'subscription': form.subscription.data,
            'is_admin': True
        })

        flash("Admin account created successfully!", "success")
        return redirect(url_for('main.login'))

    return render_template('admin_signup.html', form=form)
