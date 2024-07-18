import os
from flask import Flask, send_from_directory
from .extensions import db, migrate, login_manager, bcrypt, jwt
from .models import Author, Song
from .routes import register_routes
from .auth_routes import register_auth_routes


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), '../frontend/dist'),
        static_url_path=''
    )

    # Настройки приложения
    app.config.from_object('backend.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    register_routes(app)
    register_auth_routes(app)

    @app.route('/')
    def serve_vue_app(path='index.html'):
        return send_from_directory(app.static_folder, path)

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')

    return app
