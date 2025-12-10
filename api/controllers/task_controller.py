"""
Task Controller
Handles HTTP requests for task management
"""
from flask import request
from api.workers.task_worker import TaskWorker
from api.utils.responses import (
    success_response, error_response, created_response,
    validation_error_response, server_error_response, not_found_response
)

task_worker = TaskWorker()

def get_all_tasks(current_user):
    """Get all tasks for current user"""
    try:
        user_id = current_user['id']
        tasks = task_worker.get_all_tasks(user_id)
        
        return success_response(tasks)
        
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return server_error_response()

def get_task(task_id, current_user):
    """Get a specific task"""
    try:
        user_id = current_user['id']
        task = task_worker.get_task(task_id, user_id)
        
        return success_response(task)
        
    except ValueError as e:
        return not_found_response(str(e))
    except Exception as e:
        print(f"Error fetching task: {e}")
        return server_error_response()

def create_task(current_user):
    """Create a new task"""
    try:
        data = request.get_json()
        user_id = current_user['id']
        
        # Validation
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        status = data.get('status', 'pending')
        
        errors = {}
        if not title:
            errors['title'] = "Title is required"
        if status not in ['pending', 'in_progress', 'completed']:
            errors['status'] = "Invalid status"
        
        if errors:
            return validation_error_response(errors)
        
        # Create task
        result = task_worker.create_task(user_id, title, description, status)
        
        return created_response(result, "Task created successfully")
        
    except ValueError as e:
        return error_response(str(e))
    except Exception as e:
        print(f"Error creating task: {e}")
        return server_error_response()

def update_task(task_id, current_user):
    """Update a task"""
    try:
        data = request.get_json()
        user_id = current_user['id']
        
        # Validation
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        errors = {}
        if not title:
            errors['title'] = "Title is required"
        
        if errors:
            return validation_error_response(errors)
        
        # Update task
        result = task_worker.update_task(task_id, user_id, title, description)
        
        return success_response(result, "Task updated successfully")
        
    except ValueError as e:
        return not_found_response(str(e))
    except Exception as e:
        print(f"Error updating task: {e}")
        return server_error_response()

def update_task_status(task_id, current_user):
    """Update task status"""
    try:
        data = request.get_json()
        user_id = current_user['id']
        
        # Validation
        status = data.get('status', '').strip()
        
        if status not in ['pending', 'in_progress', 'completed']:
            return validation_error_response({"status": "Invalid status"})
        
        # Update status
        result = task_worker.update_status(task_id, user_id, status)
        
        return success_response(result, "Status updated successfully")
        
    except ValueError as e:
        return not_found_response(str(e))
    except Exception as e:
        print(f"Error updating status: {e}")
        return server_error_response()

def delete_task(task_id, current_user):
    """Delete a task"""
    try:
        user_id = current_user['id']
        
        # Delete task
        task_worker.delete_task(task_id, user_id)
        
        return success_response(message="Task deleted successfully")
        
    except ValueError as e:
        return not_found_response(str(e))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return server_error_response()

def get_statistics(current_user):
    """Get task statistics"""
    try:
        user_id = current_user['id']
        stats = task_worker.get_statistics(user_id)
        
        return success_response(stats)
        
    except Exception as e:
        print(f"Error fetching statistics: {e}")
        return server_error_response()
