from .extensions import login_manager
from .models import User


@login_manager.user_loader
def load_user(user_id):
    print("Loading user")
    return User.query.get(int(user_id))
