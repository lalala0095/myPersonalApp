from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.forms import AccountForm
from werkzeug.security import generate_password_hash
from app.config import db
from flask_pymongo import MongoClient

accounts = Blueprint('accounts', __name__)

@accounts.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AccountForm()
    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = db.accounts.find_one({'username': form.username.data})   
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('accounts.signup'))
        
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Save the new account to MongoDB
        db.accounts.insert_one({
            'username': form.username.data.strip(),
            'password': hashed_password,
            'name': form.name.data.strip().title(),
            'email': form.email.data.strip().lower(),
            'subscription': form.subscription.data
        })

        flash("Account created successfully!", "success")
        return redirect(url_for('main.index'))

    return render_template('add_account.html', form=form)