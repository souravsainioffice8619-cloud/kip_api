from functools import wraps
from flask import request, jsonify
import jwt
import datetime
import os
from dotenv import load_dotenv

# Load .env (if present)
load_dotenv()

JWT_SECRET = os.environ.get('JWT_SECRET', 'supersecretkey123')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXP_MINUTES = int(os.environ.get('JWT_EXP_MINUTES', '60'))

__all__ = ['create_token', 'jwt_required']


def create_token(username: str) -> str:
    """Create a signed JWT for the given username."""
    payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def jwt_required(f):
    """Decorator that enforces a valid JWT in the Authorization header (Bearer).

    API-only behavior: return JSON 401 on missing/invalid/expired tokens.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Prefer cookie-based token for browser flows
        token = request.cookies.get('access_token')

        # 1) check Authorization header for Bearer token (if no cookie)
        if not token:
            auth = request.headers.get('Authorization', None)
            if auth:
                parts = auth.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token = parts[1]
                else:
                    return jsonify({'msg': 'Invalid Authorization header format. Expected: Bearer <token>'}), 401

        # 2) fallback to query param
        if not token:
            token = request.args.get('token')

        if not token:
            return jsonify({'msg': 'Missing token'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            resp = jsonify({'msg': 'Token expired'})
            if request.cookies.get('access_token'):
                resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
            return resp, 401
        except jwt.InvalidTokenError:
            resp = jsonify({'msg': 'Invalid token'})
            if request.cookies.get('access_token'):
                resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
            return resp, 401

        return f(*args, **kwargs)
    return decorated
