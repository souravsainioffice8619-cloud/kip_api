from flask import Blueprint, request, jsonify
from psycopg2 import  sql as pgsql
from psycopg2.extras import RealDictCursor
from jwt_utils import jwt_required
from db_utils import get_connection

db_bp = Blueprint("db", __name__, url_prefix="/db")

@db_bp.route("/tables", methods=["GET"])
# @jwt_required
def list_tables():
    """Return a list of table names in the public schema."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            tables = [row[0] for row in cur.fetchall()]
            return jsonify({"tables": tables})
    except Exception as e:
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()

@db_bp.route("/query", methods=["POST","GET"])
# @jwt_required
def query():
    """
    Execute a safe, read-only SQL query.

    JSON body:
    {
        "sql": "SELECT * FROM users WHERE id = %s",
        "params": [1]
    }

    http://localhost:5000/db/query?city=Beijing&limit=1000
    city = request.args.get("city")
    limit = request.args.get("limit", type=int)

    or
    {
        "sql": "SELECT * FROM weather WHERE city = %s LIMIT %s",
        "params": ["Beijing", 1000]
    }
    """

    body = request.get_json() or {}
    sql = body.get("sql")
    params = body.get("params", [])

    if not sql or not isinstance(sql, str):
        return jsonify({"msg": "Missing or invalid sql"}), 400

    # Safety checks
    sql_stripped = sql.strip().lower()
    if not sql_stripped.startswith("select"):
        return jsonify({"msg": "Only SELECT queries are allowed"}), 400
    if ";" in sql:
        return jsonify({"msg": "Semicolons are not allowed"}), 400

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()


@db_bp.route("/city", methods=["POST","GET"])
# @jwt_required
def city():
    """ Query weather data for a specific city with an optional limit.
        http://localhost:5000/db/query?city=Beijing&limit=1000
    """
    city = request.args.get("city")
    limit = request.args.get("limit", type=int) or 1000
    table = request.args.get("table") 
    if not city:
        return jsonify({"msg": "Missing city parameter"}), 400
    if not table:
        return jsonify({"msg": "Missing table parameter"}), 400
    sql = pgsql.SQL("SELECT * FROM {} WHERE city = %s LIMIT %s").format(pgsql.Identifier(table))
    params = [city, limit]
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return jsonify({"rows": rows})
    except Exception as e:
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()