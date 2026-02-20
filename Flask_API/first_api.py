from flask import Flask, render_template, request, abort
import os
from dotenv import load_dotenv
from controllers import register_blueprints
from db_utils import add_log_entry, save_request_to_db
import json
import time
from flask import g
from waitress import serve
import socket
from controllers.utils import get_device_info


# from waitress import serve


# load .env
load_dotenv()

app = Flask(__name__)

# Block requests that try to access Werkzeug debugger resources unless
# the app is running in debug mode and the request comes from localhost.
@app.before_request
def before_request_logging():
    g.start_time = time.time()
    # Log the request
    if not request.path.startswith('/log'):
        log_message = {
            "method": request.method,
            "path": request.path,
            "ip": request.remote_addr,
            "headers": dict(request.headers)
        }
        add_log_entry("INFO", json.dumps(log_message))
    
    # Deny debugger queries
    if '__debugger__' in request.args:
        # Allow only in debug mode and from localhost
        if app.debug and (request.remote_addr == '127.0.0.1' or request.remote_addr == '::1'):
            return
        abort(404)

# --- HOOK 2: Log the data after the response is ready ---
@app.after_request
def log_request_info(response):
    # Calculate duration
    diff = time.time() - g.start_time
    duration_ms = int(diff * 1000)

    # Capture data
    log_data = {
        "method": request.method,
        "path": request.path,
        "ip": request.remote_addr,
        "status": response.status_code,
        "duration": duration_ms
    }

    # Save to Database
    save_request_to_db(log_data)
    
    return response


# register controllers (blueprints)
register_blueprints(app)

def get_local_ip():
    """Function to find the actual local network IP of this laptop"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # We don't actually connect, but this tells us which IP we are using to talk to the world
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    # run with: python first_api.py
    # app.run(host="0.0.0.0", port=5000,threaded=True)
    port = 5000
    local_ip = get_local_ip()
    
    print("=" * 50)
    print("🚀 WAITRESS PROD SERVER STARTED")
    print(f"🔗 Local:   http://localhost:{port}")
    print(f"🌍 Network: http://{local_ip}:{port}")
    print("=" * 50)
    print("Press Ctrl+C to quit\n")
    serve(app, host='0.0.0.0', port=5000, threads=6)
    #  # --- PRODUCTION CONFIGURATION ---
    # host = "0.0.0.0"
    # port = 5000
    # threads = 6  # Number of concurrent threads to handle requests
    
    # print(f"Waitress is serving '{app.name}' on http://{host}:{port}")
    
    # # Use serve() instead of app.run()
    # serve(
    #     app, 
    #     host=host, 
    #     port=port, 
    #     threads=threads
    # )

