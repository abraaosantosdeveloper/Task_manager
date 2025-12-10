"""
HTTP status codes and response utilities
"""
from flask import jsonify

# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500

def success_response(data=None, message="Success", status_code=HTTP_200_OK):
    """Standard success response"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="Error", errors=None, status_code=HTTP_400_BAD_REQUEST):
    """Standard error response"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code

def created_response(data=None, message="Resource created successfully"):
    """Response for resource creation"""
    return success_response(data, message, HTTP_201_CREATED)

def unauthorized_response(message="Unauthorized access"):
    """Response for unauthorized access"""
    return error_response(message, status_code=HTTP_401_UNAUTHORIZED)

def not_found_response(message="Resource not found"):
    """Response for not found resources"""
    return error_response(message, status_code=HTTP_404_NOT_FOUND)

def validation_error_response(errors, message="Validation failed"):
    """Response for validation errors"""
    return error_response(message, errors, HTTP_422_UNPROCESSABLE_ENTITY)

def server_error_response(message="Internal server error"):
    """Response for server errors"""
    return error_response(message, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
