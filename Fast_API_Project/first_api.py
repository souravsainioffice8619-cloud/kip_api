import json
import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from controllers import register_routers
from db_utils import add_log_entry, save_request_to_db

load_dotenv()

app = FastAPI(title="Fast API Project")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    request.state.start_time = start_time

    client_host = request.client.host if request.client else None

    try:
        if not request.url.path.startswith("/log"):
            log_message = {
                "method": request.method,
                "path": request.url.path,
                "ip": client_host,
                "headers": dict(request.headers),
            }
            add_log_entry("INFO", json.dumps(log_message))
    except Exception as exc:
        print(f"Request pre-log failed: {exc}")

    if "__debugger__" in request.query_params:
        debug_enabled = os.getenv("FASTAPI_DEBUG", "0").lower() in {"1", "true", "yes"}
        if not (debug_enabled and client_host in {"127.0.0.1", "::1", "localhost"}):
            return JSONResponse(status_code=404, content={"detail": "Not Found"})

    response = await call_next(request)

    try:
        duration_ms = int((time.time() - start_time) * 1000)
        log_data = {
            "method": request.method,
            "path": request.url.path,
            "ip": client_host,
            "status": response.status_code,
            "duration": duration_ms,
        }
        save_request_to_db(log_data)
    except Exception as exc:
        print(f"Request post-log failed: {exc}")

    return response


register_routers(app)


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FASTAPI_DEBUG", "0").lower() in {"1", "true", "yes"}
    uvicorn.run("first_api:app", host=host, port=port, reload=debug)
