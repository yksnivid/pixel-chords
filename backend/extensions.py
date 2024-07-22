from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    from .models import User  # import User model from models.py file
    return User.query.get(int(user_id))
