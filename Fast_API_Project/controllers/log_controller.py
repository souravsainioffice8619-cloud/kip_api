from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from db_utils import get_connection

log_router = APIRouter(prefix="/log")


@log_router.get("/init")
def init_logs_table():
    """Create logs table if it doesn't exist."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    level VARCHAR(50),
                    message TEXT
                )
                """
            )
            conn.commit()
            return {"msg": "Logs table created or already exists."}
    except Exception as exc:
        return JSONResponse(status_code=500, content={"msg": "DB error", "error": str(exc)})
    finally:
        conn.close()


@log_router.post("/")
async def add_log(request: Request):
    """
    Add a log entry.

    JSON body:
    {
        "level": "INFO",
        "message": "This is a log message."
    }
    """
    try:
        body = await request.json()
    except Exception:
        body = None

    if not body or "message" not in body:
        return JSONResponse(status_code=400, content={"msg": "Missing message in request body"})

    level = body.get("level", "INFO")
    message = body.get("message")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO logs (level, message) VALUES (%s, %s)",
                (level, message),
            )
            conn.commit()
            return JSONResponse(status_code=201, content={"msg": "Log entry added."})
    except Exception as exc:
        return JSONResponse(status_code=500, content={"msg": "DB error", "error": str(exc)})
    finally:
        conn.close()
