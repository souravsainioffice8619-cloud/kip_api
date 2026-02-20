from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse

from jwt_utils import jwt_required
from .utils import get_device_info

main_router = APIRouter()

STATIC_IMAGE = Path(__file__).resolve().parent.parent / "static" / "sample_image.jpg"


@main_router.get("/image")
def hello_world(_: dict = Depends(jwt_required)):
    return HTMLResponse("<h1>Hello, Rajan ........!</h1>")


@main_router.get("/")
def send_image(request: Request):
    """Return sample image when available; fallback to request/device info."""
    if STATIC_IMAGE.exists():
        return FileResponse(path=str(STATIC_IMAGE), media_type="image/jpeg")
    return get_device_info(request)
