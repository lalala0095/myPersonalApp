from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.scripts.encrypt_card import encrypt_account_number
from werkzeug.security import generate_password_hash
from app.forms.cards import CardForm
import time

cards_blueprint = Blueprint('cards_blueprint', __name__)

@cards_blueprint.route('/cards_records', methods=['GET', 'POST'])
@login_required
def cards():
    db = current_app.db
   
    # Fetch all cards cards from the database
    cards_records = list(db.cards.find())
    return render_template('cards.html', cards_records=cards_records)


# @cards_blueprint.route('/cards_add', methods=['GET', 'POST'])
# @login_required
# def cards_add():
#     db = current_app.db
#     if request.method == 'POST':
#         # Add a new cards card
#         date_inserted = datetime.now()
#         count_of_card_existing = str(db['cards'].count_documents({}))
#         card_id = count_of_card_existing
#         card_name = request.form.get('card_name')
#         account_number = request.form.get('account_number')
#         card_type = request.form.get('card_type')
#         expiration = request.form.get('expiration')
#         cvv = request.form.get('cvv')

#         hashed_password = generate_password_hash(request.form.get('password'))

#         # store encryption to cards_encryptions
#         encrypt_account_number(card_id, account_number, expiration, cvv, hashed_password)
        
#         if card_name and account_number and hashed_password:
#             new_card = {
#                 "date_inserted": date_inserted,
#                 "account_id": session['account_id'],
#                 "card_id": card_id,
#                 "card_name": card_name,
#                 "card_type": card_type,
#                 "hashed password": hashed_password
#             }
#             db.cards.insert_one(new_card)
#             flash("Card added successfully!", "success")
#         else:
#             flash("All fields are required!", "danger")

#         return redirect(url_for('cards_blueprint.cards_add'))

#     # Fetch all cards cards from the database
#     cards_records = list(db.cards.find())
#     return render_template('cards_add.html', cards_records=cards_records)


@cards_blueprint.route('/cards_add', methods=['GET', 'POST'])
def cards_add():
    db = current_app.db
    cards_records = list(db.cards.find())
    form = CardForm()

    if form.validate_on_submit():
        flash("Please wait while the encryption is in progress. This may take some time.", "info")

        # Check if the card_name already exists
        existing_card = db.cards.find_one({'card_name': form.card_name.data})
        if existing_card:
            flash("Card already exists. Please choose a different one.", "danger")
            return render_template('cards_add.html', form=form, cards_records=cards_records)

        # Add a new card
        date_inserted = datetime.now()
        card_id = str(db['cards'].count_documents({}))  # Create card_id based on the current number of documents
        card_name = form.card_name.data
        account_number = form.account_number.data
        card_type = form.card_type.data
        expiration = form.expiration.data
        cvv = form.cvv.data
        
        hashed_password = generate_password_hash(form.password.data)  # Use form.password.data to get the password value

        encrypt_account_number(card_id, account_number, expiration, cvv, hashed_password)
        
        if card_name and account_number and hashed_password:
            new_card = {
                "date_inserted": date_inserted,
                "account_id": session['account_id'],
                "card_id": card_id,
                "card_name": card_name,
                "card_type": card_type,
                "hashed_password": hashed_password
            }
            db.cards.insert_one(new_card)
            flash("Card added successfully!", "success")
        else:
            flash("All fields are required!", "danger")

        return redirect(url_for('cards_blueprint.cards_add'))

    return render_template('cards_add.html', form=form, cards_records=cards_records)


# Route to delete a cards card
@cards_blueprint.route('/cards_delete/<string:card_id>', methods=['POST'])
@login_required
def cards_delete(card_id):
    db = current_app.db
    try:
        card_id_doc = db.cards.find_one({"_id": ObjectId(card_id)})
        card_id_real = card_id_doc['card_id']

        db.cards.delete_one({"_id": ObjectId(card_id)})
        # flash(type(card_id_real))
        flash(f"Deleting card record for: {card_id_doc['card_name']}")

        db.card_encryptions.delete_many({"card_id": card_id_real})
        
        flash("Card record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting card: {e}", "danger")
    return redirect(url_for('cards_blueprint.cards'))

@cards_blueprint.route('/cards_edit/<string:card_id>', methods=['GET', 'POST'])
@login_required
def cards_edit(card_id):
    db = current_app.db
    card = db.cards.find_one({"_id": ObjectId(card_id)})
    cards = list(db.cards.find())

    if not card:
        flash("Card not found!", "danger")
        return redirect(url_for('cards_blueprint.cards'))

    if request.method == 'POST':
        date_inserted = request.form.get('date_inserted')
        account_id = session['account_id']
        card_id_int = request.form.get('card_id')
        card_name = request.form.get('card_name')
        card_type = request.form.get('card_type')
        expiration = request.form.get('expiration')
        cvv = request.form.get('cvv')
        date_updated = datetime.now()

        if card_name and card_id:
            updated_card = {
                "date_inserted": date_inserted,
                "account_id": account_id,
                "card_id": card_id_int,
                "card_name": card_name,
                "card_type": card_type,
                "expiration": expiration,
                "cvv": cvv,
                "date_updated": date_updated
            }
            try:
                db.cards.update_one({"_id": ObjectId(card_id)}, {"$set": updated_card})
                flash("cards card updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating card: {e}", "danger")
            return redirect(url_for('cards_blueprint.cards'))

        flash("All fields are required!", "danger")

    return render_template('cards_edit.html', card=card, cards=cards)