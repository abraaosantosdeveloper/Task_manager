"""
Task Repository - Database operations for tasks
"""
from api.utils.database import Database
from datetime import datetime

class TaskRepository:
    """Handles all database operations related to tasks"""
    
    def __init__(self):
        self.db = Database()
    
    def create_task(self, user_id, title, status='pending'):
        """Create a new task"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO tasks (user_id, title, status, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (user_id, title, status))
            conn.commit()
            
            task_id = cursor.lastrowid
            cursor.close()
            conn.close()
            
            return task_id
        except Exception as e:
            print(f"Error creating task: {e}")
            raise
    
    def find_all_by_user(self, user_id):
        """Get all tasks for a user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, title, status, created_at, completed_at
                FROM tasks
                WHERE user_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(query, (user_id,))
            tasks = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return tasks
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            raise
    
    def find_by_id(self, task_id, user_id):
        """Get a specific task by ID for a user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, title, status, created_at, completed_at
                FROM tasks
                WHERE id = %s AND user_id = %s
            """
            cursor.execute(query, (task_id, user_id))
            task = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return task
        except Exception as e:
            print(f"Error finding task: {e}")
            raise
    
    def update_task(self, task_id, user_id, title):
        """Update a task"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE tasks
                SET title = %s
                WHERE id = %s AND user_id = %s
            """
            cursor.execute(query, (title, task_id, user_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating task: {e}")
            raise
    
    def update_status(self, task_id, user_id, status):
        """Update task status"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            completed_at = datetime.now() if status == 'completed' else None
            
            query = """
                UPDATE tasks
                SET status = %s, completed_at = %s
                WHERE id = %s AND user_id = %s
            """
            cursor.execute(query, (status, completed_at, task_id, user_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error updating task status: {e}")
            raise
    
    def delete_task(self, task_id, user_id):
        """Delete a task"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM tasks WHERE id = %s AND user_id = %s"
            cursor.execute(query, (task_id, user_id))
            conn.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error deleting task: {e}")
            raise
    
    def get_statistics(self, user_id):
        """Get task statistics for a user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM tasks
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            stats = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return stats
        except Exception as e:
            print(f"Error getting statistics: {e}")
            raise
