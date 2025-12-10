"""
Task Manager API - Main Entry Point for Vercel
"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.routes.auth_routes import auth_bp
from api.routes.task_routes import task_bp
from api.utils.config import Config
from api.utils.database import Database

# Create Flask app
app = Flask(__name__)

# CORS Configuration
CORS(app, 
     origins=Config.CORS_ORIGINS,
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(task_bp, url_prefix='/api/tasks')

# Health check endpoint
@app.route('/')
@app.route('/api')
def health_check():
    """API health check"""
    return jsonify({
        "success": True,
        "message": "Task Manager API is running",
        "version": "2.0.0",
        "endpoints": {
            "auth": {
                "register": "POST /api/auth/register",
                "login": "POST /api/auth/login",
                "me": "GET /api/auth/me (requires token)"
            },
            "tasks": {
                "list": "GET /api/tasks (requires token)",
                "get": "GET /api/tasks/:id (requires token)",
                "create": "POST /api/tasks (requires token)",
                "update": "PUT /api/tasks/:id (requires token)",
                "update_status": "PUT /api/tasks/:id/status (requires token)",
                "delete": "DELETE /api/tasks/:id (requires token)",
                "statistics": "GET /api/tasks/statistics (requires token)"
            }
        }
    })

# Database connection test endpoint
@app.route('/api/health/database')
def database_health():
    """Test database connection"""
    try:
        is_connected = Database.test_connection()
        if is_connected:
            return jsonify({
                "success": True,
                "message": "Database connection successful"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Database connection failed"
            }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Database error: {str(e)}"
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

# For local development
if __name__ == '__main__':
    print("🚀 Starting Task Manager API...")
    print(f"📊 Environment: {Config.FLASK_ENV}")
    print(f"🔌 Port: {Config.PORT}")
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.FLASK_DEBUG
    )
