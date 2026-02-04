from flask import Blueprint, jsonify, request
from jwt_utils import jwt_required
from .utils import get_device_info

device_bp = Blueprint('device', __name__)


@device_bp.route('/device', methods=['GET'])
@jwt_required
def device_info():
    """Return device info extracted from the incoming request. Protected by JWT."""
    info = get_device_info(request)
    # include authenticated subject from JWT
    info['auth'] = request.jwt_payload.get('sub') if getattr(request, 'jwt_payload', None) else None
    return jsonify(info)
