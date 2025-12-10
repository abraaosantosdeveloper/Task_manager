"""
Keep Alive Routes - Simple endpoint to prevent database sleep
"""
from flask import Blueprint
from api.utils.database import Database
from api.utils.responses import success_response, server_error_response

keep_alive_bp = Blueprint('keep_alive', __name__)

@keep_alive_bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint to keep database active
    No authentication required - designed for cron jobs
    """
    try:
        db = Database()
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query dummy table to keep database active
        query = "SELECT * FROM dummy_data LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return success_response({
            "status": "alive",
            "dummy_data": result
        }, "Database is active")
        
    except Exception as e:
        print(f"Keep-alive error: {e}")
        return server_error_response("Database connection failed")

@keep_alive_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint without database query
    """
    return success_response({
        "status": "healthy",
        "service": "Task Manager API",
        "version": "2.0.0"
    }, "API is running")
