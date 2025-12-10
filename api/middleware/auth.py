"""
Authentication Middleware
"""
from functools import wraps
from flask import request
from api.workers.auth_worker import AuthWorker
from api.utils.responses import unauthorized_response, error_response

auth_worker = AuthWorker()

def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    Usage: @token_required above route function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        print(f"[Auth Middleware] Authorization header: {auth_header[:50] + '...' if auth_header and len(auth_header) > 50 else auth_header}")
        
        if auth_header:
            try:
                # Expected format: "Bearer <token>"
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token = parts[1]
                    print(f"[Auth Middleware] Token extraído: {token[:20]}...")
                else:
                    print(f"[Auth Middleware] Formato inválido: {len(parts)} partes, primeira: {parts[0] if parts else 'N/A'}")
            except Exception as e:
                print(f"[Auth Middleware] Erro ao processar header: {e}")
                return unauthorized_response("Invalid authorization header format")
        
        if not token:
            print("[Auth Middleware] ERRO: Token não encontrado no header!")
            return unauthorized_response("Token is missing")
        
        try:
            # Verify token and get user
            current_user = auth_worker.get_user_from_token(token)
            
            # Add user to request context
            request.current_user = current_user
            
        except ValueError as e:
            return unauthorized_response(str(e))
        except Exception as e:
            print(f"Authentication error: {e}")
            return error_response("Authentication failed", status_code=401)
        
        return f(*args, **kwargs)
    
    return decorated

def get_current_user():
    """Get current authenticated user from request context"""
    return getattr(request, 'current_user', None)
