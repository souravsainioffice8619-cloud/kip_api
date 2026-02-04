from flask import Blueprint, send_file, request
from jwt_utils import jwt_required
from .utils import get_device_info

main_bp = Blueprint('main', __name__)


@main_bp.route('/image')
@jwt_required
def hello_world():
    print("Hello, World!")
    return "<h1>Hello, Rajan ........!</h1>"


# send an image
@main_bp.route('/')
# @jwt_required
def send_image():
    """Return device info extracted from the incoming request then send an image."""
    info = get_device_info(request)
    print(info)
    return send_file("static/sample_image.jpg", mimetype='image/jpeg')