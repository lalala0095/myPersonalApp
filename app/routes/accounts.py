from flask import Blueprint, render_template, redirect, url_for
from app.forms.forms import AccountForm  # Import the AccountForm

accounts = Blueprint('accounts', __name__)

@accounts.route('/', methods=['GET', 'POST'])
def index():
    form = AccountForm()  # Create an instance of the form
    if form.validate_on_submit():
        # Handle form submission here
        pass
    
    return render_template('add_account.html', form=form)  # Pass the form to the template

# @accounts.route("/add_account")
# def add_account():
#     form = AccountForm()

#     if form.validate_on_submit():
#         username = form.username.data
#         return redirect(url_for('index'))

#     return render_template("add_account.html", form=form)