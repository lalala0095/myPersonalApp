from app import create_app
from flask import render_template, Flask, Blueprint
from app.routes.sales import sales_blueprint
from app.routes.accounts import accounts
from app.routes.products import products_blueprint

app = create_app()
app.register_blueprint(sales_blueprint, url_prefix='/sales')
app.register_blueprint(accounts)
app.register_blueprint(products_blueprint, url_prefix='/products')

# Placeholder for a dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", title="Sales Dashboard")

if __name__ == "__main__":
    app.run(debug=True)