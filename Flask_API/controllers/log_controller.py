from flask import Blueprint, request, jsonify
from psycopg2.extras import RealDictCursor
from db_utils import get_connection

log_bp = Blueprint("log", __name__, url_prefix="/log")

@log_bp.route("/init", methods=["GET"])
def init_logs_table():
    """Create the logs table if it doesn't exist."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    level VARCHAR(50),
                    message TEXT
                )
            """)
            conn.commit()
            return jsonify({"msg": "Logs table created or already exists."})
    except Exception as e:
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()

@log_bp.route("/", methods=["POST"])
def add_log():
    """
    Add a log entry.

    JSON body:
    {
        "level": "INFO",
        "message": "This is a log message."
    }
    """
    body = request.get_json()
    if not body or "message" not in body:
        return jsonify({"msg": "Missing message in request body"}), 400

    level = body.get("level", "INFO")
    message = body.get("message")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO logs (level, message) VALUES (%s, %s)",
                (level, message)
            )
            conn.commit()
            return jsonify({"msg": "Log entry added."}), 201
    except Exception as e:
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()
