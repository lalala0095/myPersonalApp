from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required

cogs_blueprint = Blueprint('cogs_blueprint', __name__)

@cogs_blueprint.route('/cogs_records', methods=['GET', 'POST'])
@login_required
def cogs():
    db = current_app.db
   
    # Fetch all cogs records from the database
    cogs_records = list(db.cogs.find())
    return render_template('cogs.html', cogs_records=cogs_records)


@cogs_blueprint.route('/cogs_add', methods=['GET', 'POST'])
@login_required
def cogs_add():
    db = current_app.db
    if request.method == 'POST':
        # Add a new cogs record
        date_inserted = datetime.now()
        count_of_product_existing = str(db['cogs'].count_documents({}))
        product_id = count_of_product_existing.zfill(6)
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('product_type')

        if product_name and price:
            new_record = {
                "date_inserted": date_inserted,
                "product_id": int(product_id),
                "product_name": product_name,
                "product_type": product_type,
                "price": float(price),
            }
            db.cogs.insert_one(new_record)
            print("successfully added product")
            flash("Cost of Goods record added successfully!", "success")
        else:
            flash("All fields are required!", "danger")
            print("failed to add product")

        return redirect(url_for('cogs_blueprint.cogs_add'))

    # Fetch all cogs records from the database
    cogs_records = list(db.cogs.find())
    return render_template('cogs_add.html', cogs_records=cogs_records)



# Route to delete a cogs record
@cogs_blueprint.route('/cogs_delete/<string:record_id>', methods=['POST'])
@login_required
def cogs_delete(record_id):
    db = current_app.db
    try:
        db.cogs.delete_one({"_id": ObjectId(record_id)})
        flash("cogs record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('cogs_blueprint.cogs'))

@cogs_blueprint.route('/cogs_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def cogs_edit(record_id):
    db = current_app.db
    record = db.cogs.find_one({"_id": ObjectId(record_id)})
    cogs = list(db.cogs.find())

    if not record:
        flash("cogs record not found!", "danger")
        return redirect(url_for('cogs_blueprint.cogs'))

    if request.method == 'POST':
        date_inserted = request.form.get('date_inserted')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        product_type = request.form.get('product_type')
        date_updated = datetime.now()

        if product_name and product_id:
            updated_record = {
                "date_inserted": date_inserted,
                "product_id": int(product_id),
                "product_name": product_name,
                "product_type": product_type,
                "price": float(price),
                "date_updated": date_updated
            }
            try:
                db.cogs.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                flash("cogs record updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating record: {e}", "danger")
            return redirect(url_for('cogs_blueprint.cogs'))

        flash("All fields are required!", "danger")

    return render_template('cogs_edit.html', record=record, cogs=cogs)