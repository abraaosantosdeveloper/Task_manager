"""
Task Routes
"""
from flask import Blueprint
from api.controllers import task_controller
from api.middleware.auth import token_required, get_current_user

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('', methods=['GET'])
@token_required
def get_all_tasks():
    """Get all tasks"""
    return task_controller.get_all_tasks(get_current_user())

@task_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
    """Get a specific task"""
    return task_controller.get_task(task_id, get_current_user())

@task_bp.route('', methods=['POST'])
@token_required
def create_task():
    """Create a new task"""
    return task_controller.create_task(get_current_user())

@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    """Update a task"""
    return task_controller.update_task(task_id, get_current_user())

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
@token_required
def update_task_status(task_id):
    """Update task status"""
    return task_controller.update_task_status(task_id, get_current_user())

@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    """Delete a task"""
    return task_controller.delete_task(task_id, get_current_user())

@task_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics():
    """Get task statistics"""
    return task_controller.get_statistics(get_current_user())
