from flask import render_template, request, redirect, url_for, flash, Blueprint
from pymongo import MongoClient
from app.config import db
from datetime import datetime

sales_blueprint = Blueprint('sales_blueprint', __name__)

@sales_blueprint.route('/sales_records', methods=['GET', 'POST'])
def sales():
    if request.method == 'POST':
        # Add a new sales record
        date_inserted = datetime.now()
        product_name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        product_type = request.form.get('product_type')

        if product_name and quantity and price:
            new_record = {
                "date_inserted": date_inserted,
                "product_name": product_name,
                "quantity": int(quantity),
                "product_type": product_type,
                "price": float(price),
                "total": int(quantity) * float(price)
            }
            db.sales.insert_one(new_record)
            flash("Sales record added successfully!", "success")
        else:
            flash("All fields are required!", "danger")

        return redirect(url_for('sales_blueprint.sales'))

    # Fetch all sales records from the database
    sales_records = list(db.sales.find())
    return render_template('sales.html', sales_records=sales_records)
