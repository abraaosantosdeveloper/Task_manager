"""
Authentication Controller
Handles HTTP requests for authentication
"""
from flask import request
from api.workers.auth_worker import AuthWorker
from api.utils.responses import (
    success_response, error_response, created_response,
    validation_error_response, server_error_response
)

auth_worker = AuthWorker()

def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validation
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        errors = {}
        if not email:
            errors['email'] = "Email is required"
        if not password:
            errors['password'] = "Password is required"
        elif len(password) < 6:
            errors['password'] = "Password must be at least 6 characters"
        if not name:
            errors['name'] = "Name is required"
        
        if errors:
            return validation_error_response(errors)
        
        # Register user
        result = auth_worker.register(email, password, name)
        
        return created_response(result, "User registered successfully")
        
    except ValueError as e:
        return error_response(str(e), status_code=409)
    except Exception as e:
        print(f"Registration error: {e}")
        return server_error_response("Registration failed")

def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validation
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        errors = {}
        if not email:
            errors['email'] = "Email is required"
        if not password:
            errors['password'] = "Password is required"
        
        if errors:
            return validation_error_response(errors)
        
        # Login user
        result = auth_worker.login(email, password)
        
        return success_response(result, "Login successful")
        
    except ValueError as e:
        return error_response(str(e), status_code=401)
    except Exception as e:
        print(f"Login error: {e}")
        return server_error_response("Login failed")

def me(current_user):
    """Get current user info"""
    try:
        return success_response({
            "id": current_user['id'],
            "email": current_user['email'],
            "name": current_user['name'],
            "created_at": str(current_user['created_at'])
        })
    except Exception as e:
        print(f"Error getting user info: {e}")
        return server_error_response()
