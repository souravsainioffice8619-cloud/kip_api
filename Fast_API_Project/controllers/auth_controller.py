from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import jwt

from jwt_utils import JWT_EXP_MINUTES, create_token, verify_token
from user_store import add_user, get_user, verify_user

auth_router = APIRouter()


async def _read_json_body(request: Request):
    if "application/json" not in request.headers.get("content-type", ""):
        return None
    try:
        return await request.json()
    except Exception:
        return {}


@auth_router.api_route("/login", methods=["POST", "GET"])
async def login(request: Request):
    """Login endpoint that supports token validation or username/password auth."""
    data = await _read_json_body(request)
    if data is None:
        return JSONResponse(
            status_code=400,
            content={"msg": "Content-Type must be application/json"},
        )

    token = data.get("token")
    if token:
        try:
            payload = verify_token(token)
            return {"valid": True, "payload": payload}
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"valid": False, "msg": "Token expired"},
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"valid": False, "msg": "Invalid token"},
            )

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return JSONResponse(
            status_code=400,
            content={"msg": "username and password are required"},
        )

    if verify_user(username, password):
        access_token = create_token(username)
        max_age = JWT_EXP_MINUTES * 60 if JWT_EXP_MINUTES else None
        response = JSONResponse(
            content={
                "access_token": access_token,
                "expires_in": max_age,
            }
        )
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            samesite="Lax",
            secure=(request.url.scheme == "https"),
            max_age=max_age,
        )
        return response

    return JSONResponse(status_code=401, content={"msg": "Invalid credentials"})


@auth_router.api_route("/register", methods=["POST", "GET"])
async def register(request: Request):
    """Registration endpoint: expects JSON {'username', 'password'}."""
    data = await _read_json_body(request)
    if data is None:
        return JSONResponse(
            status_code=400,
            content={"msg": "Content-Type must be application/json"},
        )

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JSONResponse(
            status_code=400,
            content={"msg": "username and password are required"},
        )

    if len(password) < 6:
        return JSONResponse(
            status_code=400,
            content={"msg": "password must be at least 6 characters"},
        )

    if get_user(username):
        return JSONResponse(status_code=409, content={"msg": "User already exists"})

    try:
        add_user(username, password)
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={"msg": "Server error", "error": str(exc)},
        )

    access_token = create_token(username)
    seconds_in_12_hours = 12 * 60 * 60
    response = JSONResponse(
        status_code=201,
        content={
            "msg": "User registered successfully",
            "access_token": access_token,
            "expires_in": seconds_in_12_hours,
        },
    )
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        samesite="Lax",
        secure=(request.url.scheme == "https"),
        max_age=seconds_in_12_hours,
    )
    return response


@auth_router.api_route("/logout", methods=["POST", "GET"])
def logout():
    """Clear the access_token cookie to log the user out."""
    response = JSONResponse(content={"msg": "Logged out"})
    response.set_cookie("access_token", "", expires=0, httponly=True, samesite="Lax")
    return response
