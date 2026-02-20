from fastapi import APIRouter, Depends, Request

from jwt_utils import jwt_required
from .utils import get_device_info

device_router = APIRouter()


@device_router.get("/device")
def device_info(request: Request, payload: dict = Depends(jwt_required)):
    """Return device info for the authenticated request."""
    info = get_device_info(request)
    info["auth"] = payload.get("sub")
    return info
