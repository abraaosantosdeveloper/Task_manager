"""
Authentication Worker - Business logic for authentication
"""
import jwt
from datetime import datetime, timedelta
from api.repositories.user_repository import UserRepository
from api.utils.config import Config

class AuthWorker:
    """Handles authentication business logic"""
    
    def __init__(self):
        self.user_repo = UserRepository()
    
    def register(self, email, password, name):
        """Register a new user"""
        # Check if user exists
        if self.user_repo.email_exists(email):
            raise ValueError("Email already registered")
        
        # Create user
        user_id = self.user_repo.create_user(email, password, name)
        
        # Generate token
        token = self.generate_token(user_id, email)
        
        return {
            "token": token,
            "user": {
                "id": user_id,
                "email": email,
                "name": name
            }
        }
    
    def login(self, email, password):
        """Authenticate user and generate token"""
        # Find user
        user = self.user_repo.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not self.user_repo.verify_password(password, user['password']):
            raise ValueError("Invalid email or password")
        
        # Generate token
        token = self.generate_token(user['id'], user['email'])
        
        return {
            "token": token,
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user['name']
            }
        }
    
    def generate_token(self, user_id, email):
        """Generate JWT token"""
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )
        
        return token
    
    def verify_token(self, token):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
    
    def get_user_from_token(self, token):
        """Get user data from token"""
        payload = self.verify_token(token)
        user_id = payload.get('user_id')
        
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return user
    
    def update_profile(self, user_id, name, email, current_password=None, new_password=None):
        """Update user profile"""
        # Get current user (sem senha)
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if email is being changed and if it's already in use
        if email != user['email']:
            if self.user_repo.email_exists(email):
                raise ValueError("Email already in use")
        
        # If changing password, verify current password
        if new_password:
            if not current_password:
                raise ValueError("Current password is required to set a new password")
            
            # Get user with password for verification
            user_with_password = self.user_repo.find_by_email(user['email'])
            if not self.user_repo.verify_password(current_password, user_with_password['password']):
                raise ValueError("Current password is incorrect")
            
            if len(new_password) < 6:
                raise ValueError("New password must be at least 6 characters")
        
        # Update user
        updated_user = self.user_repo.update_user(user_id, name, email, new_password)
        
        return {
            "user": {
                "id": updated_user['id'],
                "name": updated_user['name'],
                "email": updated_user['email']
            }
        }
