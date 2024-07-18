import random

import names
import requests
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import AddFundsForm, LoginForm, RegistrationForm
from models import CartItem, Product, User, db


def configure_routes(app):

    @app.route("/")
    @login_required
    def index():
        page = request.args.get("page", 1, type=int)
        per_page = 9

        # Check if there existing products in the database, if not request new Shibas
        # Max amount per queries is 25
        products_count = Product.query.count()
        if products_count < 25:
            response = requests.get("https://dog.ceo/api/breed/shiba/images/random/25")
            # Convert the response from Dog.Ceo and store the URL.
            # Give each Shiba a random name
            shibas = response.json().get("message", [])
            shibas_data = [
                {
                    "image_url": url,
                    "name": f"Shiba {names.get_first_name()}",
                    "price": round(random.uniform(10, 100), 2),
                }
                for url in shibas
            ]
            # Add newly created Shibas to the database if none already exist
            for shiba in shibas_data:
                product = Product.query.filter_by(image_url=shiba["image_url"]).first()
                if not product:
                    new_product = Product(
                        name=shiba["name"],
                        price=shiba["price"],
                        image_url=shiba["image_url"],
                    )
                    db.session.add(new_product)
            db.session.commit()

        # Use index.html as the template to render the shibas and handle max amount per page
        products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        next_url = (
            url_for("index", page=products.next_num) if products.has_next else None
        )
        prev_url = (
            url_for("index", page=products.prev_num) if products.has_prev else None
        )
        return render_template(
            "index.html", products=products.items, next_url=next_url, prev_url=prev_url
        )

    # Handles creating new users and registering them
    @app.route("/register", methods=["GET", "POST"])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = generate_password_hash(
                form.password.data, method="pbkdf2:sha256"
            )
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password,
                balance=100.00,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    # Handles logging in the user
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=True)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("index"))
            else:
                flash("Login Unsuccessful. Please check email and password", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    # Handles the user adding additional funds to account
    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account():
        form = AddFundsForm()
        if form.validate_on_submit():
            current_user.balance += form.amount.data
            db.session.commit()
            flash("Your balance has been updated!", "success")
        return render_template("account.html", form=form)

    # Adds Shibas to user's cart, adds duplicates
    @app.route("/add_to_cart/<int:product_id>")
    @login_required
    def add_to_cart(product_id):
        product = Product.query.get(product_id)
        if product:
            cart_item = CartItem.query.filter_by(
                user_id=current_user.id, product_id=product_id
            ).first()
            if cart_item:
                cart_item.quantity += 1
            else:
                cart_item = CartItem(user_id=current_user.id, product_id=product_id)
                db.session.add(cart_item)
            db.session.commit()
            flash(f"Added {product.name} to your cart!", "success")
        return redirect(url_for("index"))

    # Stores the item the user has purchased
    @app.route("/cart")
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        rounded_total = round(total, 2)
        return render_template("cart.html", cart_items=cart_items, total=total)

    # Handles user paying for items, and deleting them from cart_item
    @app.route("/checkout")
    @login_required
    def checkout():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total_cost = sum(item.product.price * item.quantity for item in cart_items)
        if current_user.balance >= total_cost:
            current_user.balance -= total_cost
            for item in cart_items:
                db.session.delete(item)
            db.session.commit()
            flash("Purchase successful! Thank you for your purchase.", "success")
        else:
            flash("Insufficient funds to complete the purchase.", "danger")
        return redirect(url_for("cart"))
