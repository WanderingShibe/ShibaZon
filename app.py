import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager

from models import User, db
from routes import configure_routes

# Load environment variables from .env file
load_dotenv()


def create_app(config_name=None):
    # Initialise the Flask instance, the and the login manager
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"  # type: ignore

    # Get required secret key and database URI
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Configure seperate configurations for testing database and real database
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Load the user ID stored in the session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    configure_routes(app)

    return app


# Run the application and update any new database changes
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
