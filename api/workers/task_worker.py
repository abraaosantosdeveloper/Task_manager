"""
Task Worker - Business logic for task management
"""
from api.repositories.task_repository import TaskRepository

class TaskWorker:
    """Handles task management business logic"""
    
    def __init__(self):
        self.task_repo = TaskRepository()
    
    def create_task(self, user_id, title, description, status='pending'):
        """Create a new task"""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")
        
        if status not in ['pending', 'in_progress', 'completed']:
            raise ValueError("Invalid status")
        
        task_id = self.task_repo.create_task(user_id, title, description, status)
        
        return {
            "id": task_id,
            "title": title,
            "description": description,
            "status": status
        }
    
    def get_all_tasks(self, user_id):
        """Get all tasks for a user"""
        tasks = self.task_repo.find_all_by_user(user_id)
        return tasks
    
    def get_task(self, task_id, user_id):
        """Get a specific task"""
        task = self.task_repo.find_by_id(task_id, user_id)
        if not task:
            raise ValueError("Task not found")
        return task
    
    def update_task(self, task_id, user_id, title, description):
        """Update a task"""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")
        
        # Check if task exists
        task = self.task_repo.find_by_id(task_id, user_id)
        if not task:
            raise ValueError("Task not found")
        
        success = self.task_repo.update_task(task_id, user_id, title, description)
        
        if not success:
            raise ValueError("Failed to update task")
        
        return self.get_task(task_id, user_id)
    
    def update_status(self, task_id, user_id, status):
        """Update task status"""
        if status not in ['pending', 'in_progress', 'completed']:
            raise ValueError("Invalid status")
        
        # Check if task exists
        task = self.task_repo.find_by_id(task_id, user_id)
        if not task:
            raise ValueError("Task not found")
        
        success = self.task_repo.update_status(task_id, user_id, status)
        
        if not success:
            raise ValueError("Failed to update status")
        
        return self.get_task(task_id, user_id)
    
    def delete_task(self, task_id, user_id):
        """Delete a task"""
        # Check if task exists
        task = self.task_repo.find_by_id(task_id, user_id)
        if not task:
            raise ValueError("Task not found")
        
        success = self.task_repo.delete_task(task_id, user_id)
        
        if not success:
            raise ValueError("Failed to delete task")
        
        return True
    
    def get_statistics(self, user_id):
        """Get task statistics"""
        stats = self.task_repo.get_statistics(user_id)
        return stats
