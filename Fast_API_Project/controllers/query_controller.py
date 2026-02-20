from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

from db_utils import get_connection, save_error_log


def query_execution(table, limit, sql, endpoint_name):
    if not table:
        save_error_log(Exception("Missing table parameter"), endpoint_name)
        raise HTTPException(status_code=400, detail="Missing table parameter")
    if not limit or limit <= 0:
        save_error_log(Exception("Invalid limit parameter"), endpoint_name)
        raise HTTPException(status_code=400, detail="Invalid limit parameter")

    params = [limit]
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return {"rows": rows}
    except Exception as exc:
        save_error_log(exc, endpoint_name)
        raise HTTPException(
            status_code=500,
            detail=f"DB error: {exc}",
        ) from exc
    finally:
        conn.close()
