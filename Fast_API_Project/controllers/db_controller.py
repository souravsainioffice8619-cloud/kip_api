from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from psycopg2 import sql as pgsql
from psycopg2.extras import RealDictCursor

from db_utils import get_connection
from jwt_utils import jwt_required

db_router = APIRouter(prefix="/db")


@db_router.get("/tables")
def list_tables(_: dict = Depends(jwt_required)):
    """Return a list of table names in the public schema."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
            tables = [row[0] for row in cur.fetchall()]
            return {"tables": tables}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"msg": "DB error", "error": str(exc)})
    finally:
        conn.close()


@db_router.api_route("/query", methods=["POST", "GET"])
async def query(request: Request):
    """
    Execute a safe read-only SQL query.

    JSON body:
    {
        "sql": "SELECT * FROM users WHERE id = %s",
        "params": [1]
    }
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    sql = body.get("sql")
    params = body.get("params", [])

    if not sql or not isinstance(sql, str):
        return JSONResponse(status_code=400, content={"msg": "Missing or invalid sql"})

    sql_stripped = sql.strip().lower()
    if not sql_stripped.startswith("select"):
        return JSONResponse(status_code=400, content={"msg": "Only SELECT queries are allowed"})
    if ";" in sql:
        return JSONResponse(status_code=400, content={"msg": "Semicolons are not allowed"})

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return {"rows": rows}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"msg": "DB error", "error": str(exc)})
    finally:
        conn.close()


@db_router.api_route("/city", methods=["POST", "GET"])
def city(
    city: str | None = Query(default=None),
    limit: int = Query(default=1000),
    table: str | None = Query(default=None),
):
    """Query table data for a specific city with optional limit."""
    if not city:
        return JSONResponse(status_code=400, content={"msg": "Missing city parameter"})
    if not table:
        return JSONResponse(status_code=400, content={"msg": "Missing table parameter"})

    sql = pgsql.SQL("SELECT * FROM {} WHERE city = %s LIMIT %s").format(pgsql.Identifier(table))
    params = [city, limit]

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return {"rows": rows}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"msg": "DB error", "error": str(exc)})
    finally:
        conn.close()
