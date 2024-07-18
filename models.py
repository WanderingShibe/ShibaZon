from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Initialising the SQLAlchemy instance into the project
db = SQLAlchemy()


# Creating the User class, with flask_login handling the authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password_hash, balance):
        self.username = username
        self.email = email
        self.password_hash = password_hash


# Creating the Product class for the Shiba images
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, default=1)
    image_url = db.Column(db.String(500), nullable=False)

    def __init__(self, name, price, image_url):
        self.name = name
        self.price = price
        self.image_url = image_url


# Creating the cart item model for the items the user wants to purchase
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    # Establishing the connection between the models
    user = db.relationship("User", backref=db.backref("cart_items", lazy=True))
    product = db.relationship("Product", backref=db.backref("cart_items", lazy=True))
