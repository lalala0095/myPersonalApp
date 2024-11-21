from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required, admin_required
from app.forms.forms import UserForm
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route('/users_records', methods=['GET', 'POST'])
@login_required
def users():
    db = current_app.db
   
    # Fetch all users records from the database
    users_records = list(db.users.find())
    return render_template('users.html', users_records=users_records)


@users_blueprint.route('/users_add', methods=['GET', 'POST'])
@admin_required
def users_add():
    db = current_app.db
    users_records = list(db.users.find())
    form = UserForm()

    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = db.users.find_one({'username': form.username.data})
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('users_blueprint.users_add'))
        else:
            existing_user = db.users.find_one({'username': form.username.data})
            
        # Hash the password
        hashed_password = generate_password_hash(form.password.data)
        is_admin = form.is_admin.data == 'True'
        db_count = db['users'].count_documents({})
        # Save the new account to MongoDB
        db.users.insert_one({
            'user_id': db_count,
            'date_inserted': datetime.now(),
            'account_id': session['account_id'],
            'username': form.username.data.strip(),
            'password': hashed_password,
            'name': form.name.data.strip().title(),
            'email': form.email.data.strip().lower(),
            'is_admin': is_admin
        })

        flash("Account created successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template('users_add.html', form=form, users_records=users_records)



# Route to delete a users record
@users_blueprint.route('/users_delete/<string:record_id>', methods=['POST'])
@login_required
def users_delete(record_id):
    db = current_app.db
    try:
        db.users.delete_one({"_id": ObjectId(record_id)})
        flash("User record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('users_blueprint.users'))

@users_blueprint.route('/users_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def users_edit(record_id):
    db = current_app.db
    record = db.users.find_one({"_id": ObjectId(record_id)})
    users = list(db.users.find())

    if not record:
        flash("User record not found!", "danger")
        return redirect(url_for('users_blueprint.users'))

    if request.method == 'POST':
        date_inserted = request.form.get('date_inserted')
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        price = request.form.get('price')
        user_type = request.form.get('user_type')
        date_updated = datetime.now()

        if user_name and user_id:
            updated_record = {
                "date_inserted": date_inserted,
                "user_id": int(user_id),
                "user_name": user_name,
                "user_type": user_type,
                "price": float(price),
                "date_updated": date_updated
            }
            try:
                db.users.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                flash("User record updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating record: {e}", "danger")
            return redirect(url_for('users_blueprint.users'))

        flash("All fields are required!", "danger")

    return render_template('users_edit.html', record=record, users=users)