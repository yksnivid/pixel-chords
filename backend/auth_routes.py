from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .extensions import db, bcrypt, limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/users', methods=['POST'])
@limiter.limit("3 per minute")
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'User with that email or username already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@limiter.limit("3 per minute")
@login_required
def delete_user(user_id):

    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized to delete'}), 401

    password = request.get_json().get('password')
    user = User.query.get(user_id)

    if not user.check_password(password):
        return jsonify({'message': 'Wrong password'}), 401

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Deleted successfully'}), 200


@auth_bp.route('/api/users/<int:user_id>/password', methods=['PUT'])
@limiter.limit("3 per minute")
@login_required
def change_password(user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Unauthorized to change password'}), 401

    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not current_user.check_password(current_password):
        return jsonify({'message': 'Wrong password'}), 401

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200


@auth_bp.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role,

            'message': 'Logged in successfully'
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/api/current_user', methods=['GET'])
@limiter.limit("60 per minute")
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role
        }), 200
    return jsonify({'error': 'User not authenticated'}), 401


def register_auth_routes(app):
    app.register_blueprint(auth_bp)
