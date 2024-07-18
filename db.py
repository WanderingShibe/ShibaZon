import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import CartItem, Product, User, db

# Import variables from .env file
load_dotenv()

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_HOST = os.getenv("DATABASE_HOST")

# Initialize the Flask application
app = Flask(__name__)

# Creating the DB URI and configuring SQLAlchemy
DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy db instance
db.init_app(app)

# Create an engine
engine = create_engine(DATABASE_URI)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create the database and the database table
with app.app_context():
    print("Creating all tables...")
    db.create_all()
    print("Tables created successfully.")

    # # Create some test data
    # user1 = User(
    #     username="testuser1",
    #     email="testuser1@example.com",
    #     password_hash="hashed_password",
    # )
    # user2 = User(
    #     username="testuser2",
    #     email="testuser2@example.com",
    #     password_hash="hashed_password",
    # )

    # product1 = Product(
    #     name="Shiba Inu 1", price=9.99, image_url="http://example.com/shiba1.jpg"
    # )
    # product2 = Product(
    #     name="Shiba Inu 2", price=19.99, image_url="http://example.com/shiba2.jpg"
    # )

    # cart_item1 = CartItem(user_id=1, product_id=1)
    # cart_item2 = CartItem(user_id=1, product_id=2)
    # cart_item3 = CartItem(user_id=2, product_id=1)

    # # Add the records to the session
    # print("Adding records to the session...")
    # session.add(user1)
    # session.add(user2)
    # session.add(product1)
    # session.add(product2)
    # session.add(cart_item1)
    # session.add(cart_item2)
    # session.add(cart_item3)

    # # Commit the session to the database
    # print("Committing the session to the database...")
    # session.commit()
    # print("Records inserted successfully.")

print("Script execution completed.")
