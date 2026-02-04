from flask import Blueprint, request, jsonify
from jwt_utils import create_token, JWT_EXP_MINUTES

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """API-only login endpoint.

    Behavior:
    - If JSON contains a 'token', verify and return its payload (or error).
    - Otherwise expects JSON {'username','password'} and returns a JWT on success.
    """
    if not request.is_json:
        return jsonify({'msg': 'Content-Type must be application/json'}), 400

    data = request.get_json() or {}

    # If a token is provided, verify it and return the payload
    token = data.get('token')
    if token:
        try:
            from jwt_utils import verify_token
            payload = verify_token(token)
            return jsonify({'valid': True, 'payload': payload})
        except Exception as e:
            import jwt
            if isinstance(e, jwt.ExpiredSignatureError):
                return jsonify({'valid': False, 'msg': 'Token expired'}), 401
            return jsonify({'valid': False, 'msg': 'Invalid token'}), 401

    # Otherwise process username/password login
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'msg': 'username and password are required'}), 400

    # verify credentials against user store
    from user_store import verify_user

    if verify_user(username, password):
        token = create_token(username)
        resp = jsonify({'access_token': token, 'expires_in': JWT_EXP_MINUTES * 60})
        # set HttpOnly cookie so browsers store token securely
        max_age = JWT_EXP_MINUTES * 60 if JWT_EXP_MINUTES else None
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', secure=request.is_secure, max_age=max_age)
        return resp

    return jsonify({'msg': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear the access_token cookie to log the user out."""
    resp = jsonify({'msg': 'Logged out'})
    resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    return resp
