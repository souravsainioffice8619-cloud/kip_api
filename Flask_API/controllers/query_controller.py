from flask import  jsonify
from psycopg2.extras import RealDictCursor
from db_utils import get_connection
from db_utils import save_error_log
from flask import request

def query_execution(table, limit, sql):  
    if not table:
        save_error_log(Exception("Missing table parameter"), request.path)
        return jsonify({"msg": "Missing table parameter"}), 400
    if not limit or limit <= 0:
        save_error_log(Exception("Invalid limit parameter"), request.path)
        return jsonify({"msg": "Invalid limit parameter"}), 400  
    params = [limit,]
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return jsonify({"rows": rows})
    except Exception as e:
        save_error_log(e, request.path)
        return jsonify({"msg": "DB error", "error": str(e)}), 500
    finally:
        conn.close()