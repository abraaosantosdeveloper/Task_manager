"""
Authentication Routes
"""
from flask import Blueprint
from api.controllers import auth_controller
from api.middleware.auth import token_required, get_current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    return auth_controller.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    return auth_controller.login()

@auth_bp.route('/me', methods=['GET'])
@token_required
def me():
    """Get current user info"""
    return auth_controller.me(get_current_user())

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    return auth_controller.update_profile(get_current_user())
