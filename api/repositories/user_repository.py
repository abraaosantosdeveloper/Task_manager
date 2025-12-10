"""
User Repository - Database operations for users
"""
from api.utils.database import Database
import bcrypt

class UserRepository:
    """Handles all database operations related to users"""
    
    def __init__(self):
        self.db = Database()
    
    def create_user(self, email, password, name):
        """Create a new user"""
        try:
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO users (email, password, name, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (email, hashed_password, name))
            conn.commit()
            
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
    
    def find_by_email(self, email):
        """Find user by email"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return user
        except Exception as e:
            print(f"Error finding user by email: {e}")
            raise
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT id, email, name, created_at FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return user
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            raise
    
    def verify_password(self, plain_password, hashed_password):
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password if isinstance(hashed_password, bytes) else hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
    
    def email_exists(self, email):
        """Check if email already exists"""
        user = self.find_by_email(email)
        return user is not None
    
    def update_user(self, user_id, name, email, new_password=None):
        """Update user information"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if new_password:
                # Hash new password
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                query = """
                    UPDATE users 
                    SET name = %s, email = %s, password = %s
                    WHERE id = %s
                """
                cursor.execute(query, (name, email, hashed_password, user_id))
            else:
                query = """
                    UPDATE users 
                    SET name = %s, email = %s
                    WHERE id = %s
                """
                cursor.execute(query, (name, email, user_id))
            
            conn.commit()
            
            # Get updated user
            cursor.execute("SELECT id, email, name, created_at FROM users WHERE id = %s", (user_id,))
            updated_user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return updated_user
        except Exception as e:
            print(f"Error updating user: {e}")
            raise
