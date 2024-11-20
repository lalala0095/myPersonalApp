from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from pymongo import MongoClient
from app.config import Config
from datetime import datetime

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route('/products_records', methods=['GET', 'POST'])
def products():
    db = current_app.db
    if request.method == 'POST':
        # Add a new products record
        date_inserted = datetime.now()
        count_of_product_existing = str(db['products'].count_documents({}))
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
            db.products.insert_one(new_record)
            flash("Products record added successfully!", "success")
        else:
            flash("All fields are required!", "danger")

        return redirect(url_for('products_blueprint.products'))

    # Fetch all products records from the database
    products_records = list(db.products.find())
    print("Products Records:", products_records)  # Debugging: Check the data passed to the template
    return render_template('products.html', products_records=products_records)
