from flask import Blueprint, request, jsonify
from jwt_utils import create_token, JWT_EXP_MINUTES

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST','GET'])
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
        resp = jsonify({'access_token': token, 'expires_in': JWT_EXP_MINUTES * 60*720})
        # set HttpOnly cookie so browsers store token securely
        max_age = JWT_EXP_MINUTES * 60 if JWT_EXP_MINUTES else None
        resp.set_cookie('access_token', token, httponly=True, samesite='Lax', secure=request.is_secure, max_age=max_age)
        return resp

    return jsonify({'msg': 'Invalid credentials'}), 401

# Import this for password hashing if your user_store supports it
# from werkzeug.security import generate_password_hash 

@auth_bp.route('/register', methods=['POST','GET'])
def register():
    """API-only registration endpoint.
    Expects JSON {'username', 'password'}
    """
    if not request.is_json:
        return jsonify({'msg': 'Content-Type must be application/json'}), 400

    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    # 1. Validation
    if not username or not password:
        return jsonify({'msg': 'username and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'msg': 'password must be at least 6 characters'}), 400

    # 2. Check if user exists
    from user_store import get_user  # Assuming this helper exists
    if get_user(username):
        return jsonify({'msg': 'User already exists'}), 409

    # 3. Save User
    from user_store import add_user 
    try:
        # It is highly recommended to hash passwords before saving!
        # hashed_pw = generate_password_hash(password)
        # add_user(username, hashed_pw)
        
        success = add_user(username, password)
        if not success:
            return jsonify({'msg': 'Registration failed'}), 500
            
    except Exception as e:
        return jsonify({'msg': 'Server error', 'error': str(e)}), 500

    # 4. Success Response
    # Optionally: create a token immediately so they are logged in
    token = create_token(username)
    
    # Correct math for 12 hours: 12 * 60 minutes * 60 seconds = 43200
    seconds_in_12_hours = 12 * 60 * 60 
    
    resp = jsonify({
        'msg': 'User registered successfully',
        'access_token': token,
        'expires_in': seconds_in_12_hours
    })
    
    # Set the cookie so the browser logs them in automatically
    resp.set_cookie(
        'access_token', 
        token, 
        httponly=True, 
        samesite='Lax', 
        secure=request.is_secure, 
        max_age=seconds_in_12_hours
    )
    
    return resp, 201

@auth_bp.route('/logout', methods=['POST','GET'])
def logout():
    """Clear the access_token cookie to log the user out."""
    resp = jsonify({'msg': 'Logged out'})
    resp.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    return resp

